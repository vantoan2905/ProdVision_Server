from pathlib import Path
import os
import dotenv
from mongoengine import connect

# ------------------------
# Base setup
# ------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv()

# ------------------------
# Basic settings
# ------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-default")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# ------------------------
# Installed apps
# ------------------------
INSTALLED_APPS = [
    "corsheaders",

    # Custom apps
    # "apps.task",
    # "apps.vision",
    # "apps.product",
    "apps.chatbot",
    # "apps.camera",
    # "apps.employee",

    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Authentication
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",

    # REST & Swagger
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
]

SITE_ID = 1
CORS_ORIGIN_ALLOW_ALL = True

# ------------------------
# REST Framework settings
# ------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1", "v2"],
    "VERSION_PARAM": "version",
}
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,  
    'AUTH_HEADER_TYPES': ('Bearer',),
}



# ------------------------
# Middleware
# ------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ⚡ Nên để ngay sau SecurityMiddleware
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "config.urls"

# ------------------------
# Templates
# ------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ------------------------
# Authentication
# ------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

LOGIN_REDIRECT_URL = "/swagger/"

# ------------------------
# Swagger
# ------------------------
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
    "DEFAULT_MODEL_RENDERING": "example",
    "PERSIST_AUTH": True,
    "USE_STATIC_URLS": True,  # ✅ Cho phép dùng static local
}

# ------------------------
# WSGI
# ------------------------
WSGI_APPLICATION = "config.wsgi.application"

# ------------------------
# Database (PostgreSQL)
# ------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "task_manager"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# ------------------------
# Password validators
# ------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------
# Internationalization
# ------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True

# ------------------------
# Static & Media
# ------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"        # Dùng khi chạy collectstatic
STATICFILES_DIRS = [BASE_DIR / "static"]      # Dùng trong dev
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------
# Default auto field
# ------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------
# Email settings
# ------------------------
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "webmaster@localhost")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

# ------------------------
# MongoDB Connection
# ------------------------
from mongoengine import connect

connect(
    db="prod_chatbot",
    host="mongodb://localhost:27017/prod_chatbot"
)
from mongoengine import get_connection
print("[DEBUG] MONGO CONNECT =", get_connection())

