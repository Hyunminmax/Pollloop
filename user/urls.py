from django.urls import path

from user import views

urlpatterns = [
    path('', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    # path('social/kakao/log-in/', views.KakaoSocialLoginView.as_view(), name='kakao-social-login'),
    # path("social/kakao/callback/", views.KakaoSocialCallbackView.as_view(),name="kakao_social_callback"),

]