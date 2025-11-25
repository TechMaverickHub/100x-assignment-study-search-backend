from rest_framework import serializers

from app.filesearch.models import FileSearchStore


class FileSearchStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileSearchStore
        fields = ['id', 'user', 'title', 'file', 'store_name', 'status', 'error_message', 'created', 'updated']
        read_only_fields = ['id', 'user', 'store_name', 'status', 'error_message', 'created', 'updated']


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    title = serializers.CharField(required=False, allow_blank=True)


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()
    document_id = serializers.IntegerField()


class FileStoreCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileSearchStore
        fields = ['title', 'file', 'user', 'status']
