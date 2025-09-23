from django.urls import path, include
from rest_framework.routers import DefaultRouter
from provision.views.user_views import UserViewSet, AuthViewSet

router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]