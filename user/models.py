from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid as uuid_lib
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, username, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수 입력 사항입니다.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    # 기존 AbstractUser의 필드들을 유지하면서 확장
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name="이메일")  # EMAIL을 고유 식별자로 설정
    first_name = None
    last_name = None
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # 추가 필드
    name = models.CharField(max_length=100, blank=True, verbose_name="이름")  # 사용자 이름 추가
    profile = models.CharField(max_length=255, blank=True, verbose_name="프로필")  # 사용자 프로필 추가
    age = models.IntegerField(blank=True, null=True, verbose_name="나이")  # 나이 필드 추가
    refresh_token = models.CharField(max_length=255, blank=True, verbose_name="리프레시 토큰")  # 리프레시 토큰 추가
    uuid = models.UUIDField(unique=True, default=uuid_lib.uuid4, editable=False, verbose_name="UUID")  # UUID 필드 추가

    objects = CustomUserManager()

    # email을 기본 인증 필드로 설정
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # createsuperuser에서 추가로 요구하는 필드

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자들"

    def __str__(self):
        return self.email  # email을 사용자 문자열 표현으로 사용
