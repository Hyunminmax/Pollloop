from django.urls import path

from user import views


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),

    # password 재설정
    path('password-reset/', views.RequestPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/', views.SetNewPasswordView.as_view(), name='password_reset_confirm'),

    # Kakao 소셜로그인
    path('oauth/kakao/login/', views.KakaoLoginView.as_view(), name='kakao_login'),
    path('oauth/kakao/callback/', views.KakaoCallbackView.as_view(), name='kakao_callback'),

]