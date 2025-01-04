import uuid

from audioop import reverse
from django.shortcuts import render, redirect
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny

from config import settings_base
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer
import requests


# 회원가입
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary="사용자 회원가입",
        description="새로운 사용자 계정을 생성하고 JWT TOKEN 발급",
        request=RegisterSerializer,
        responses={
            201: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                'Successful registration',
                value={
                    "message": "회원가입이 성공적으로 완료되었습니다.",
                    "usernaem": "username예시",
                    "email": "user@gmail.com",
                    "refrash": "user_refresh_token",
                    "access": "user_access_token",
                },
                response_only=True,
                status_codes=["201"]
            ),
            OpenApiExample(
                'Failed registration',
                value={
                    "message": "이런 회원가입에 실패하셨습니다.",
                    "errors": {
                        "email": ["이미 존재하는 이메일입니다."],
                    }
                },
                response_only=True,
                status_codes=["400"]
            ),
            OpenApiExample(
                "Failed registration - Password Mismatch",
                value={
                    "message": "에큥 회원가입에 실패하셨습니다.",
                    "errors": {
                        "password2": ["비밀번호가 일치하지 않습니다."],
                    }
                },
                response_only=True,
                status_codes=["400"]
            )
        ]
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "회원가입이 성공적으로 완료되었습니다",
                "username": user.username,
                "email": user.email,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "회원가입에 실패하셨습니다.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# 로그인
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary="사용자 로그인",
        description="사용자 인증 및 JWT 토큰 발급",
        request=LoginSerializer,
        parameters=[
            OpenApiParameter(
                name='username',
                description="사용자 이름(필수)",       #
                required=True,
                type=str,
                location=OpenApiParameter.QUERY,
                examples=[
                    OpenApiExample(
                        name='username예시',
                        value='example_user',
                        description='예시로 제공된 사용자 이름'
                    ),
                ],
            ),
            OpenApiParameter(
                name='password',
                description="비밀번호(필수)",
                required=True,
                type=str,
                location=OpenApiParameter.QUERY,
                examples=[
                    OpenApiExample(
                        name='password예시',
                        value='password123',
                        description='예시로 제공된 비밀번호'
                    ),
                ],
            ),
        ],
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        }
    )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "로그인이 성공적으로 완료되었습니다.",
                "username": user.username,
                "email": user.email,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "로그인에 실패하셨습니다.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

