# workout_tracker/settings.py
import os
from pathlib import Path
import urllib.parse as up

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Core ---
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "CHANGE_ME_FOR_LOCAL_DEV_ONLY")
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "pawelstrength.com,www.pawelstrength.com,127.0.0.1,localhost"
).split(",")

# --- Apps ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework.authtoken",

    "tracker",
    # "corsheaders",  # only if you later build a web client on another origin
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "workout_tracker.urls"
WSGI_APPLICATION = "workout_tracker.wsgi.application"

# --- Templates ---
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

# --- Database ---
# Option A: DATABASE_URL env (preferred)
#   export DATABASE_URL="postgres://USER:PASS@HOST:5432/DBNAME"
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

# Option B: Use your RDS values when DATABASE_URL is not set
RDS_HOST = "workout-tracker-db.cl8waeakayez.us-east-2.rds.amazonaws.com"
RDS_NAME = "workoutdb"
RDS_USER = "postgres"
RDS_PASSWORD = "***REMOVED***"
RDS_PORT = "5432"

if DATABASE_URL:
    up.uses_netloc.append("postgres")
    url = up.urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": (url.path or "/")[1:],
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": url.port or "5432",
            "CONN_MAX_AGE": 60,
            "OPTIONS": {"sslmode": "require"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": RDS_NAME,
            "USER": RDS_USER,
            "PASSWORD": RDS_PASSWORD,
            "HOST": RDS_HOST,
            "PORT": RDS_PORT,
            "CONN_MAX_AGE": 60,
            "OPTIONS": {"sslmode": "require"},
        }
    }

# --- Password validators ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- I18N ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static & Media (served by Nginx in prod) ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- Security (tight in prod) ---
CSRF_TRUSTED_ORIGINS = ["https://pawelstrength.com", "https://www.pawelstrength.com"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 86400 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = False  # enable later only when all subdomains are HTTPS-only
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"

# --- DRF ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

# --- CORS (off; not needed for iOS or static privacy page) ---
# if "corsheaders" in INSTALLED_APPS:
#     CORS_ALLOWED_ORIGINS = [
#         "https://pawelstrength.com",
#         "https://www.pawelstrength.com",
#     ]

# --- Logging ---
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO" if not DEBUG else "DEBUG"},
}
