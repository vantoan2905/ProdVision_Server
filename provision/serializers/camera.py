from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class CameraSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    status = serializers.CharField(required=False)
    snapshot_url = serializers.CharField(required=False)


class ErrorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField()
    level = serializers.CharField()
    position = serializers.ListField(child=serializers.IntegerField(), required=False)
    acknowledged = serializers.BooleanField(required=False)