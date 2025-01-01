from django.urls import path
from .views import FormCreateView, FormView

urlpatterns = [
    path('form/<uuid:uuid>/', FormView.as_view(), name='FormLoad'),
    path('form/create/', FormCreateView.as_view(), name='NewForm'),
]
