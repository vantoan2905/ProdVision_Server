from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from provision.views.user_views import (
    RegisterView, LogoutView, MeView, ChangePasswordView,
    ResetPasswordRequestView, ResetPasswordConfirmView,
    VerifyEmailView, ResendVerificationView,
    VerifyOTPView, UserListView, UserDetailView,
    SetRoleView, UserPermissionsView,
    SocialLoginView, TwoFactorAuthView, DeactivateAccountView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("me/", MeView.as_view(), name="me"),

    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("reset-password/", ResetPasswordRequestView.as_view(), name="reset_password"),
    path("reset-password-confirm/", ResetPasswordConfirmView.as_view(), name="reset_password_confirm"),

    path("verify-email/", VerifyEmailView.as_view(), name="verify_email"),
    path("resend-verification/", ResendVerificationView.as_view(), name="resend_verification"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify_otp"),

    path("", UserListView.as_view(), name="user_list"),  # GET /api/users/
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),  # GET /api/users/{id}/
    path("<int:pk>/set-role/", SetRoleView.as_view(), name="set_role"),
    path("permissions/", UserPermissionsView.as_view(), name="user_permissions"),

    path("social-login/", SocialLoginView.as_view(), name="social_login"),
    path("two-factor/", TwoFactorAuthView.as_view(), name="two_factor"),
    path("deactivate/", DeactivateAccountView.as_view(), name="deactivate_account"),
]
