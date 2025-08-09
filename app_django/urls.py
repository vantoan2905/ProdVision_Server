# app_django/urls.py

from django.contrib import admin
from django.urls import path, include  # 🔥 Bạn quên dòng này trong phiên bản trước

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="Swagger UI for your Django APIs",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('provision.urls.user_urls')),
    path('api/camera/', include('provision.urls.camera_urls')),
    path('api/model/', include('provision.urls.model_urls')),

    # Swagger & Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
