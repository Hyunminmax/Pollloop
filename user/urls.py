from django.urls import path

from user import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('oauth/kakao/login/', views.KakaoLoginView.as_view(), name='kakao_login'),
    path('oauth/kakao/callback/', views.KakaoCallbackView.as_view(), name='kakao_callback'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]