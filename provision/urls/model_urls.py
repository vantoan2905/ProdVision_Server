from django.urls import path
from provision.views.model_views import load_pretrained_model

urlpatterns = [
    path('load_pretrained_model/', load_pretrained_model, name='load_pretrained_model'),
    path('train_model/', load_pretrained_model, name='train_model'),
    path('evaluate_model/', load_pretrained_model, name='evaluate_model'),
    path('save_model/', load_pretrained_model, name='save_model'),
    path('save_results/', load_pretrained_model, name='save_results'),
]
