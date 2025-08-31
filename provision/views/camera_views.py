from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from channels.generic.websocket import AsyncWebsocketConsumer

import cv2
import base64
import asyncio

from provision.serializers.respon.camera_respon_forms import CameraResponseFrom
from provision.serializers.request.camera_request_froms import (
    CameraRequestFrom, LoadAllCamerasRequestFrom,
    UpdateCameraRequestFrom, CreateCameraRequestFrom
)
from provision.services.camera.camera_service import CameraService


# ===============================
# CAMERA API VIEWS
# ===============================

class CameraRequestView(APIView):
    """API for getting a specific camera by ID"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a specific camera by ID",
        query_serializer=CameraRequestFrom,
        responses={200: CameraResponseFrom}
    )
    def get(self, request):
        serializer = CameraRequestFrom(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        camera_id = serializer.validated_data["camera_id"]

        camera = CameraService.get_camera_by_id(camera_id)
        response_serializer = CameraResponseFrom(camera)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class CreateCameraView(APIView):
    """API for creating a new camera"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new camera",
        request_body=CreateCameraRequestFrom,
        responses={201: CameraResponseFrom}
    )
    def post(self, request):
        serializer = CreateCameraRequestFrom(data=request.data)
        serializer.is_valid(raise_exception=True)

        camera_name = serializer.validated_data["camera_name"]
        camera_key = serializer.validated_data["camera_key"]
        camera_info = serializer.validated_data["camera_info"]

        camera = CameraService.add_new_camera(
            request.user.id, camera_name, camera_key, camera_info
        )
        response_serializer = CameraResponseFrom(camera)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class UpdateCameraView(APIView):
    """API for updating an existing camera"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update a camera",
        request_body=UpdateCameraRequestFrom,
        responses={200: CameraResponseFrom}
    )
    def post(self, request):
        serializer = UpdateCameraRequestFrom(data=request.data)
        serializer.is_valid(raise_exception=True)

        camera_id = serializer.validated_data["camera_id"]
        camera_name = serializer.validated_data["camera_name"]
        camera_key = serializer.validated_data["camera_key"]
        camera_info = serializer.validated_data["camera_info"]

        camera = CameraService.update_camera(camera_id, camera_name, camera_key, camera_info)
        response_serializer = CameraResponseFrom(camera)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class LoadAllCamerasView(APIView):
    """API for loading all cameras of the authenticated user"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all cameras for the authenticated user",
        responses={200: CameraResponseFrom(many=True)}
    )
    def get(self, request, version=None, *args, **kwargs):
        user = request.user
        list_cameras = CameraService.get_all_cameras(user.id)

        if not list_cameras:
            return Response(
                {"message": "User has no cameras"},
                status=status.HTTP_404_NOT_FOUND
            )

        response_serializer = CameraResponseFrom(list_cameras, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


# ===============================
# CAMERA WEBSOCKET VIEW
# ===============================

class CameraWebSocketView(AsyncWebsocketConsumer):
    """WebSocket for streaming video frames from a camera"""
    permission_classes = [IsAuthenticated]

    async def connect(self):
        self.camera_id = self.scope["url_route"]["kwargs"]["camera_id"]
        await self.accept()
        self.stream_task = asyncio.create_task(self.stream_video())

    async def disconnect(self, close_code):
        if hasattr(self, "stream_task"):
            self.stream_task.cancel()

    async def receive(self, text_data=None, bytes_data=None):
        # You can handle incoming messages if needed
        pass

    async def stream_video(self):
        """Stream video frames from OpenCV to WebSocket"""
        video_path = f"media/videos/{self.camera_id}.mp4"
        cap = cv2.VideoCapture(video_path)

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.resize(frame, (640, 480))

                _, buffer = cv2.imencode(".jpg", frame)
                frame_bytes = buffer.tobytes()
                frame_b64 = base64.b64encode(frame_bytes).decode("utf-8")

                await self.send(text_data=frame_b64)
                await asyncio.sleep(0.03)  # ~30 FPS
        finally:
            cap.release()
