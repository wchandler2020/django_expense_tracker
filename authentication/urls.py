from django.contrib import admin
from django.urls import path
from .views import RegistrationView, UserNameValidationView, EmailValidationView, VerificationView, LoginView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('registration', RegistrationView.as_view(), name='registration'),
    path('registration', LoginView.as_view(), name='login'),
    path('validate-username', csrf_exempt(UserNameValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('activate/<uidb64>/<token>', csrf_exempt(VerificationView.as_view()), name='activate'),
    
]