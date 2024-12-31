from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
import uuid as uuid_lib

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # 오버라이딩
    email = models.EmailField(unique=True) # 오버라이딩 필요
    
    # 추가
    name = models.CharField(max_length=100) # 추가
    profile = models.CharField(max_length=255) #추가
    age = models.IntegerField(default=0) #추가 
    refresh_token = models.CharField(max_length=255) #추가
    uuid = models.UUIDField(unique=True) #추가

    USERNAME_FIELD = 'email'
    # class Meta:
    #     db_table = 'user'
    #     verbose_name = 'user'
    #     verbose_name_plural = 'Users'
