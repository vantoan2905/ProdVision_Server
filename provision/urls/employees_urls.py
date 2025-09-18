
from django.urls import path
from provision.views.employee_views import (
    EmployeeListView, 
    EmployeeCreateView, 
    EmployeeDetailView, 
    EmployeeUpdateView, 
    EmployeeDeleteView

)


base_urls = "employees"
"""
| Endpoint               | Method    | Mô tả                   | Input                               | Output                  |
| ---------------------- | --------- | ----------------------- | ----------------------------------- | ----------------------- |
| `/api/employees/`      | GET       | Lấy danh sách nhân viên | -                                   | List of employees       |
| `/api/employees/`      | POST      | Thêm nhân viên mới      | JSON: `{name, employee_code, role}` | Employee object created |
| `/api/employees/<id>/` | GET       | Xem chi tiết            | -                                   | Employee object         |
| `/api/employees/<id>/` | PUT/PATCH | Cập nhật thông tin      | JSON: fields cần update             | Employee object updated |
| `/api/employees/<id>/` | DELETE    | Xóa nhân viên           | -                                   | Status 204              |

"""
urlpatterns = [
    path(f"{base_urls}/", EmployeeListView.as_view(), name="employee_list"),
    path(f"{base_urls}/", EmployeeCreateView.as_view(), name="employee_create"),
    path(f"{base_urls}/<int:pk>/", EmployeeDetailView.as_view(), name="employee_detail"),
    path(f"{base_urls}/<int:pk>/", EmployeeUpdateView.as_view(), name="employee_update"),
    path(f"{base_urls}/<int:pk>/", EmployeeDeleteView.as_view(), name="employee_delete"),
]
