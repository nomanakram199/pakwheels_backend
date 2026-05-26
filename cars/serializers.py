from rest_framework import serializers
from django.contrib.auth import get_user_model

from cars.models import Brand, CarModel, Car, Image


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']
        read_only_fields = fields


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'created']
        read_only_fields = ['created']


class CarModelSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = CarModel
        fields = ['id', 'brand', 'name', 'created']
        read_only_fields = ['created']


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'car', 'image', 'is_primary', 'created', 'modified']
        read_only_fields = ['created', 'modified']


class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'is_primary', 'created', 'modified']
        read_only_fields = ['id', 'created', 'modified']

class CarListSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source='model.name', read_only=True)
    brand_name = serializers.CharField(source='model.brand.name', read_only=True)
    seller = SellerSerializer(source='seller', read_only=True)
    images = ImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = [
            'id', 'model', 'model_name', 'brand_name', 'seller', 'year', 'license_plate', 'city', 'price',
            'condition', 'is_active', 'images', 'created', 'modified'
        ]
        read_only_fields = ['created', 'modified']


class CarDetailSerializer(serializers.ModelSerializer):
    model = CarModelSerializer(source='model', read_only=True)
    seller = SellerSerializer(source='seller', read_only=True)
    images = ImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = [
            'id', 'model', 'seller', 'year', 'license_plate', 'city', 'price',
            'condition', 'description', 'is_active', 'images', 'created', 'modified'
        ]
        read_only_fields = ['created', 'modified']


class CarCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            'model', 'year', 'license_plate', 'city', 'price',
            'condition', 'description'
        ]
