from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from cars.filters import BrandFilter, CarModelFilter
from cars.models import Brand, CarModel
from cars.serializers import (
    BrandSerializer,
    CarModelSerializer,
    CarModelQuerySerializer,
    BrandQuerySerializer,
)

class BrandListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query_serializer = BrandQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        queryset = Brand.objects.all()
        brand_filter = BrandFilter(query_serializer.validated_data, queryset=queryset)

        serializer = BrandSerializer(brand_filter.qs, many=True)
        return Response(serializer.data)


class ModelListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query_serializer = CarModelQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        queryset = CarModel.objects.select_related('brand')
        model_filter = CarModelFilter(query_serializer.validated_data, queryset=queryset)

        serializer = CarModelSerializer(model_filter.qs, many=True)
        return Response(serializer.data)
