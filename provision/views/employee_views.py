from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

class EmployeeViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="List all employees",
        operation_description="Get a list of all employees",
        responses={200: "Employee list"},
        tags=["Employee Requests"]
    )
    def list(self, request):
        return Response({"employees": []}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new employee",
        operation_description="Create a new employee",
        responses={201: "Employee created"},
        tags=["Employee Requests"]
    )
    def create(self, request):
        return Response({"message": "Employee created"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Retrieve employee details",
        operation_description="Get detailed information of an employee",
        responses={200: "Employee details"},
        tags=["Employee Requests"]
    )
    def retrieve(self, request, pk=None):
        return Response({"id": pk, "name": "Production Line Employee"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update an employee",
        operation_description="Update an employee",
        responses={200: "Employee updated"},
        tags=["Employee Requests"]
    )
    def update(self, request, pk=None):
        return Response({"message": "Employee updated"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Delete an employee",
        operation_description="Delete an employee",
        responses={200: "Employee deleted"},
        tags=["Employee Requests"]
    )
    def destroy(self, request, pk=None):
        return Response({"message": "Employee deleted"}, status=status.HTTP_200_OK)
