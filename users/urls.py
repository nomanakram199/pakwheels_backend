from django.urls import path
from users.views import SignupAPIView, OTPVerifyAPIView, LoginAPIView, ResendOTPAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('verify-otp/', OTPVerifyAPIView.as_view(), name='verify_otp'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('resend-otp/', ResendOTPAPIView.as_view(), name='resend_otp'),
]

