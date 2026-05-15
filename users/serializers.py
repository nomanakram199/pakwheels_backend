from rest_framework import serializers
from users.models import User
from django.utils import timezone
from datetime import timedelta
import random
import logging

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
            raise serializers.ValidationError("User not found.")

        if user.is_verified:
            raise serializers.ValidationError("Email already verified.")

        if user.otp != data['otp']:
            raise serializers.ValidationError("Invalid OTP.")

        if timezone.now() > user.otp_expires_at:
            raise serializers.ValidationError("OTP expired.")

        user.is_verified = True
        user.otp = None
        user.otp_expires_at = None
        user.save(update_fields=['is_verified', 'otp', 'otp_expires_at'])
        data['user'] = user
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
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
            raise serializers.ValidationError("User not found.")

        if user.is_verified:
            raise serializers.ValidationError("Email already verified.")

        otp = str(random.randint(100000, 999999))
        user.otp = otp
        print("OTP sent to your email:", otp)
        user.otp_expires_at = timezone.now() + timedelta(minutes=10)
        user.save(update_fields=['otp', 'otp_expires_at'])

        data['user'] = user
        data['otp'] = otp
        return data


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'city', 'is_verified', 'created_at', 'updated_at']


