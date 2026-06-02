import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

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


class ImageSerializer(serializers.ModelSerializer):
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
    brand_name = serializers.CharField(
        source='model.brand.name', read_only=True
    )
    seller = SellerSerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = [
            'id',
            'model',
            'model_name',
            'brand_name',
            'seller',
            'year',
            'license_plate',
            'city',
            'price',
            'condition',
            'images',
            'created',
            'modified',
        ]
        read_only_fields = ['created', 'modified']


class CarDetailSerializer(serializers.ModelSerializer):
    model = CarModelSerializer(read_only=True)
    seller = SellerSerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = [
            'id',
            'model',
            'seller',
            'year',
            'license_plate',
            'city',
            'price',
            'condition',
            'description',
            'images',
            'created',
            'modified',
        ]
        read_only_fields = ['created', 'modified']


class CarCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            'model', 'year', 'license_plate', 'city', 'price',
            'condition', 'description'
        ]

    def validate_year(self, value):
        current_year = datetime.date.today().year
        if value < 1886 or value > current_year + 1:
            raise serializers.ValidationError(
                f"Year must be between 1886 and {current_year + 1}."
            )
        return value
