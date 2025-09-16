# provision/views/model_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class LoadAllModelsView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all models",
        responses={200: "Model list"},
        tags=["Model Requests"]
    )
    def get(self, request):
        return Response({"models": []}, status=status.HTTP_200_OK)


class CreateModelView(APIView):
    @swagger_auto_schema(
        operation_description="Create a new model",
        responses={201: "Model created"},
        tags=["Model Requests"]
    )
    def post(self, request):
        return Response({"message": "Model created"}, status=status.HTTP_201_CREATED)


class HealthCheckView(APIView):
    @swagger_auto_schema(
        operation_description="Health check",
        responses={200: "OK"},
        tags=["Health Check"]
    )
    def get(self, request):
        return Response({"message": "OK"}, status=status.HTTP_200_OK)
class UpdateModelView(APIView):
    @swagger_auto_schema(
        operation_description="Update a model",
        responses={200: "Model updated"},
        tags=["Model Requests"]
    )
    def put(self, request, pk):
        return Response({"message": "Model updated"}, status=status.HTTP_200_OK)
    
class DeleteModelView(APIView):
    @swagger_auto_schema(
        operation_description="Delete a model",
        responses={200: "Model deleted"},
        tags=["Model Requests"]
    )
    def delete(self, request, pk):
        return Response({"message": "Model deleted"}, status=status.HTTP_200_OK)