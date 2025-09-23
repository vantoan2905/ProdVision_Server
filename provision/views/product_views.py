# provision/views/product_views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class ProductViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="List all products",
        operation_description="Get a list of all products",
        responses={200: "Product list"},
        tags=["Product Requests"]
    )
    def list(self, request):
        return Response({"products": []}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new product",
        operation_description="Create a new product",
        responses={201: "Product created"},
        tags=["Product Requests"]
    )
    def create(self, request):
        return Response({"message": "Product created"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Retrieve product details",
        operation_description="Get detailed information of a product",
        responses={200: "Product details"},
        tags=["Product Requests"]
    )
    def retrieve(self, request, pk=None):
        return Response({"id": pk, "name": "Production Line Product"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a product",
        operation_description="Update a product",
        responses={200: "Product updated"},
        tags=["Product Requests"]
    )
    def update(self, request, pk=None):
        return Response({"message": "Product updated"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Delete a product",
        operation_description="Delete a product",
        responses={200: "Product deleted"},
        tags=["Product Requests"]
    )
    def destroy(self, request, pk=None):
        return Response({"message": "Product deleted"}, status=status.HTTP_200_OK)
