from django.urls import path
from provision.views.model_views import (
    ModelManagerViews,
    HealthModelCheckView,
    TrainModelView,
    EvaluateModelView,
    SaveModelView,
    SaveResultsView
)

urlpatterns = [
    path('health_check/', ModelManagerViews.as_view(), name='health_check'),
    path('health_model_check/', HealthModelCheckView.as_view(), name='health_model_check'),
    path('train_model/', TrainModelView.as_view(), name='train_model'),
    path('evaluate_model/', EvaluateModelView.as_view(), name='evaluate_model'),
    path('save_model/', SaveModelView.as_view(), name='save_model'),
    path('save_results/', SaveResultsView.as_view(), name='save_results'),
]
