from django.urls import path
from .views import do

urlpatterns = [
    path('', do, name='home'),
]