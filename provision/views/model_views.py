# provision/views/model_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from provision.serializers.model_serializers import ModelRequest
from drf_yasg.utils import swagger_auto_schema



class ModelManagerViews(APIView):
    def health_check(self, request):
        return Response({"message": "OK"}, status=status.HTTP_200_OK)
    def health_model_check(self, request):
        # TODO: health check model
        pass
    def train_model(self, request):
        # TODO: train model
        pass
    def evaluate_model(self, request):
        # TODO: evaluate model
        pass
    def save_model(self, request):
        # TODO: save model
        pass
    def save_results(self, request):
        # TODO: save results
        pass
    
