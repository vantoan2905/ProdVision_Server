from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class TaskViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="List all tasks",
        operation_description="Get a list of all tasks",
        responses={200: "Task list"},
        tags=["Task Requests"]
    )
    def list(self, request):
        return Response({"tasks": []}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new task",
        operation_description="Create a new task",
        responses={201: "Task created"},
        tags=["Task Requests"]
    )
    def create(self, request):
        return Response({"message": "Task created"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Retrieve task details",
        operation_description="Get detailed information of a task",
        responses={200: "Task details"},
        tags=["Task Requests"]
    )
    def retrieve(self, request, pk=None):
        return Response({"id": pk, "name": "Production Line Task"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a task",
        operation_description="Update a task",
        responses={200: "Task updated"},
        tags=["Task Requests"]
    )
    def update(self, request, pk=None):
        return Response({"message": "Task updated"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Delete a task",
        operation_description="Delete a task",
        responses={200: "Task deleted"},
        tags=["Task Requests"]
    )
    def destroy(self, request, pk=None):
        return Response({"message": "Task deleted"}, status=status.HTTP_200_OK)
