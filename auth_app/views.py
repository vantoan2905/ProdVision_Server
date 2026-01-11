from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from .lib.token import send_mail
from auth_app.lib.permissions import JWTOptional
from auth_app.lib.authenticate_by_email import authenticate_by_email
User = get_user_model()


class RegisterView(APIView):
    require_auth = False 
    permission_classes = [JWTOptional]

    @swagger_auto_schema(
        tags=["Authentication"],
        operation_description="Register a new user",
        request_body=RegisterSerializer,
        responses={201: "User registered successfully"},
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        return Response(
            {
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            },
            status=status.HTTP_201_CREATED,
        )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate_by_email(
            serializer.validated_data["email"],
            serializer.validated_data["password"],
        )

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
            },
            status=200
        )




class ForgotPasswordView(APIView):
    require_auth = False 
    permission_classes = [JWTOptional]

    @swagger_auto_schema(
        operation_description="Send email with password reset link",
        request_body=ForgotPasswordSerializer,
        responses={200: "Email sent"}
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Email not found"}, status=400)
        token = default_token_generator.make_token(user)
        reset_url = f"/api/v1/auth/reset/{user.pk}/{token}/"
        send_mail(
            subject="Reset your password",
            message=f"Click link to reset password: {reset_url}",
            from_email="noreply@server.local",
            recipient_list=[email],
        )
        return Response({"message": "Reset link sent to email"}, status=200)


class ResetPasswordView(APIView):
    require_auth = False 
    permission_classes = [JWTOptional]
    @swagger_auto_schema(
        operation_description="Reset password using token",
        request_body=ResetPasswordSerializer,
    
        responses={200: "Password updated"}
    )
    def post(self, request, user_id, token):
        form = ResetPasswordSerializer(data=request.data)
        if not form.is_valid():
            return Response(form.errors, status=400)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "Invalid user"}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=400)

        user.set_password(form.cleaned_data["password"])
        user.save()

        return Response({"message": "Password reset successful"}, status=200)



class LogoutView(APIView):

    @swagger_auto_schema(
        operation_description="Logout user (invalidate token on frontend)"
    )
    def post(self, request):
        return Response({"message": "Logout successful"})



class UserProfile(APIView):

    
    @swagger_auto_schema(
        operation_description="Get user profile",
        responses={200: "User profile data"}
    )

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        profile_data = {
            "username": user.username,
            "email": user.email,
            # Add other fields as needed
        }
        return Response(profile_data, status=status.HTTP_200_OK)
    
