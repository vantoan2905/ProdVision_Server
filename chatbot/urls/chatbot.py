from django.urls import path

from . import views

urlpatterns = [
    path("", views.ChatbotListCreateView.as_view(), name="chatbot-list-create"),
    path("<int:pk>/", views.ChatbotRetrieveUpdateDestroyView.as_view(), name="chatbot-retrieve-update-destroy"),
    
]