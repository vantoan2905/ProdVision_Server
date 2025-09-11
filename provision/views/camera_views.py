from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from provision.serializers.camera import CameraSerializer, ErrorSerializer


class CameraRequestView(APIView):
    @swagger_auto_schema(
        operation_description="Create a new camera request",
        responses={201: "Camera request created"},
        tags=["Camera Requests"]
    )
    def post(self, request):
        return Response({"message": "Camera request created"}, status=status.HTTP_201_CREATED)


class LoadAllCamerasView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all cameras",
        responses={200: CameraSerializer(many=True)},
        tags=["Camera Requests"]
    )
    def get(self, request):
        return Response({"cameras": []}, status=status.HTTP_200_OK)


class CameraDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get detailed information of a camera",
        responses={200: CameraSerializer()},
        tags=["Camera Requests"]
    )
    def get(self, request, pk):
        return Response({"id": pk, "name": "Production Line Camera"}, status=status.HTTP_200_OK)


class CameraStartView(APIView):
    @swagger_auto_schema(
        operation_description="Start camera stream",
        responses={200: CameraSerializer()},
        tags=["Camera Requests"]
    )
    def post(self, request, pk):
        return Response({"id": pk, "status": "started"}, status=status.HTTP_200_OK)


class CameraStopView(APIView):
    @swagger_auto_schema(
        operation_description="Stop camera stream",
        responses={200: CameraSerializer()},
        tags=["Camera Requests"]
    )
    def post(self, request, pk):
        return Response({"id": pk, "status": "stopped"}, status=status.HTTP_200_OK)


class CameraSnapshotView(APIView):
    @swagger_auto_schema(
        operation_description="Capture a frame from the camera",
        responses={200: CameraSerializer()},
        tags=["Camera Requests"]
    )
    def post(self, request, pk):
        return Response({"id": pk, "snapshot_url": f"/media/cameras/{pk}/snapshot.jpg"}, status=status.HTTP_200_OK)


# ========================
# Error APIs
# ========================

class CameraErrorsView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of errors from the camera",
        responses={200: ErrorSerializer(many=True)},
        tags=["Camera Errors"]
    )
    def get(self, request, pk):
        errors = [
            {"id": 1, "level": "HIGH", "type": "Surface Defect"},
            {"id": 2, "level": "MEDIUM", "type": "Color Variation"},
        ]
        return Response({"camera_id": pk, "errors": errors}, status=status.HTTP_200_OK)


class ErrorDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get error details",
        responses={200: ErrorSerializer()},
        tags=["Camera Errors"]
    )
    def get(self, request, pk):
        return Response({"id": pk, "type": "Surface Defect", "level": "HIGH"}, status=status.HTTP_200_OK)


class ErrorAcknowledgeView(APIView):
    @swagger_auto_schema(
        operation_description="Mark error as acknowledged",
        responses={200: ErrorSerializer()},
        tags=["Camera Errors"]
    )
    def post(self, request, pk):
        return Response({"id": pk, "acknowledged": True}, status=status.HTTP_200_OK)


class CapturedImagesView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of error images from the camera",
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "camera_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "captured_images": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
            }
        )},
        tags=["Camera Errors"]
    )
    def get(self, request, pk):
        return Response({"camera_id": pk, "captured_images": ["/media/errors/1.jpg", "/media/errors/2.jpg"]}, status=status.HTTP_200_OK)


class ErrorStatisticsView(APIView):
    @swagger_auto_schema(
        operation_description="Get error statistics by date",
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            additional_properties=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "HIGH": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "MEDIUM": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "LOW": openapi.Schema(type=openapi.TYPE_INTEGER),
                }
            )
        )},
        tags=["Camera Errors"]
    )
    def get(self, request):
        stats = {
            "2025-08-30": {"HIGH": 5, "MEDIUM": 3, "LOW": 7},
            "2025-08-31": {"HIGH": 2, "MEDIUM": 1, "LOW": 4},
        }
        return Response({"statistics": stats}, status=status.HTTP_200_OK)
    


# ========================
# WebSocket Consumer
# ========================

class CameraWebSocketView(AsyncWebsocketConsumer):
    async def connect(self):
        self.camera_id = self.scope['url_route']['kwargs']['camera_id']
        await self.accept()
        # TODO: Authenticate user if needed
        await self.send(text_data=json.dumps({
            "message": f"Connected to camera {self.camera_id}"
        }))

    async def disconnect(self, close_code):
        # TODO: Cleanup if needed
        """
        Called when the socket is closed. This is the last message we will
        receive from the client, and we should clean up any resources we've
        allocated at this point.
        """
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "start":
            await self.send(text_data=json.dumps({"status": "streaming started"}))
        elif action == "stop":
            await self.send(text_data=json.dumps({"status": "streaming stopped"}))
        else:
            await self.send(text_data=json.dumps({"error": "unknown action"}))
