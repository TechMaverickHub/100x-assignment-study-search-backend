from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class FileSearchStore(models.Model):

    class StoreStatus(models.TextChoices):
        CREATED = 'CREATED', 'Created'
        UPLOADING = 'UPLOADING', 'Uploading'
        PROCESSING = 'PROCESSING', 'Processing'
        READY = 'READY', 'Ready'
        FAILED = 'FAILED', 'Failed'


    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='file_search_stores')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/filesearch/')
    store_name = models.CharField(max_length=512, blank=True, null=True)
    status = models.CharField(max_length=32, choices=StoreStatus.choices, default=StoreStatus.CREATED)

    error_message = models.TextField(blank=True, null=True)


    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


