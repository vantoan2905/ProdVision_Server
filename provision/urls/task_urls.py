from django.urls import path
from provision.views.task_views import (
    
    TaskListView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView
)

base_urls = 'task_management'
"""
| Endpoint           | Method    | Mô tả                     | Input                                                                                          | Output                                         |
| ------------------ | --------- | ------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| `/api/tasks/`      | GET       | Lấy danh sách tất cả task | Query params: `has_employee`, `start_date`, `end_date`                                         | List of tasks                                  |
| `/api/tasks/`      | POST      | Tạo task mới              | JSON: `{name, start_date, end_date, has_employee, product_ids[], model_ids[], employee_ids[]}` | Task object created                            |
| `/api/tasks/<id>/` | GET       | Lấy chi tiết task         | -                                                                                              | Task object, kèm list product, model, employee |
| `/api/tasks/<id>/` | PUT/PATCH | Cập nhật task             | JSON: fields cần update                                                                        | Task object updated                            |
| `/api/tasks/<id>/` | DELETE    | Xóa task                  | -                                                                                              | Status 204                                     |

"""
urlpatterns = [

path(f"{base_urls}/", TaskListView.as_view(), name="task_list"),
path(f"{base_urls}/", TaskCreateView.as_view(), name="task_create"),
path(f"{base_urls}/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
path(f"{base_urls}/<int:pk>/", TaskUpdateView.as_view(), name="task_update"),
path(f"{base_urls}/<int:pk>/", TaskDeleteView.as_view(), name="task_delete"),




]