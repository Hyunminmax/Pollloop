from django.urls import path
from .views import InputFile

urlpatterns = [
    path('inputfile/', InputFile.as_view(), name='InputFile'),
    ]
