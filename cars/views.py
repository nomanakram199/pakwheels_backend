from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.exceptions import PermissionDenied
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

    def get_queryset(self):
        return Car.objects.with_car_relations()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CarCreateUpdateSerializer
        return CarListSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class CarRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSellerOrReadOnly]

    def get_queryset(self):
        return Car.objects.with_car_relations()

    def get_serializer_class(self):
        if self.request.method in {'PUT', 'PATCH'}:
            return CarCreateUpdateSerializer
        return CarDetailSerializer

    def destroy(self, request, *args, **kwargs):
        car = self.get_object()
        car.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyCarListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter

    def get_queryset(self):
        return Car.objects.with_car_relations().filter(seller=self.request.user)


class CarImageUploadAPIView(CreateAPIView):
    serializer_class = ImageCreateSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        car = get_object_or_404(
            Car.objects.select_related('seller'),
            pk=self.kwargs['pk'],
        )
        if car.seller_id != self.request.user.id:
            raise PermissionDenied("You can only upload images for your own cars.")

        image = serializer.save(car=car)
        if image.is_primary:
            car.images.exclude(id=image.id).update(is_primary=False)
