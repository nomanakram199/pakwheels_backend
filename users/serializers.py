from datetime import timedelta
import logging
import random

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from users.models import User

logger = logging.getLogger(__name__)

class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number', 'first_name', 'last_name', 'city']
        extra_kwargs = {
            'phone_number': {'required': True,'min_length': 8,},
            'city': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.otp_expires_at = timezone.now() + timedelta(minutes=5)
        logger.info(f"OTP sent to email {user.email}: {otp}")
        user.save(update_fields=['otp', 'otp_expires_at'])
        return user


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6, min_length=6)

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP must be numeric.")
        return value

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise NotFound("User not found.")

        if user.is_verified:
            raise serializers.ValidationError("Email already verified.")

        if user.otp != data['otp']:
            raise serializers.ValidationError("Invalid OTP.")

        if timezone.now() > user.otp_expires_at:
            raise serializers.ValidationError("OTP expired.")

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        user.is_verified = True
        user.save(update_fields=['is_verified'])
        return user


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")

        if not user.is_verified:
            raise serializers.ValidationError("Please verify email first.")

        if not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid credentials.")

        data['user'] = user
        return data


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise NotFound("User not found.")

        if user.is_verified:
            raise serializers.ValidationError("Email already verified.")

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.otp_expires_at = timezone.now() + timedelta(minutes=10)
        logger.info(f"OTP sent to email {user.email}: {otp}")
        user.save(update_fields=['otp', 'otp_expires_at'])
        return user


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'city', 'is_verified', 'created_at', 'updated_at']


