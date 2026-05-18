from rest_framework import serializers
from catalog.models import Brand, Model


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['created_at']


class ModelsSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Model
        fields = ['id', 'brand', 'name', 'created_at']  
        read_only_fields = ['created_at']

class ModelByBrandQuerySerializer(serializers.Serializer):
    brand_id = serializers.IntegerField(required=True)
