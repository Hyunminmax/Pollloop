from django.urls import path
from .views import FormCreateView, FormView, FormInvitedView

urlpatterns = [
    path('uuid:<slug:uuid>/', FormView.as_view(), name='FormLoad'),
    path('create/', FormCreateView.as_view(), name='NewForm'),
    path('invited/', FormInvitedView.as_view(), name='FormInvited'),
]
