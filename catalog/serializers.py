from rest_framework import serializers
from .models import Brand, Model


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['created_at']


class ModelSerializer(serializers.ModelSerializer):
    # brand_id = serializers.IntegerField(source='brand.id', read_only=True) Not best practice
    # brand_name = serializers.CharField(source='brand.name', read_only=True)
    brand = BrandSerializer(read_only=True) # best practice

    class Meta:
        model = Model
        # fields = ['id', 'brand_id', 'brand_name', 'name', 'created_at'] 
        fields = ['id', 'brand', 'name', 'created_at']  
        read_only_fields = ['created_at']
