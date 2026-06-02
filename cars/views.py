from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from cars.filters import BrandFilter, CarFilter, CarModelFilter
from cars.models import Brand, CarModel, Car
from cars.permissions import IsSellerOrReadOnly
from cars.serializers import (
    BrandSerializer,
    CarCreateUpdateSerializer,
    CarDetailSerializer,
    CarListSerializer,
    CarModelSerializer,
    ImageCreateSerializer,
)


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


class CarListCreateAPIView(ListCreateAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter
    queryset = Car.objects.with_car_relations()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CarCreateUpdateSerializer
        return CarListSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class CarRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.with_car_relations()
    permission_classes = [IsSellerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in {'PUT', 'PATCH'}:
            return CarCreateUpdateSerializer
        return CarDetailSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()


class MyCarListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter

    def get_queryset(self):
        return Car.objects.with_car_relations().filter(
            seller=self.request.user
        )


class CarImageUploadAPIView(CreateAPIView):
    serializer_class = ImageCreateSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsSellerOrReadOnly]

    def get_car(self):
        return get_object_or_404(
            Car.objects.only('id', 'seller_id'),
            pk=self.kwargs['pk'],
        )

    @transaction.atomic
    def perform_create(self, serializer):
        car = self.get_car()
        self.check_object_permissions(self.request, car)
        image = serializer.save(car=car)
        if image.is_primary:
            car.images.exclude(id=image.id).update(is_primary=False)
