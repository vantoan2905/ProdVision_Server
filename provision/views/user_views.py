# provision/views/user_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RefreshTokenView(APIView):
    def post(self, request):
        # TODO: refresh token logic
        return Response({"message": "Token refreshed"}, status=status.HTTP_200_OK)
    


