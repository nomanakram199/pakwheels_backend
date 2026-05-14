from rest_framework import serializers
from .models import Car
from catalog.serializers import ModelSerializer
from users.serializers import UserResponseSerializer


class CarListSerializer(serializers.ModelSerializer):
    model = ModelSerializer(read_only=True)
    seller = UserResponseSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'model', 'year', 'license_plate', 'city', 'price', 'condition', 'seller', 'created_at']
        read_only_fields = ['created_at']


class CarDetailSerializer(serializers.ModelSerializer):
    model = ModelSerializer(read_only=True)
    seller = UserResponseSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'model', 'year', 'license_plate', 'city', 'price', 'condition', 'description', 'seller', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CarCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'model', 'year', 'license_plate', 'city', 'price', 'condition', 'description']
        read_only_fields = ['id']
