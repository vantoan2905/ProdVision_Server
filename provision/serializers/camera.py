from rest_framework import status, serializers
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