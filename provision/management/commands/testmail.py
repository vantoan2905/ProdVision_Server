
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from provision.utils.mail_manager import MailFormation, MailManager


class Command(BaseCommand):
    help = "Test sending email"

    def handle(self, *args, **kwargs):
        user = User(username="toan", email="toanvippk115@gmail.com")
        subject, message, from_email, recipient_list = MailFormation.code_registration(user, "654321")
        MailManager.send_mail(subject, message, from_email, recipient_list)
        self.stdout.write(self.style.SUCCESS("✅ Test email sent successfully!"))
