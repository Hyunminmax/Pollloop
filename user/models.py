from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid as uuid_lib

class CustomUser(AbstractUser):
    # 오버라이딩
    email = models.EmailField(unique=True) # 오버라이딩 필요
    
    # 추가
    name = models.CharField(max_length=100) # 추가
    profile = models.CharField(max_length=255) #추가
    age = models.IntegerField(default=0) #추가 
    refresh_token = models.CharField(max_length=255) #추가
    uuid = models.UUIDField(default=uuid_lib.uuid4, unique=True) #추가

    # class Meta:
    #     db_table = 'user'
    #     verbose_name = 'user'
    #     verbose_name_plural = 'Users'