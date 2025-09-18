from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class TaskReportView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all task reports",
        responses={200: "Task report list"},
        tags=["Task Reports"]
    )
    def get(self, request):
        return Response({"task_reports": []}, status=status.HTTP_200_OK)
    
class EmployeeReportView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all employee reports",
        responses={200: "Employee report list"},
        tags=["Employee Reports"]
    )
    def get(self, request):
        return Response({"employee_reports": []}, status=status.HTTP_200_OK)