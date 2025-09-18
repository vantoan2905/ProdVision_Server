
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class ProductListView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all products",
        responses={200: "Product list"},
        tags=["Product Requests"]
    )
    def get(self, request):
        return Response({"products": []}, status=status.HTTP_200_OK)


class ProductCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Create a new product",
        responses={201: "Product created"},
        tags=["Product Requests"]
    )
    def post(self, request):
        return Response({"message": "Product created"}, status=status.HTTP_201_CREATED)

class ProductDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get detailed information of a product",
        responses={200: "Product details"},
        tags=["Product Requests"]
    )
    def get(self, request, pk):
        return Response({"id": pk, "name": "Production Line Product"}, status=status.HTTP_200_OK)
    

class ProductUpdateView(APIView):
    @swagger_auto_schema(
        operation_description="Update a product",
        responses={200: "Product updated"},
        tags=["Product Requests"]
    )
    def put(self, request, pk):
        return Response({"message": "Product updated"}, status=status.HTTP_200_OK)
    

class ProductDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Delete a product",
        responses={200: "Product deleted"},
        tags=["Product Requests"]
    )
    def delete(self, request, pk):
        return Response({"message": "Product deleted"}, status=status.HTTP_200_OK)