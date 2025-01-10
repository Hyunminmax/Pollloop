from .settings_base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["43.200.4.153"]

CORS_ALLOW_METHODS = ["GET", "POST", "DELETE", "OPTIONS"]

# # 보안 설정 추가
# SECURE_HSTS_SECONDS = 3600
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

CORS_ALLOWED_ORIGINS = [
    # 3000으로 개발환경 세팅
    "http://localhost:3000",
    # 배포시
    "https://fe-three-omega.vercel.app"
]

CORS_ALLOW_CREDENTIALS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

