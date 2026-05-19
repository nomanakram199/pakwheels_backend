from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from cars.models import Brand, CarModel
from cars.serializers import (
    BrandSerializer,
    CarModelSerializer,
)

class BrandListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)


class ModelListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        brand_id = request.query_params.get('brand_id')
        queryset = CarModel.objects.select_related('brand')

        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)

        serializer = CarModelSerializer(queryset, many=True)
        return Response(serializer.data)
