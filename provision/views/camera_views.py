# provision/views/camera_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from provision.serializers.camera_serializers import CameraRequest
from drf_yasg.utils import swagger_auto_schema
from provision.models import Camera
from provision.models import User



class CameraManagerView(APIView):
    @swagger_auto_schema(request_body=CameraRequest, responses={200: "OK"})
    def load_all_camera(self, request):
        serializer = CameraRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data['id_user_id']

        # TODO: data processing
        return Response({"message": "Camera data accepted"}, status=status.HTTP_200_OK)
    def request_camera(self, request):
        serializer = CameraRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data['id_user_id']
        camera_id = serializer.validated_data['id_camera']

        # TODO: get camera info from database
        

        # TODO: check camera status


        # TODO: check camera connection


        # TODO: check camera permission


        # TODO: connect camera

        
        # TODO: detect object

        # TODO: return object

        # TODO: return video
        
        pass



    def load_pretrained_model(self):
        # TODO: load pretrained model
        pass
    def detect_object(self):
        # TODO: detect object
        pass

