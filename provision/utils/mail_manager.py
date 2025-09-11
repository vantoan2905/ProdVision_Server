from django.core.mail import send_mail
from django.conf import settings


class MailFormation:
    @staticmethod
    def code_registration(user, code):
        return (
            "Verify your email",
            f"Hello {user.username},\n\nYour verification code is: {code}\n\nThank you!",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )

    @staticmethod
    def code_reset_password(user, code):
        return (
            "Reset your password",
            f"Hello {user.username},\n\nYour password reset code is: {code}\n\nThank you!",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )

    @staticmethod
    def notify_admin(subject, message):
        return subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL]

    @staticmethod
    def notify_user(subject, message, user):
        return subject, message, settings.DEFAULT_FROM_EMAIL, [user.email]


class MailManager:
    @staticmethod
    def send_mail(subject, message, from_email, recipient_list, fail_silently=False):
        send_mail(subject, message, from_email, recipient_list, fail_silently=fail_silently)



