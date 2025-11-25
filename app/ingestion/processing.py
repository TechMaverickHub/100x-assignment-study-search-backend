from django.shortcuts import get_object_or_404

from app.ingestion.gemini_client import GeminiClientWrapper
from app.ingestion.models import FileSearchStore


def process_file_search_store(store_id):
    """Synchronous processing: create Gemini store + upload file."""

    store = get_object_or_404(FileSearchStore, id=store_id)

    print("Inside process file search")

    try:
        store.status = FileSearchStore.StoreStatus.UPLOADING
        store.save()

        client = GeminiClientWrapper()
        created_store = client.create_store()
        store.store_name = created_store.name
        store.status = FileSearchStore.StoreStatus.PROCESSING
        store.save()

        local_path = store.file.path
        upload_op = client.upload_file_to_store(created_store.name, local_path)

        # Poll until finished
        max_wait = 300
        waited = 0
        while not upload_op.done:
            if waited >= max_wait:
                raise RuntimeError('Upload timeout')
            import time
            time.sleep(3)
            waited += 3
            upload_op = client.client.operations.get(upload_op)

        store.status = FileSearchStore.StoreStatus.READY
        store.save()

    except Exception as exc:
        store.status = FileSearchStore.StoreStatus.FAILED
        store.error_message = str(exc)
        store.save()
        raise