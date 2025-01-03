from django.urls import path

from user import views

urlpatterns = [
    path('', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
]