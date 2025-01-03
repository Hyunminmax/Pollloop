"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
from dotenv import dotenv_values


# env 파일 로드
ENV = dotenv_values(".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV.get("Secret_Key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
CUSTOM_APPS = [
    'ask',
    'form',
    'user',
    'rest_framework',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'django_seed',
    'rest_framework_simplejwt',
]

SYSTEM_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS = CUSTOM_APPS + SYSTEM_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': ENV.get('DB_ENGINE'),
        'NAME': ENV.get('DB_NAME'),
        'USER': ENV.get('DB_USER'),
        'PASSWORD': ENV.get('DB_PASSWORD'),
        'HOST': ENV.get('DB_HOST'),
        'PORT': ENV.get('DB_PORT'),
    }
}

AUTH_USER_MODEL = "user.CustomUser"


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Swagger settings
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': "rest_framework_simplejwt.authentication.JWTAuthentication",

    # JWT 토큰 활성화 후 적용
    # 'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication',],
    # 'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated',],
}
# Swagger settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Pollloop',
    'DESCRIPTION': '폼!폼! 뿌린!',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,  # 스키마 엔드포인트를 포함하지 않도록 설정
}   # '/api/schema/' 숨김처리


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


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

SIMPLE_JWT = {
    # 토큰 수명관리
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),     # ACCESS_TOKEN 유효기간
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),        # 새로고침 토큰 유효기간
    # 토큰 갱신 정책
    'ROTATE_REFRESH_TOKENS': True,         # 리플레시 토큰 사용시 새로운 토큰 발급여부
    'BLACKLIST_AFTER_ROTATION': True,       # 사용한 리플래시 토큰 -> 블랙리스트로 할지
# 보안 설정
    # 일고리즘 and 키 관리
    "ALGORITHM": "HS256",       # token 서명/검증에 사용할 알고리즘
    "SIGNING_KEY": SECRET_KEY,     # token 서명에 사용되는 키
    "VERIFYING_KEY": "",        # token 검증에 사용되는 키
    # 토큰 클레임
    "AUDIENCE": None,           # token의 대상 지정
    "ISSUER": None,             # token 발급자 지정
    #
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 180,      # 만료시간 3분 여유 시간 지정
# 사용자 인증
    # 헤더 설정
    "AUTH_HEADER_TYPES": ("Bearer",),       # 허용되는 인증 헤더 타입
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",       # 인증에 사용할 헤더 이름
    "USER_ID_FIELD": "id",                  # token에 포함될 사용자 식별 필드
    "USER_ID_CLAIM": "user_id",             # 사용자 식별자를 지정할 클레임 이름
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    # 토큰 유형 및 검증
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),     # 인증 가능한 토큰 유형 지정
    "TOKEN_TYPE_CLAIM": "token_type",                                           # 토큰 유형을 지정하는 클레임
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",            # 토큰의 고유 식별자를 지정하는 클레임 이름

    "JTI_CLAIM": "jti",
    # 슬라이딩 토큰 (선택)
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",       # 슬라이딩 토큰의 인증 유효긴간
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}