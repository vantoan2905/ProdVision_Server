
from django.urls import path
from provision.views.task_report_views import (
    TaskReportView,
    EmployeeReportView
)
"""
| Endpoint                      | Method | Mô tả                  | Input                           | Output                                                         |
| ----------------------------- | ------ | ---------------------- | ------------------------------- | -------------------------------------------------------------- |
| `/api/tasks/<id>/report/`     | GET    | Báo cáo tổng hợp task  | Query: `start_date`, `end_date` | JSON: tổng sản phẩm, số lỗi, tổng giờ nhân viên, tổng ngày làm |
| `/api/employees/<id>/report/` | GET    | Báo cáo theo nhân viên | Query: `start_date`, `end_date` | JSON: tổng giờ làm, số task, số defect detected                |
"""

urlpatterns = [
    path('tasks/<int:task_id>/report/', TaskReportView.as_view(), name='task-report'),
    path('employees/<int:employee_id>/report/', EmployeeReportView.as_view(), name='employee-report'),
]
