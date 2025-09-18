from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class InspectionListView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all inspections",
        responses={200: "Inspection list"},
        tags=["Inspection Requests"]
    )
    def get(self, request):
        return Response({"inspections": []}, status=status.HTTP_200_OK)
    

class InspectionView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all inspections",
        responses={200: "Inspection list"},
        tags=["Inspection Requests"]
    )
    def get(self, request):
        return Response({"inspections": []}, status=status.HTTP_200_OK)

class InspectionCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all inspections",
        responses={200: "Inspection list"},
        tags=["Inspection Requests"]
    )
    def get(self, request):
        return Response({"inspections": []}, status=status.HTTP_200_OK)
    

class InspectionUpdateView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all inspections",
        responses={200: "Inspection list"},
        tags=["Inspection Requests"]
    )
    def get(self, request):
        return Response({"inspections": []}, status=status.HTTP_200_OK)

class InspectionDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all inspections",
        responses={200: "Inspection list"},
        tags=["Inspection Requests"]
    )
    def get(self, request):
        return Response({"inspections": []}, status=status.HTTP_200_OK)

class InspectionDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all inspections",
        responses={200: "Inspection list"},
        tags=["Inspection Requests"]
    )
    def get(self, request):
        return Response({"inspections": []}, status=status.HTTP_200_OK)