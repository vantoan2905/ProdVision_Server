from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a customer user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True, help='Username')
        parser.add_argument('--email', type=str, required=True, help='Email')
        parser.add_argument('--password', type=str, required=True, help='Password')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR('User already exists'))
            return

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_type='customer'  # 🔥 Nếu bạn có field user_type
        )

        self.stdout.write(self.style.SUCCESS(f'Customer user {username} created successfully'))
x