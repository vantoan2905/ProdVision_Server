
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

    # 🔹 Các API với version cố định 'v1'
    path("api/v1/user/", include("provision.urls.user_urls")),
    path("api/v1/camera/", include("provision.urls.camera_urls")),
    path("api/v1/model/", include("provision.urls.model_urls")),
    path("api/v1/task/", include("provision.urls.task_urls")),
    path("api/v1/inspection/", include("provision.urls.inspection_urls")),
    path("api/v1/product/", include("provision.urls.products_urls")),
    path("api/v1/employee/", include("provision.urls.employees_urls")),
    path("api/v1/task_report/", include("provision.urls.task_report_urls")),
    path("api/v1/employee_report/", include("provision.urls.employee_report_urls")),

    # 🔑 JWT endpoints 
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # 🔹 Swagger / Redoc
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]

# 🔹 Static / Media
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
