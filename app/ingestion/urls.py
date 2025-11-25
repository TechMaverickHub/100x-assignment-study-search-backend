from django.urls import path

from app.ingestion.views import TestAPIView, CreateFileSearchStoreView, DocumentUploadView, QueryDocumentView, \
    FileSearchStoreListView, FileSearchStoreDetailView

urlpatterns = [
    # Document ingestion endpoints
    path('test/', TestAPIView.as_view(), name='document-upload'),
    path('api/filesearch/stores/', CreateFileSearchStoreView.as_view(), name='filesearch-create-store'),
    path('api/filesearch/upload/', DocumentUploadView.as_view(), name='filesearch-upload'),
    path('api/filesearch/query/', QueryDocumentView.as_view(), name='filesearch-query'),
    path('api/filesearch/stores/list/', FileSearchStoreListView.as_view(), name='filesearch-list'),
    path('api/filesearch/stores/<int:id>/', FileSearchStoreDetailView.as_view(), name='filesearch-detail'),
]

