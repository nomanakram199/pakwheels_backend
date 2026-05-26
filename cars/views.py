from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from cars.filters import BrandFilter, CarModelFilter
from cars.models import Brand, CarModel
from cars.serializers import BrandSerializer, CarModelSerializer


class BrandListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BrandFilter


class ModelListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = CarModel.objects.select_related('brand')
    serializer_class = CarModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarModelFilter
