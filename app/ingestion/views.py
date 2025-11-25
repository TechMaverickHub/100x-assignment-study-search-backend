from rest_framework import status
from rest_framework.generics import GenericAPIView

from app.global_constants import SuccessMessage
from app.utils import get_response_schema


# Create your views here.
class TestAPIView(GenericAPIView):

    def post(self, request):
        return get_response_schema({"message": "Hello world"}, SuccessMessage.RECORD_RETRIEVED.value,
                                   status.HTTP_200_OK)
