from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt


from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .serializers import *
from datetime import timezone, timedelta
import requests
import uuid


# 사용자 회원가입을 처리하는 뷰
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # 누구나 접근 가능
    authentication_classes = []  # 인증 불필요

    @extend_schema(
        summary="사용자 회원가입",
        description="새로운 사용자 계정을 생성하고 JWT TOKEN 발급 (비밀번호는 8자 이상 20자 이하)",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'nullable': True},
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
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            # 리프레시 토큰 저장
            user.refresh_token = str(refresh)
            user.save()

            return Response({
                "message": "로그인이 성공적으로 완료되었습니다.",
                "email": user.email,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({
            "message": "로그인에 실패하셨습니다.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# 카카오 로그인 URL을 제공하는 뷰
# class KakaoLoginView(APIView):
#     permission_classes = [AllowAny]  # 누구나 접근 가능
#
#     @extend_schema(
#         summary="카카오 로그인 URL 요청",
#         description="카카오 로그인을 위한 인증 URL을 반환합니다.",
#         responses={200: OpenApiTypes.OBJECT},
#         tags=["Kakao Social"],
#     )
#     def get(self, request):
#         # 카카오 로그인 URL 생성
#         kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={settings.KAKAO_REST_API_KEY}&redirect_uri={settings.KAKAO_REDIRECT_URI}&response_type=code"
#         return Response({"auth_url": kakao_auth_url})
#

# 카카오 로그인 콜백을 처리하는 뷰
class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]  # 누구나 접근 가능

    @extend_schema(
        summary="카카오 로그인 콜백 처리",
        description="카카오 로그인 후 받은 코드로 사용자 정보를 조회하고 로그인 처리합니다.",
        parameters=[
            OpenApiParameter(name='code', description='카카오 인증 코드', required=True, type=str)
        ],
        responses={200: UserSerializer},
        tags=["Kakao Social"],
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
            # 이미 가입된 사용자인 경우
            user = CustomUser.objects.get(email=kakao_account.get("email"))
        except CustomUser.DoesNotExist:
            # 새로운 사용자 생성
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
    authentication_classes = []  # 인증 클래스 제거
    permission_classes = []  # 권한 클래스 제거

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "리프레시 토큰이 제공되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

CustomUser = get_user_model()

class RequestPasswordResetView(APIView):
    # 비밀번호 재설정 요청을 처리하는 뷰
    permission_classes = [AllowAny]

    @extend_schema(
        summary="비밀번호 재설정 요청",
        description="사용자 이메일로 비밀번호 재설정 링크를 발송합니다.",
        request=NewPasswordSerializer,
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="비밀번호 재설정 이메일 발송 성공",
                examples=[
                    OpenApiExample(
                        "Success",
                        value={
                            "message": "비밀번호 재설정 이메일을 발송했습니다.",
                            "email": "CustomUser.email"
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="잘못된 요청",
                examples=[
                    OpenApiExample(
                        "Invalid Email",
                        value={"error": "유효하지 않은 이메일 형식입니다."}
                    )
                ]
            ),
            404: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="사용자를 찾을 수 없음",
                examples=[
                    OpenApiExample(
                        "User Not Found",
                        value={"error": "해당 이메일로 등록된 사용자가 없습니다."}
                    )
                ]
            )
        }
    )
    def post(self, request):
        serializer = NewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({'error': '해당 이메일로 등록된 사용자가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

            token = default_token_generator.make_token(user)
            uid = user.uuid
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

            send_mail(
                '비밀번호 재설정',
                f'비밀번호를 재설정하려면 다음 링크를 클릭하세요: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return Response({'message': '비밀번호 재설정 이메일을 발송했습니다.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordView(APIView):
    # 새 비밀번호 설정을 처리하는 뷰
    permission_classes = [AllowAny]

    @extend_schema(
        summary="새 비밀번호 설정",
        description="비밀번호 재설정 링크를 통해 새 비밀번호를 설정합니다.",
        request=SetNewPasswordSerializer,
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT}
    )
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']
            password = serializer.validated_data['new_password']

            try:
                user = CustomUser.objects.get(uuid=uid)
            except CustomUser.DoesNotExist:
                return Response({'error': '유효하지 않은 사용자입니다.'}, status=status.HTTP_400_BAD_REQUEST)

            if default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                return Response({'message': '비밀번호가 성공적으로 재설정되었습니다.'}, status=status.HTTP_200_OK)
            return Response({'error': '유효하지 않은 토큰입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user profile 관리 페이지

class UserProfileRetrieveUpdateView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="사용자 프로필 조회",
        description="현재 로그인한 사용자의 프로필 정보를 조회합니다.",
        responses={200: UserProfileSerializer},
        tags=["프로필"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="사용자 프로필 수정",
        description="현재 로그인한 사용자의 프로필 정보를 수정합니다.",
        request=UserProfileUpdateSerializer,
        responses={
            200: OpenApiResponse(response=UserProfileSerializer, description="프로필 수정 성공"),
            400: OpenApiResponse(description="잘못된 요청"),
        },
        examples=[
            OpenApiExample(
                "프로필 수정 예시",
                value={
                    "phone_number": "010xxxxxxxx",
                    "profile": "str"
                },
                request_only=True
            )
        ],
        tags=["프로필"]
    )
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_object(self):
        return self.request.user.userprofile

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer
        return UserProfileUpdateSerializer

    def perform_update(self, serializer):
        serializer.save()


class UserDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary='user 계정 정보 삭제 요청',
        description='계정 탈퇴를 요청하고 50일 후 삭제 예정',
        request=UserDeleteRequestSerializer,
        responses={200: UserDeleteResponseSerializer}
    )
    def post(self, request):
        serializer = UserDeleteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not serializer.validated_data['confirm']:
            return Response({"error": "계정 삭제를 확인하지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.withdraw_at = timezone.now()
        user.is_active = False
        user.save()

        deletion_date = user.withdraw_at + timedelta(days=50)

        response_data = {
            "message": "계정 탈퇴가 요청되었습니다. 50일 후에 완전히 삭제됩니다.",
            "deletion_date": deletion_date
        }

        response_serializer = UserDeleteResponseSerializer(data=response_data)
        response_serializer.is_valid()

        return Response(response_serializer.data, status=status.HTTP_200_OK)