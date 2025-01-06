from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser

# 에러 메시지 상수
PASSWORD_MISMATCH_ERROR = "입력하신 비밀번호가 일치하지 않습니다. 다시 한번 확인해주세요."
INVALID_CREDENTIALS_ERROR = "이메일 또는 비밀번호가 올바르지 않습니다."
MISSING_FIELDS_ERROR = "이메일과 비밀번호 모두 입력해주세요."
PASSWORD_TOO_LONG_ERROR = "비밀번호는 20자를 초과할 수 없습니다."

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "password2"]

    def validate_password(self, value):
        # 비밀번호 길이 검증 (최대 20자)
        if len(value) > 20:
            raise ValidationError(PASSWORD_TOO_LONG_ERROR)
        return value

    def validate(self, data):
        # 비밀번호 일치 여부 검증
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(PASSWORD_MISMATCH_ERROR)
        return data

    def create(self, validated_data):
        # 비밀번호 확인 필드 제거
        validated_data.pop('password2', None)
        # 사용자 생성 및 반환
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            # 사용자 인증
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                raise serializers.ValidationError(INVALID_CREDENTIALS_ERROR)
        else:
            raise serializers.ValidationError(MISSING_FIELDS_ERROR)

        # JWT 토큰 생성
        data = super().validate(attrs)
        refresh = self.get_token(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = user
        return data

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'refresh', 'access']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'name', 'profile', 'age', 'uuid')
