from django.urls import path, include
from rest_framework.routers import DefaultRouter
from provision.views.model_views import ModelViewSet

router = DefaultRouter()
router.register(r'models', ModelViewSet, basename='model')

urlpatterns = [
    path('', include(router.urls)),
    # path('health/', HealthCheckView.as_view(), name="health_check"),
]
