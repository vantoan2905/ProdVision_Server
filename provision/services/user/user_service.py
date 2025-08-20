from django.shortcuts import get_object_or_404
from provision.models import User
from django.core.exceptions import PermissionDenied

class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieve a user by ID or raise a 404 if not found.
        """
        return get_object_or_404(User, id=user_id)

    @staticmethod
    def check_user_active(user):
        """
        Check if the user account is active.
        """
        return user.is_active

    @staticmethod
    def has_permission(user, camera):
        """
        Check if the user has permission to access a camera.
        """
        # Example: Only admin or the owner of the camera can access
        if user.is_superuser or camera.user_id == user.id:
            return True
        return False

    @staticmethod
    def create_user(username, email, password, **extra_fields):
        """
        Create a new user with provided details.
        """
        if User.objects.filter(username=username).exists():
            raise ValueError("Username already exists")
        user = User.objects.create_user(username=username, email=email, password=password, **extra_fields)
        return user

    @staticmethod
    def update_user(user_id, **kwargs):
        """
        Update user details.
        """
        user = UserService.get_user_by_id(user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return user

    @staticmethod
    def delete_user(user_id):
        """
        Delete a user by ID.
        """
        user = UserService.get_user_by_id(user_id)
        user.delete()
        return True
