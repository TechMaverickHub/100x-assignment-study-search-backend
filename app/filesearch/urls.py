from django.urls import path

from app.filesearch.views import TestAPIView, CreateFileSearchStoreView, DocumentUploadView, QueryDocumentView, \
    FileSearchStoreListView, FileSearchStoreDetailView

urlpatterns = [
    # Document ingestion endpoints
    path('test/', TestAPIView.as_view(), name='document-upload'),
    path('stores/', CreateFileSearchStoreView.as_view(), name='filesearch-create-store'),
    path('upload/', DocumentUploadView.as_view(), name='filesearch-upload'),
    path('query/', QueryDocumentView.as_view(), name='filesearch-query'),
    path('stores/list-filter/', FileSearchStoreListView.as_view(), name='filesearch-list'),
    path('stores/<int:pk>/', FileSearchStoreDetailView.as_view(), name='filesearch-detail'),
]

