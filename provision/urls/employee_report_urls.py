from django.urls import path, include
from rest_framework.routers import DefaultRouter
from provision.views.employee_report_views import EmployeeReportViewSet

router = DefaultRouter()
router.register(r'employee_reports', EmployeeReportViewSet, basename='employee_report')

urlpatterns = [
    path('', include(router.urls)),
]