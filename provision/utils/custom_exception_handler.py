# provision/utils/custom_exception_handler.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import traceback
from django.conf import settings

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response({
            "error": True,
            "status_code": response.status_code,
            "message": response.data
        }, status=response.status_code)

    if settings.DEBUG:
        return Response({
            "error": True,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(exc),
            "traceback": traceback.format_exc()
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({
            "error": True,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Internal server error"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
