from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
# 🔑 JWT Views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version="v1",
        description="Swagger UI for your Django APIs",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
def home(request):
    return HttpResponse("Welcome to provision project")

urlpatterns = [
    path("", home),  # 👈 Trang chủ
    path("admin/", admin.site.urls),
    path("api/<version>/user/", include("provision.urls.user_urls")),
    path("api/<version>/camera/", include("provision.urls.camera_urls")),
    path("api/<version>/model/", include("provision.urls.model_urls")),
    path("api/<version>/task/", include("provision.urls.task_urls")),
    path("api/<version>/inspection/", include("provision.urls.inspection_urls")),
    path("api/<version>/product/", include("provision.urls.products_urls")),
    path("api/<version>/employee/", include("provision.urls.employees_urls")),
    path("api/<version>/task_report/", include("provision.urls.task_report_urls")),
    # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("accounts/", include("allauth.urls")),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("chatbot/", include("provision.urls.chatbot_urls")),

    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
