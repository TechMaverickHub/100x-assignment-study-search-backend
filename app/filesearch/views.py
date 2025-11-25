from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404, ListAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from app.global_constants import SuccessMessage, ErrorMessage
from app.utils import get_response_schema
from permissions import IsUser
from .gemini_client import GeminiClientWrapper
from .models import FileSearchStore
from .processing import process_file_search_store
from .serializers import FileSearchStoreSerializer, FileUploadSerializer, QuerySerializer


class TestAPIView(GenericAPIView):

    def post(self, request):

       return get_response_schema({}, SuccessMessage.RECORD_UPDATED.value, status.HTTP_200_OK)


import logging
logger = logging.getLogger(__name__)


class CreateFileSearchStoreView(GenericAPIView):
    """Create an (empty) FileSearchStore record. POST /api/filesearch/stores/"""
    permission_classes = [IsUser]
    serializer_class = FileSearchStoreSerializer

    @swagger_auto_schema(
        operation_description='Create a FileSearchStore record (no file upload).',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Optional title'),
            }
        ),
        responses={201: FileSearchStoreSerializer}
    )
    def post(self, request):
        title = request.data.get('title') or 'Untitled Document'
        store = FileSearchStore.objects.create(
            user=request.user,
            title=title
        )
        serializer = self.get_serializer(store)
        return get_response_schema(serializer.data, SuccessMessage.RECORD_CREATED.value, status.HTTP_201_CREATED)


class DocumentUploadView(GenericAPIView):
    """Upload PDF and start ingestion (synchronous). POST /api/filesearch/upload/"""
    permission_classes = [IsUser]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FileUploadSerializer

    @swagger_auto_schema(
        operation_description='Upload a PDF file for ingestion. The file will be processed synchronously.',
        manual_parameters=[
            openapi.Parameter(name='file', in_=openapi.IN_FORM, type=openapi.TYPE_FILE, required=True, description='PDF file to upload'),
            openapi.Parameter(name='title', in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=False, description='Title for the document (defaults to filename)'),
        ],
        responses={201: openapi.Response('Document created successfully', FileSearchStoreSerializer)}
    )
    def post(self, request):
        try:
            if 'file' not in request.FILES:
                return_data = {
                    settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: [ErrorMessage.PDF_FILE_REQUIRED.value]
                }
                return get_response_schema(return_data, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

            uploaded_file = request.FILES['file']
            if not uploaded_file.name.lower().endswith('.pdf'):
                return_data = {
                    settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: [ErrorMessage.PDF_FILE_REQUIRED.value]
                }
                return get_response_schema(return_data, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

            title = request.data.get('title') or uploaded_file.name

            # Create DB record with UPLOADING status (do NOT mark READY here)
            document = FileSearchStore.objects.create(
                user=request.user,
                title=title,
                file=uploaded_file,
                status=FileSearchStore.StoreStatus.UPLOADING
            )

            # Synchronous processing: create Gemini store and upload file.
            # This will update document.status -> PROCESSING/READY/FAILED and set store_name or error_message.
            try:
                process_file_search_store(str(document.id))
            except Exception as proc_exc:
                logger.exception("Processing failed for document %s", document.id)
                # process_file_search_store already updates DB on failure; return the document state
                serializer = FileSearchStoreSerializer(document)
                return get_response_schema(serializer.data, ErrorMessage.SOMETHING_WENT_WRONG.value, status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = FileSearchStoreSerializer(document)
            return get_response_schema(serializer.data, SuccessMessage.RECORD_CREATED.value, status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception('Error uploading document')
            return_data = {
                settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: [ErrorMessage.SOMETHING_WENT_WRONG.value]
            }
            return get_response_schema(return_data, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)


class QueryDocumentView(GenericAPIView):
    """POST /api/filesearch/query/ - Query a specific document (by id) or latest user store if not provided"""
    permission_classes = [IsUser]
    serializer_class = QuerySerializer

    @swagger_auto_schema(
        operation_description='Query the uploaded document(s) via Gemini file search',
        request_body=QuerySerializer,
        responses={200: 'Query result (text and grounding metadata)'}
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data['query']
        document_id = serializer.validated_data.get('document_id')

        if document_id:
            document = get_object_or_404(FileSearchStore, id=document_id, user=request.user)
        else:
            # get the latest READY document for user
            document = FileSearchStore.objects.filter(user=request.user, status=FileSearchStore.StoreStatus.READY).order_by('-created').first()
            if not document:
                return_data = {
                    settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: [ErrorMessage.DOCUMENT_NOT_READY.value]
                }

                return get_response_schema(return_data, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        if not document.store_name:
            return_data = {
                settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: [ErrorMessage.DOCUMENT_NO_STORE.value]
            }

            return get_response_schema(return_data, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        try:
                client = GeminiClientWrapper()
                response = client.query_store(document.store_name, query)

                # Extract response text and grounding sources (best-effort)
                text = getattr(response, 'text', None) or (getattr(response, 'candidates', [None])[0].content if getattr(response, 'candidates', None) else '')
                grounding_sources = []
                try:
                    grounding = response.candidates[0].grounding_metadata
                    if grounding:
                        grounding_sources = [c.retrieved_context.title for c in grounding.grounding_chunks]
                except Exception:
                    grounding_sources = []

                return_data = {
                    'query': query,
                    'response_text': text,
                    'grounding_sources': grounding_sources,
                    'document_id': str(document.id),
                }

                return get_response_schema(return_data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)

        except Exception as e:
            logger.exception('Error querying document')
            return_data = {
                settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: [str(e)]
            }

            return get_response_schema(return_data, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)


class FileSearchStoreListView(ListAPIView):
    permission_classes = [IsUser]
    serializer_class = FileSearchStoreSerializer

    def get_queryset(self):
        return FileSearchStore.objects.filter(user=self.request.user).order_by('-created')


class FileSearchStoreDetailView(RetrieveAPIView):
    permission_classes = [IsUser]
    serializer_class = FileSearchStoreSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return FileSearchStore.objects.filter(user=self.request.user)