from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class EmployeeReportViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="List all employee reports",
        operation_description="Get a list of all employee reports",
        responses={200: "Employee report list"},
        tags=["Employee Report Requests"]
    )
    def list(self, request):
        return Response({"employee_reports": []}, status=status.HTTP_200_OK)