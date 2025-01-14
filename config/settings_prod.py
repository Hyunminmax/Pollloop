from .settings_base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# 실제 서비스에서는 수정필요 "*" 삭제
ALLOWED_HOSTS = ["api.pollloop.store","*"]

# 실제 서비스에서는 로컬삭제, 5174포트는 방법을 찾아야.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # 프론트엔드 도메인
    "http://43.200.4.153",    # 백엔드 도메인
    # 배포시
    # "https://fe-three-omega.vercel.app"
    "https://pollloop.vercel.app",
]
# 실제 서비스에서 필요한지 테스트 필요
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = ["GET", "POST", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = ["content-type", "authorization", "x-csrf-token"]


# # 보안 설정 추가
SECURE_HSTS_SECONDS = 3600
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


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

