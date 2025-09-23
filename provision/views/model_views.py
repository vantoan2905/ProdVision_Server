from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

class ModelViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="List all models",
        operation_description="Get a list of all models",
        responses={200: "Model list"},
        tags=["Model Requests"]
    )
    def list(self, request):
        return Response({"models": []}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new model",
        operation_description="Create a new model",
        responses={201: "Model created"},
        tags=["Model Requests"]
    )
    def create(self, request):
        return Response({"message": "Model created"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Retrieve model details",
        operation_description="Get model details",
        responses={200: "Model details"},
        tags=["Model Requests"]
    )
    def retrieve(self, request, pk=None):
        return Response({"id": pk, "name": "Demo Model"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a model",
        operation_description="Update a model",
        responses={200: "Model updated"},
        tags=["Model Requests"]
    )
    def update(self, request, pk=None):
        return Response({"message": "Model updated"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Delete a model",
        operation_description="Delete a model",
        responses={200: "Model deleted"},
        tags=["Model Requests"]
    )
    def destroy(self, request, pk=None):
        return Response({"message": "Model deleted"}, status=status.HTTP_200_OK)
