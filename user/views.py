import uuid
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny

from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
import requests

# 사용자 회원가입을 처리하는 뷰
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary="사용자 회원가입",
        description="새로운 사용자 계정을 생성하고 JWT TOKEN 발급 (비밀번호는 8자 이상 20자 이하)",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'nullable':True},
                    'email': {'type': 'string'},
                    'password': {'type': 'string', 'minLength': 8, 'maxLength': 20},
                    'password2': {'type': 'string', 'minLength': 8, 'maxLength': 20},
                },
                'required': ['email', 'password', 'password2']
            }
        },
        responses={
            201: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            # 성공적인 회원가입 예시
            OpenApiExample(
                'Successful registration',
                value={
                    "message": "회원가입이 성공적으로 완료되었습니다",
                    "username": "newuser",
                    "email": "newuser@example.com",
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                },
                response_only=True,
                status_codes=["201"]
            ),
            # 이미 존재하는 이메일로 인한 실패 예시
            OpenApiExample(
                'Failed registration - Email exists',
                value={
                    "message": "회원가입에 실패하셨습니다.",
                    "errors": {
                        "email": [
                            "이미 이 이메일로 등록된 사용자가 있습니다."
                        ]
                    }
                },
                response_only=True,
                status_codes=["400"]
            ),
            # 비밀번호 불일치로 인한 실패 예시
            OpenApiExample(
                "Failed registration - Password mismatch",
                value={
                    "message": "회원가입에 실패하셨습니다.",
                    "errors": {
                        "password2": [
                            "두 개의 비밀번호 필드가 일치하지 않습니다."
                        ]
                    }
                },
                response_only=True,
                status_codes=["400"]
            ),
            # 유효하지 않은 비밀번호로 인한 실패 예시
            OpenApiExample(
                "Failed registration - Invalid password",
                value={
                    "message": "회원가입에 실패하셨습니다.",
                    "errors": {
                        "password": [
                            "이 비밀번호는 너무 짧습니다. 최소 8자 이상이어야 합니다.",
                            "이 비밀번호는 전부 숫자로 되어 있습니다."
                        ]
                    }
                },
                response_only=True,
                status_codes=["400"]
            ),
            # 비밀번호가 너무 긴 경우의 실패 예시
            OpenApiExample(
                "Failed registration - Password too long",
                value={
                    "message": "회원가입에 실패하셨습니다.",
                    "errors": {
                        "password": [
                            "비밀번호는 20자를 초과할 수 없습니다."
                        ]
                    }
                },
                response_only=True,
                status_codes=["400"]
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        # 회원가입 데이터 유효성 검사
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 유효한 데이터로 사용자 생성
            user = serializer.save()
            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "회원가입이 성공적으로 완료되었습니다",
                "username": user.username,
                "email": user.email,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        # 유효성 검사 실패 시 에러 반환
        return Response({
            "message": "회원가입에 실패하셨습니다.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# 사용자 로그인을 처리하는 뷰
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary="사용자 로그인",
        description="사용자 인증 및 JWT 토큰 발급",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'},
                },
                'required': ['email', 'password']
            }
        },
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "로그인이 성공적으로 완료되었습니다.",
                "email": user.email,
                "username": user.username,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "로그인에 실패하셨습니다.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# 카카오 로그인 URL을 제공하는 뷰
class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="카카오 로그인 URL 요청",
        description="카카오 로그인을 위한 인증 URL을 반환합니다.",
        responses={200: OpenApiTypes.OBJECT}
    )
    def get(self, request):
        # 카카오 로그인 URL 생성
        kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={settings.KAKAO_REST_API_KEY}&redirect_uri={settings.KAKAO_REDIRECT_URI}&response_type=code"
        return Response({"auth_url": kakao_auth_url})

# 카카오 로그인 콜백을 처리하는 뷰
class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="카카오 로그인 콜백 처리",
        description="카카오 로그인 후 받은 코드로 사용자 정보를 조회하고 로그인 처리합니다.",
        parameters=[
            OpenApiParameter(name='code', description='카카오 인증 코드', required=True, type=str)
        ],
        responses={200: UserSerializer}
    )
    def get(self, request):
        code = request.GET.get('code')

        # 카카오 액세스 토큰 요청
        token_req = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": settings.KAKAO_REST_API_KEY,
                "redirect_uri": settings.KAKAO_REDIRECT_URI,
                "code": code,
            },
        )
        token_req_json = token_req.json()
        access_token = token_req_json.get("access_token")

        # 카카오 사용자 정보 요청
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")

        # 사용자 생성 또는 조회
        try:
            user = CustomUser.objects.get(email=kakao_account.get("email"))
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(
                username=kakao_account.get("email").split("@")[0],
                email=kakao_account.get("email"),
                name=kakao_account.get("profile", {}).get("nickname", ""),
                profile=kakao_account.get("profile", {}).get("profile_image_url", ""),
            )

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        user.refresh_token = str(refresh)
        user.save()

        return Response({
            "user": UserSerializer(user).data,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        })

# 사용자 로그아웃을 처리하는 뷰
class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        summary="사용자 로그아웃",
        description="사용자의 리프레시 토큰을 무효화합니다.",
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request):
        user = request.user
        # 리프레시 토큰 무효화
        user.refresh_token = ""
        user.save()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
