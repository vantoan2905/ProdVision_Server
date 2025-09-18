from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema



class TaskView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all tasks",
        responses={200: "Task list"},
        tags=["Task Requests"]
    )
    def get(self, request):
        return Response({"tasks": []}, status=status.HTTP_200_OK)
class  TaskListView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all tasks",
        responses={200: "Task list"},
        tags=["Task Requests"]
    )
    def get(self, request):
        return Response({"tasks": []}, status=status.HTTP_200_OK)
class  TaskCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Create a new task",
        responses={201: "Task created"},
        tags=["Task Requests"]
    )
    def post(self, request):
        return Response({"message": "Task created"}, status=status.HTTP_201_CREATED)


class  TaskDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get detailed information of a task",
        responses={200: "Task details"},
        tags=["Task Requests"]
    )
    def get(self, request, pk):
        return Response({"id": pk, "name": "Production Line Task"}, status=status.HTTP_200_OK)
class  TaskUpdateView(APIView):
    @swagger_auto_schema(
        operation_description="Update a task",
        responses={200: "Task updated"},
        tags=["Task Requests"]
    )
    def put(self, request, pk):
        return Response({"message": "Task updated"}, status=status.HTTP_200_OK)
    

class  TaskDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Delete a task",
        responses={200: "Task deleted"},
        tags=["Task Requests"]
    )
    def delete(self, request, pk):
        return Response({"message": "Task deleted"}, status=status.HTTP_200_OK)