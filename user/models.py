from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid as uuid_lib
from django.utils import timezone

class CustomUser(AbstractUser):
    # 기존 AbstractUser의 필드들을 유지하면서 확장
    email = models.EmailField(unique=True)  # EMAIL을 고유 식별자로 설정
    username = models.CharField(max_length=150, unique=True)  # username 필드 사용
    first_name = None
    last_name = None
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # 추가 필드
    name = models.CharField(max_length=100, blank=True)  # 사용자 이름 추가
    profile = models.CharField(max_length=255, blank=True)  # 사용자 프로필 추가
    age = models.IntegerField(blank=True, null=True)  # 나이 필드 추가
    refresh_token = models.CharField(max_length=255, blank=True)  # 리프레시 토큰 추가
    uuid = models.UUIDField(unique=True, default=uuid_lib.uuid4)  # UUID 필드 추가

    # email을 기본 인증 필드로 추가 설정
    USERNAME_FIELD = 'username'  # username을 기본 인증 필드로 사용
    REQUIRED_FIELDS = ['email']  # createsuperuser에서 추가로 요구하는 필드

    def __str__(self):
        return self.username  # username을 사용자 문자열 표현으로 사용