from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from drf_yasg.utils import swagger_auto_schema
from .serializers import LoginSerializer,RegisterSerializer , ForgotPasswordSerializer, ResetPasswordSerializer
# gen token for password reset
from django.contrib.auth.tokens import default_token_generator
from .lib.token import send_mail
User = get_user_model()

class RegisterView(APIView):

    @swagger_auto_schema(
        tags=["Authentication"],
        operation_description="Register a new user",
        request_body=RegisterSerializer,
        responses={201: "User registered successfully"},
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        return Response(
            {"message": "User registered successfully", "user": user.username},
            status=201,
        )


class LoginView(APIView):

    @swagger_auto_schema(
        tags=["Authentication"],
        operation_description="Login user (use JWT TokenObtainPairView for real token)",
        request_body = LoginSerializer,
        responses={200: "Login OK", 400: "Invalid credentials"}
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        return Response({"message": "Login successful"})


class ForgotPasswordView(APIView):
# 
    @swagger_auto_schema(
        operation_description="Send email with password reset link",
        request_body=ForgotPasswordSerializer,
        responses={200: "Email sent"}
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
# 
        email = serializer.validated_data["email"]
# 
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Email not found"}, status=400)
# 
        token = default_token_generator.make_token(user)
        reset_url = f"/api/v1/auth/reset/{user.pk}/{token}/"
# 
        send_mail(
            subject="Reset your password",
            message=f"Click link to reset password: {reset_url}",
            from_email="noreply@server.local",
            recipient_list=[email],
        )
# 
        return Response({"message": "Reset link sent to email"}, status=200)
# 


class ResetPasswordView(APIView):

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
