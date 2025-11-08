from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

class TaskReportViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="List all task reports",
        operation_description="Get a list of all task reports",
        responses={200: "Task report list"},
        tags=["Task Report Requests"]
    )
    def list(self, request):
        return Response({"task_reports": []}, status=status.HTTP_200_OK)
