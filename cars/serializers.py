from rest_framework import serializers

from cars.models import Brand, CarModel

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


class BrandQuerySerializer(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=True,trim_whitespace=True)


class CarModelQuerySerializer(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=True,trim_whitespace=True)
    brand_id = serializers.IntegerField(required=False)
