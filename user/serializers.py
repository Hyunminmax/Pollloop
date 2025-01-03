from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser

# 에러 메시지 상수
PASSWORD_MISMATCH_ERROR = "입력하신 비밀번호가 일치하지 않습니다. 다시 한번 확인해주세요."
INVALID_CREDENTIALS_ERROR = "이메일 또는 비밀번호가 올바르지 않습니다."
MISSING_FIELDS_ERROR = "이메일과 비밀번호 모두 입력해주세요."

# 회원가입
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,        # 해쉬 처리
        required=True,
        validators=[validate_password]      # 비밀번호 검증
    )
    # password와 같은지 확인 추가 입력
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "password2")


    # password와 password2가 같은지 유효성 검사
    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(PASSWORD_MISMATCH_ERROR)
        return data

    def create(self, validated_data):
        validated_data.pop('password2', None)
        user = CustomUser.objects.create_user(**validated_data)
        return user

# 로그인
class LoginSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                raise serializers.ValidationError(INVALID_CREDENTIALS_ERROR)
        else:
            raise serializers.ValidationError(MISSING_FIELDS_ERROR)

        data = super().validate(attrs)
        refresh = self.get_token(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = user
        return data
