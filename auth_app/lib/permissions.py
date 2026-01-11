from rest_framework.permissions import BasePermission

class JWTOptional(BasePermission):
    def has_permission(self, request, view):
        
        if getattr(view, "require_auth", True) is False:
            return True

        
        return request.user and request.user.is_authenticated
