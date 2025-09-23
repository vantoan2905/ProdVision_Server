from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import update_last_login
from provision.serializers.user import (
    RegisterSerializer, UserSerializer, ChangePasswordSerializer,
    ResetPasswordSerializer, ResetPasswordConfirmSerializer,
    SetRoleSerializer, LoginSerializer, RefreshTokenSerializer
)
from provision.utils.mail_manager import MailFormation, MailManager
from provision.utils.token_manager import OTPManager
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    """
    Handles registration, login, logout, password reset & refresh token
    """
    # --------------------------------
    # Register
    # --------------------------------
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary="Register new account",
        request_body=RegisterSerializer,
        tags=["Authentication"]
    )
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # --------------------------------
    # Login
    # --------------------------------
    @swagger_auto_schema(
        operation_summary="Login",
        request_body=LoginSerializer,
        tags=["Authentication"]
    )
    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=400)
        update_last_login(None, user)
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.is_superuser
            },
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })
    # --------------------------------
    # Logout
    # --------------------------------
    @swagger_auto_schema(
        operation_summary="Logout user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"refresh": openapi.Schema(type=openapi.TYPE_STRING)},
            required=["refresh"]
        ),
        tags=["Authentication"]
    )
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data["refresh"]
            print(refresh_token)
            
            token = RefreshToken(refresh_token)

            token.blacklist()
            return Response({"msg": "Logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_summary="Change password",
        request_body=ChangePasswordSerializer,
        tags=["Authentication"],
        methods=["post"]
    )
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "Password updated successfully"})

    
    
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary="Request password reset",
        request_body=ResetPasswordSerializer,
        tags=["Authentication"]
    )
    @action(detail=False, methods=["post"])
    def reset_password_request(self, request):

        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.validated_data["email"])
            code = OTPManager.generate_otp(user.id)
            subject, message, from_email, recipient_list = MailFormation.code_reset_password(user, code)
            # print(subject, message, from_email, recipient_list)
            try:
                MailManager.send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                print(e)
            
        except User.DoesNotExist:
            pass  

        return Response({
            "message": "If an account with that email exists, a reset password email has been sent"
        }, status=200)
    
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary="Confirm password reset",
        request_body=ResetPasswordConfirmSerializer,
        tags=["Authentication"]
    )
    @action(detail=False, methods=["post"])
    def reset_password_confirm(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        user_id = User.objects.get(email=email).id
        if not OTPManager.verify_otp(user_id, otp):
            return Response({"error": "Invalid or expired OTP"}, status=400)

        new_password = serializer.validated_data["new_password"]
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        user.set_password(new_password)
        user.save()
        return Response({"msg": "Password has been reset"})


class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin):
    """
    Handles user profile, permissions, deactivate account (user & admin)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["list", "set_role"]:
            permission_classes = [IsAdminUser]
        elif self.action in ["permissions", "deactivate"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [p() for p in permission_classes]

    @swagger_auto_schema(operation_summary="Get user profile", tags=["User"])
    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="Partial update user profile", tags=["User"])
    @action(detail=False, methods=["patch"])
    def update_me(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="Deactivate user account", tags=["User"])
    @action(detail=False, methods=["post"])
    def deactivate(self, request):
        request.user.is_active = False
        request.user.save()
        return Response({"msg": "Account deactivated"}, status=204)

    @swagger_auto_schema(operation_summary="Get user permissions", tags=["User"])
    @action(detail=False, methods=["get"])
    def permissions(self, request):
        return Response({"permissions": list(request.user.get_all_permissions())})

    @swagger_auto_schema(operation_summary="Assign role to user", request_body=SetRoleSerializer, tags=["Admin"])
    @action(detail=True, methods=["post"])
    def set_role(self, request, pk=None):
        serializer = SetRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO: update user role
        return Response({"msg": f"Role assigned to user {pk}"})
