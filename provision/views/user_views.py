from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from provision.serializers.user import (
    RegisterSerializer, UserSerializer, ChangePasswordSerializer,
    ResetPasswordSerializer, ResetPasswordConfirmSerializer,
    SetRoleSerializer
)

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from provision.utils.mail_manager import MailFormation, MailManager
from provision.utils.token_manager import OTPManager
# 1. Register a new user
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Register new account",
        operation_description="Create a new user account",
        tags=["Authentication"],
        request_body=RegisterSerializer
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# 2. Logout (invalidate token)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Logout user",
        tags=["Authentication"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"refresh": openapi.Schema(type=openapi.TYPE_STRING)},
            required=["refresh"]
        ),
        responses={200: "Successfully logged out"}
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"msg": "Logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


# 3. User profile (get, update, deactivate)
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Get user profile",
                          tags=["User"],
                          responses={200: UserSerializer()})
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="Update user profile", tags=["User"])
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(operation_summary="Partial update user profile", tags=["User"])
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(operation_summary="Deactivate user account", tags=["User"])
    def delete(self, request):
        request.user.is_active = False
        request.user.save()
        return Response({"msg": "Account deactivated"}, status=204)


# 4. Change password
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Change password",
        tags=["Authentication"],
        request_body=ChangePasswordSerializer
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "Password updated successfully"})


# 5. Reset password request + confirm

class ResetPasswordRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Request password reset",
        tags=["Authentication"],
        request_body=ResetPasswordSerializer
    )
    def post(self, request, *args, **kwargs):
        version = kwargs.get("version")
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print("email", serializer.validated_data["email"])
        user = User.objects.get(email=serializer.validated_data["email"])
        code = OTPManager.generate_otp()
        subject, message, from_email, recipient_list = MailFormation.code_reset_password(
            user, code
        )
        MailManager.send_mail(subject, message, from_email, recipient_list)

        return Response(
            {
                "message": "Reset password email sent successfully",
                "version": version,
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )

class ResetPasswordConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Confirm password reset",
        tags=["Authentication"],
        request_body=ResetPasswordConfirmSerializer
    )
    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]
        if not OTPManager.verify_otp(token, serializer.validated_data["otp"]):
            return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
        new_password = serializer.validated_data["new_password"]
        user = User.objects.get(id=token)  # Giả sử token là user_id
        user.set_password(new_password)
        user.save()
        OTPManager.otp_store.pop(token, None)  
        return Response({"msg": "Password has been reset"})


# 6. Email & OTP verification
class VerifyEmailView(APIView):
    @swagger_auto_schema(operation_summary="Verify email", tags=["Security"])
    def post(self, request):
        # TODO: implement email verification
        return Response({"msg": "Email verification not implemented"})


class ResendVerificationView(APIView):
    @swagger_auto_schema(operation_summary="Resend verification email", tags=["Security"])
    def post(self, request):
        # TODO: implement resend verification
        return Response({"msg": "Resend verification not implemented"})


class VerifyOTPView(APIView):
    @swagger_auto_schema(operation_summary="Verify OTP", tags=["Security"])
    def post(self, request):
        # TODO: implement OTP verification
        return Response({"msg": "OTP verification not implemented"})


# 7. Admin: list users, user details, set roles
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(operation_summary="List all users", tags=["Admin"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(operation_summary="Retrieve user detail", tags=["Admin"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SetRoleView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Assign role to user",
        tags=["Admin"],
        request_body=SetRoleSerializer
    )
    def post(self, request, pk):
        serializer = SetRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO: update user role
        return Response({"msg": f"Role assigned to user {pk}"})


class UserPermissionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Get user permissions", tags=["User"])
    def get(self, request):
        return Response({"permissions": list(request.user.get_all_permissions())})


# 8. Social login, 2FA, deactivate account
class SocialLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(operation_summary="Social login", tags=["Social"])
    def post(self, request):
        # TODO: implement social login
        return Response({"msg": "Social login not implemented"})


class TwoFactorAuthView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Enable/verify 2FA", tags=["Security"])
    def post(self, request):
        # TODO: implement 2FA
        return Response({"msg": "2FA not implemented"})


class DeactivateAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Deactivate account", tags=["User"])
    def post(self, request):
        # TODO: implement account deactivation
        return Response({"msg": "Account deactivation not implemented"})
