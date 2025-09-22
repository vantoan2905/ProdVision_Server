from django.urls import path

from provision.views.inspection_views import (
    InspectionListView,
    InspectionCreateView,
    InspectionDetailView,
    InspectionUpdateView,
    InspectionDeleteView
)

base_urls = "inspection"

"""
| Endpoint                 | Method    | Mô tả                    | Input                                                                                                                                                    | Output                    |
| ------------------------ | --------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| `/api/inspections/`      | GET       | Lấy danh sách inspection | Query: task\_id, product\_id, defect\_detected                                                                                                           | List of inspections       |
| `/api/inspections/`      | POST      | Tạo inspection           | JSON: `{task_id, product_id, employee_id?, camera_id, model_id, view_id, defect_detected, defect_type_id, confidence, image_path, start_time, end_time}` | Inspection object         |
| `/api/inspections/<id>/` | GET       | Chi tiết inspection      | -                                                                                                                                                        | Inspection object         |
| `/api/inspections/<id>/` | PUT/PATCH | Cập nhật inspection      | JSON: fields cần update                                                                                                                                  | Inspection object updated |
| `/api/inspections/<id>/` | DELETE    | Xóa inspection           | -                                                                                                                                                        | Status 204                |


"""


urlpatterns = [
    path(f"{base_urls}/", InspectionListView.as_view(), name="inspection_list"),
    path(f"{base_urls}/", InspectionCreateView.as_view(), name="inspection_create"),
    path(f"{base_urls}/<int:pk>/", InspectionDetailView.as_view(), name="inspection_detail"),
    path(f"{base_urls}/<int:pk>/", InspectionUpdateView.as_view(), name="inspection_update"),
    path(f"{base_urls}/<int:pk>/", InspectionDeleteView.as_view(), name="inspection_delete"),
]