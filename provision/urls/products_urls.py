# provision/urls/product_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from provision.views.product_views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
