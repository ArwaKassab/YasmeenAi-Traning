# users/urls.py
from django.urls import path
from .views import UserRegisterView, UserLoginView, AdminRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('register/admin/', AdminRegisterView.as_view(), name='register-admin'),
    path('login/', UserLoginView.as_view(), name='login'),
]
