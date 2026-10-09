import os
from pathlib import Path

import dj_database_url
from django.templatetags.static import static
from django.urls import reverse_lazy


BASE_DIR = Path(__file__).resolve().parent.parent

def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def env_list(name, default=""):
    return [item.strip() for item in os.environ.get(name, default).split(",") if item.strip()]


DEBUG = env_bool("DJANGO_DEBUG", True)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-change-me-pure-line-2026")
if not DEBUG and SECRET_KEY == "dev-only-change-me-pure-line-2026":
    raise RuntimeError("DJANGO_SECRET_KEY must be set to a strong unique value in production.")

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

INSTALLED_APPS = [
    "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "website",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pureline.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "pureline.wsgi.application"
ASGI_APPLICATION = "pureline.asgi.application"

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ar"
TIME_ZONE = "Asia/Riyadh"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DATA_UPLOAD_MAX_MEMORY_SIZE = 15 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 3 * 1024 * 1024

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        )
    },
}
WHITENOISE_MAX_AGE = 31536000

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", not DEBUG)
SECURE_REDIRECT_EXEMPT = [r"^health/$"]
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_SECURE_HSTS_SECONDS", "0" if DEBUG else "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

EMAIL_BACKEND = os.environ.get(
    "DJANGO_EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend" if DEBUG else "django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "Pure Line Website <website@localhost>")
CONTACT_NOTIFICATION_EMAIL = os.environ.get("CONTACT_NOTIFICATION_EMAIL", "")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO")},
}

UNFOLD = {
    "SITE_TITLE": "لوحة إدارة الخط النقي",
    "SITE_HEADER": "الخط النقي",
    "SITE_SUBHEADER": "إدارة الموقع وطلبات العملاء",
    "SITE_SYMBOL": "engineering",
    "SITE_ICON": lambda request: static("images/brand/logo-v2.webp"),
    "SITE_URL": "/",
    "SITE_DROPDOWN": [
        {
            "icon": "language",
            "title": "عرض الموقع",
            "link": "/",
            "attrs": {"target": "_blank"},
        },
        {
            "icon": "settings",
            "title": "إعدادات الشركة",
            "link": reverse_lazy("pureline_admin:website_sitesettings_changelist"),
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "BORDER_RADIUS": "12px",
    "COLORS": {
        "primary": {
            "50": "#fffaf0",
            "100": "#fff0cc",
            "200": "#ffe099",
            "300": "#f5c451",
            "400": "#e5b13d",
            "500": "#d8a63a",
            "600": "#b98724",
            "700": "#91671b",
            "800": "#6f4d18",
            "900": "#563d17",
            "950": "#2f200b",
        }
    },
    "LOGIN": {"image": lambda request: static("images/services/hvac.webp")},
    "STYLES": [lambda request: static("css/admin.css")],
    "DASHBOARD_CALLBACK": "website.admin_dashboard.dashboard_callback",
    "ENVIRONMENT": "website.admin_dashboard.environment_callback",
    "COMMAND": {
        "search_models": [
            "website.Inquiry",
            "website.Service",
            "website.Project",
            "website.SiteSettings",
        ],
        "show_history": True,
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "نظرة عامة",
                "separator": False,
                "items": [
                    {
                        "title": "الرئيسية",
                        "icon": "dashboard",
                        "link": reverse_lazy("pureline_admin:index"),
                    },
                    {
                        "title": "طلبات التواصل",
                        "icon": "inbox",
                        "link": reverse_lazy("pureline_admin:website_inquiry_changelist"),
                        "badge": "website.admin_dashboard.new_inquiries_badge",
                        "badge_variant": "warning",
                    },
                ],
            },
            {
                "title": "محتوى الموقع",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "الخدمات",
                        "icon": "design_services",
                        "link": reverse_lazy("pureline_admin:website_service_changelist"),
                    },
                    {
                        "title": "المشروعات",
                        "icon": "domain",
                        "link": reverse_lazy("pureline_admin:website_project_changelist"),
                    },
                    {
                        "title": "خطوات العمل",
                        "icon": "account_tree",
                        "link": reverse_lazy("pureline_admin:website_processstep_changelist"),
                    },
                    {
                        "title": "قيم الشركة",
                        "icon": "workspace_premium",
                        "link": reverse_lazy("pureline_admin:website_companyvalue_changelist"),
                    },
                    {
                        "title": "الأرقام والإحصائيات",
                        "icon": "monitoring",
                        "link": reverse_lazy("pureline_admin:website_metric_changelist"),
                    },
                    {
                        "title": "آراء العملاء",
                        "icon": "reviews",
                        "link": reverse_lazy("pureline_admin:website_testimonial_changelist"),
                    },
                ],
            },
            {
                "title": "إعدادات الشركة",
                "separator": True,
                "items": [
                    {
                        "title": "البيانات والتواصل",
                        "icon": "contact_phone",
                        "link": reverse_lazy("pureline_admin:website_sitesettings_changelist"),
                    },
                    {
                        "title": "المستخدمون",
                        "icon": "group",
                        "link": reverse_lazy("pureline_admin:auth_user_changelist"),
                    },
                    {
                        "title": "الصلاحيات",
                        "icon": "admin_panel_settings",
                        "link": reverse_lazy("pureline_admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
}
