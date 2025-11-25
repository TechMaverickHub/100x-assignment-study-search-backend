import os
from django.conf import settings

try:
    from google import genai
    from google.genai import types
except Exception:
    genai = None
    types = None


class GeminiClientWrapper:
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY') or getattr(settings, 'GOOGLE_API_KEY', None)
        if not api_key:
            raise RuntimeError('GOOGLE_API_KEY is not set')

        if genai is None:
            raise RuntimeError('google-genai library is not available')

        self.client = genai.Client(api_key=api_key)

    def create_store(self):
        # create a new file search store
        return self.client.file_search_stores.create()

    def upload_file_to_store(self, store_name: str, file_path: str):
        # returns operation object
        return self.client.file_search_stores.upload_to_file_search_store(
            file_search_store_name=store_name,
            file=file_path
        )

    def query_store(self, store_name: str, query: str):
        # Use models.generate_content with file_search tool
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=query,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[store_name]
                        )
                    )
                ]
            )
        )
        return response
