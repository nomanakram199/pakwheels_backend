from django.urls import path
from .views import SignupView, OTPVerifyView, LoginView, ResendOTPView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
]