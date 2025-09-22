from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from provision.models import Camera, CameraInfo


class ModelSevice:

    @staticmethod
    def get_model_by_id(model_id):
        return get_object_or_404(CameraInfo, id=model_id)
    
    @staticmethod
    def check_model_active(model):
        return model.is_active

    @staticmethod
    def check_model_permission(user, model):
        if user.is_superuser or model.user_id == user.id:
            return True
        return False
    
    @staticmethod
    def delete_model(model_id):
        model = ModelSevice.get_model_by_id(model_id)
        model.delete()
        return True
    
    @staticmethod
    def update_model(model_id, **kwargs):
        model = ModelSevice.get_model_by_id(model_id)
        for key, value in kwargs.items():
            setattr(model, key, value)
        model.save()
        return model
    
    

