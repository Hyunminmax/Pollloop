from django.urls import path
from .views import FormCreateView, FormView

urlpatterns = [
    path('uuid:<slug:uuid>/', FormView.as_view(), name='FormLoad'),
    path('create/', FormCreateView.as_view(), name='NewForm'),
]
