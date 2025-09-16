from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
import psycopg2
from psycopg2 import sql
import subprocess

class Command(BaseCommand):
    help = "Create database and run migrations if database does not exist" \
    "\nUsage run command: python manage.py create_db" 


    def handle(self, *args, **kwargs):
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']

        conn = psycopg2.connect(
            dbname='postgres',
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname=%s", (db_name,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            self.stdout.write(self.style.SUCCESS(f"Database '{db_name}' created successfully."))
        else:
            self.stdout.write(self.style.WARNING(f"Database '{db_name}' already exists."))

        cursor.close()
        conn.close()

        subprocess.run(["python", "manage.py", "migrate"])

        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="admin123"
            )
            self.stdout.write(self.style.SUCCESS("Default superuser created: admin / admin123"))
        else:
            self.stdout.write(self.style.WARNING("Superuser 'admin' already exists."))
