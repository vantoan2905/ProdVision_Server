
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from provision.views.task_report_views import TaskReportViewSet

router = DefaultRouter()
router.register(r'task_reports', TaskReportViewSet, basename='task_report')

urlpatterns = [
    path('', include(router.urls)),
]
