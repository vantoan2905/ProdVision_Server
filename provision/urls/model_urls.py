from django.urls import path
from provision.views.model_views import (
    LoadAllModelsView,
    HealthCheckView,
    CreateModelView,
    UpdateModelView,
    DeleteModelView
    
)
base_url = 'model_management'
urlpatterns = [
    # CRUD for model
    path(f"{base_url}/load_all_models/", LoadAllModelsView.as_view(), name="load_all_models"),
    path(f"{base_url}/health_check/", HealthCheckView.as_view(), name="health_check"),
    path(f"{base_url}/create/", CreateModelView.as_view(), name="create_model"),
    path(f"{base_url}/update/<int:pk>/", UpdateModelView.as_view(), name="update_model"),
    path(f"{base_url}/delete/<int:pk>/", DeleteModelView.as_view(), name="delete_model"),

]


