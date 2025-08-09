# provision/views/camera_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from provision.serializers.camera_serializers import CameraRequest
from drf_yasg.utils import swagger_auto_schema
class CameraManagerView(APIView):
    @swagger_auto_schema(request_body=CameraRequest, responses={200: "OK"})
    def post(self, request):
        serializer = CameraRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO: data processing
        return Response({"message": "Camera data accepted"}, status=status.HTTP_200_OK)
    def load_pretrained_model(self):
        # TODO: load pretrained model
        pass
    def detect_object(self):
        # TODO: detect object
        pass

