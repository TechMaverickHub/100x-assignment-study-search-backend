from django.urls import path

from app.ingestion.views import TestAPIView

urlpatterns = [
    # Authentication
    path('test/', TestAPIView.as_view(), name='test-api')

]
