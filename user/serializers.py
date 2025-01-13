from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from jsonschema.validators import validate
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

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                raise serializers.ValidationError("이메일 또는 비밀번호가 올바르지 않습니다.")
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("이메일과 비밀번호를 모두 입력해주세요.")


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'profile', 'uuid')        # 보안을 위해 password 필드는 제외


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'uuid', 'profile')

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    profile = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'profile']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# 비밀번호 재설정
CustomUser = get_user_model()

class PasswordValidator:
    # 비밀번호 길이 검증을 위한 커스텀 유효성 검사기
    def __init__(self, min_length=8, max_length=20):
        self.min_length = min_length
        self.max_length = max_length

    def __call__(self, password):
        if len(password) < self.min_length or len(password) > self.max_length:
            raise ValidationError(
                f"비밀번호의 길이는 {self.min_length}자 이상 {self.max_length}자 이하여야 합니다."
            )

class NewPasswordSerializer(serializers.Serializer):
    # 비밀번호 재설정 요청을 위한 시리얼라이저
    email = serializers.EmailField()

class SetNewPasswordSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()  # UUID 필드로 변경
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        # 새 비밀번호 일치 여부 확인
        if data["new_password"] != data["new_password2"]:
            raise serializers.ValidationError("새 비밀번호가 서로 일치하지 않습니다.")

        try:
            uuid = data['uuid']
            user = CustomUser.objects.get(uuid=uuid)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("유효하지 않은 사용자입니다.")

        # 새 비밀번호가 현재 비밀번호와 다른지 확인
        if user.check_password(data["new_password"]):
            raise serializers.ValidationError("새로운 비밀번호는 이전 비밀번호와 달라야 합니다.")

        # Django의 기본 비밀번호 유효성 검사 및 커스텀 길이 검사 실행
        try:
            validate_password(data["new_password"], user=user)
            PasswordValidator()(data["new_password"])
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return data
    """
    1. 사용자가 비밀번호 재설정 요청
    2. 사용자 이메일로 재설정 링크 전송
    3. 링크에 uid, token 포함 되어있음
    4. 사용자 링크 클릭시 프론트에서 uid, token 추출
    5. 사용자 새 비번 입력시 프론트에서 uid, tokem, 새비번 백엔드로
    """

class UserDeleteResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    deletion_date = serializers.DateTimeField()

class UserDeleteRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirm = serializers.BooleanField(required=True)