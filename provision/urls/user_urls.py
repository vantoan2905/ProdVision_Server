from django.urls import path
from provision.views.user_views import (
    RegisterView, LogoutView, MeView, ChangePasswordView,
    ResetPasswordRequestView, ResetPasswordConfirmView,
    VerifyEmailView, ResendVerificationView,
    VerifyOTPView, UserListView, UserDetailView,
    SetRoleView, UserPermissionsView,
    SocialLoginView, TwoFactorAuthView, DeactivateAccountView, LoginView, RefreshTokenView
)
base_urls = 'user_management'

urlpatterns = [
    path(f"{base_urls}/register/", RegisterView.as_view(), name="register"),
    path(f"{base_urls}/login/", LoginView.as_view(), name="login"),
    path(f"{base_urls}/logout/", LogoutView.as_view(), name="logout"),
    path(f"{base_urls}/refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path(f"{base_urls}/me/", MeView.as_view(), name="me"),
    path(f"{base_urls}/change-password/", ChangePasswordView.as_view(), name="change_password"),
    path(f"{base_urls}/reset-password/", ResetPasswordRequestView.as_view(), name="reset_password"),
    path(f"{base_urls}/reset-password-confirm/", ResetPasswordConfirmView.as_view(), name="reset_password_confirm"),
    path(f"{base_urls}/verify-email/", VerifyEmailView.as_view(), name="verify_email"),
    path(f"{base_urls}/resend-verification/", ResendVerificationView.as_view(), name="resend_verification"),
    path(f"{base_urls}/verify-otp/", VerifyOTPView.as_view(), name="verify_otp"),
    path(f"{base_urls}/", UserListView.as_view(), name="user_list"),  # GET /api/users/
    path(f"{base_urls}/<int:pk>/", UserDetailView.as_view(), name="user_detail"),  # GET /api/users/{id}/
    path(f"{base_urls}/<int:pk>/set-role/", SetRoleView.as_view(), name="set_role"),
    path(f"{base_urls}/permissions/", UserPermissionsView.as_view(), name="user_permissions"),
    path(f"{base_urls}/social-login/", SocialLoginView.as_view(), name="social_login"),
    path(f"{base_urls}/two-factor/", TwoFactorAuthView.as_view(), name="two_factor"),
    path(f"{base_urls}/deactivate/", DeactivateAccountView.as_view(), name="deactivate_account"),
]
