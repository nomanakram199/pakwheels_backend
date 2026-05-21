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
        queryset = Brand.objects.all()

        search = request.query_params.get('search','').strip()
        if search:
            queryset = queryset.filter(name__icontains=search)
            
        serializer = BrandSerializer(queryset, many=True)
        return Response(serializer.data)


class ModelListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        brand_id = request.query_params.get('brand_id')
        search = request.query_params.get('search','').strip()
        queryset = CarModel.objects.select_related('brand')

        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)

        if search:
            queryset = queryset.filter(name__icontains=search)

        serializer = CarModelSerializer(queryset, many=True)
        return Response(serializer.data)
