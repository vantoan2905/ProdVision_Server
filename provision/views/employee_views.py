from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class EmployeeView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all employees",
        responses={200: "Employee list"},
        tags=["Employee Requests"]
    )
    def get(self, request):
        return Response({"employees": []}, status=status.HTTP_200_OK)
    

class EmployeeCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Create a new employee",
        responses={201: "Employee created"},
        tags=["Employee Requests"]
    )
    def post(self, request):
        return Response({"message": "Employee created"}, status=status.HTTP_201_CREATED)
    
class EmployeeListView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all employees",
        responses={200: "Employee list"},
        tags=["Employee Requests"]
    )
    def get(self, request):
        return Response({"employees": []}, status=status.HTTP_200_OK)
    

class EmployeeDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get detailed information of an employee",
        responses={200: "Employee details"},
        tags=["Employee Requests"]
    )
    def get(self, request, pk):
        return Response({"id": pk, "name": "Production Line Employee"}, status=status.HTTP_200_OK)
    

class EmployeeUpdateView(APIView):
    @swagger_auto_schema(
        operation_description="Update an employee",
        responses={200: "Employee updated"},
        tags=["Employee Requests"]
    )
    def put(self, request, pk):
        return Response({"message": "Employee updated"}, status=status.HTTP_200_OK)
    

class EmployeeDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Delete an employee",
        responses={200: "Employee deleted"},
        tags=["Employee Requests"]
    )
    def delete(self, request, pk):
        return Response({"message": "Employee deleted"}, status=status.HTTP_200_OK)