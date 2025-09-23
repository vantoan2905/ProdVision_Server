from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from provision.serializers.camera import CameraSerializer, ErrorSerializer

class CameraViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="List all cameras",
        operation_description="Get a list of all cameras",
        responses={200: CameraSerializer(many=True)},
        tags=["Camera Requests"]
    )
    def list(self, request):
        return Response({"cameras": []}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a camera",
        operation_description="Create a new camera",
        responses={201: "Camera created"},
        tags=["Camera Requests"]
    )
    def create(self, request):
        return Response({"message": "Camera created"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Retrieve camera details",
        operation_description="Get detailed information of a camera",
        responses={200: CameraSerializer()},
        tags=["Camera Requests"]
    )
    def retrieve(self, request, pk=None):
        return Response({"id": pk, "name": "Production Line Camera"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Start camera stream",
        operation_description="Start camera streaming",
        responses={200: CameraSerializer()},
        tags=["Camera Requests"]
    )
    def start(self, request, pk=None):
        return Response({"id": pk, "status": "started"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Stop camera stream",
        operation_description="Stop camera streaming",
        responses={200: CameraSerializer()},
        tags=["Camera Requests"]
    )
    def stop(self, request, pk=None):
        return Response({"id": pk, "status": "stopped"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Capture camera snapshot",
        operation_description="Capture a frame from the camera",
        responses={200: CameraSerializer()},
        tags=["Camera Requests"]
    )
    def snapshot(self, request, pk=None):
        return Response({"id": pk, "snapshot_url": f"/media/cameras/{pk}/snapshot.jpg"}, status=status.HTTP_200_OK)


class CameraErrorViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="List camera errors",
        operation_description="Get a list of errors from the camera",
        responses={200: ErrorSerializer(many=True)},
        tags=["Camera Errors"]
    )
    def list(self, request, camera_pk=None):
        errors = [
            {"id": 1, "level": "HIGH", "type": "Surface Defect"},
            {"id": 2, "level": "MEDIUM", "type": "Color Variation"},
        ]
        return Response({"camera_id": camera_pk, "errors": errors}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Retrieve error details",
        operation_description="Get detailed information of a specific error",
        responses={200: ErrorSerializer()},
        tags=["Camera Errors"]
    )
    def retrieve(self, request, pk=None):
        return Response({"id": pk, "type": "Surface Defect", "level": "HIGH"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Acknowledge an error",
        operation_description="Mark error as acknowledged",
        responses={200: ErrorSerializer()},
        tags=["Camera Errors"]
    )
    def acknowledge(self, request, pk=None):
        return Response({"id": pk, "acknowledged": True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="List captured error images",
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
    def captured_images(self, request, camera_pk=None):
        return Response({"camera_id": camera_pk, "captured_images": ["/media/errors/1.jpg", "/media/errors/2.jpg"]}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Get error statistics",
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
    def statistics(self, request):
        stats = {
            "2025-08-30": {"HIGH": 5, "MEDIUM": 3, "LOW": 7},
            "2025-08-31": {"HIGH": 2, "MEDIUM": 1, "LOW": 4},
        }
        return Response({"statistics": stats}, status=status.HTTP_200_OK)
