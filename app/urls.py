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

# ======================================
# 🔹 Swagger & API Documentation
# ======================================
schema_view = get_schema_view(
    openapi.Info(
        title="ProdVision API",
        default_version="v1",
        description="Swagger UI for Django APIs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@prodvision.local"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


def home(request):
    return HttpResponse("✅ Welcome to ProdVision Server")

# ======================================
# 🔹 URL Patterns
# ======================================
urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),

    # --- App routes (chưa có file urls.py nên comment lại) ---
    # path("api/v1/employee/", include("app.employee.urls")),  # ⚙️ uncomment khi có file app/employee/urls.py
    # path("api/v1/task/", include("app.task.urls")),          # ⚙️ uncomment khi có file app/task/urls.py
    # path("api/v1/product/", include("app.product.urls")),    # ⚙️ uncomment khi có file app/product/urls.py
    # path("api/v1/chatbot/", include("app.chatbot.urls")),    # ⚙️ uncomment khi có file app/chatbot/urls.py
    # path("api/v1/model/", include("app.model.urls")),        # ⚙️ uncomment khi có file app/model/urls.py
    
    # --- JWT Auth ---
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # --- Swagger / Redoc ---
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]

# ======================================
# 🔹 Static & Media (for DEBUG mode)
# ======================================
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
