from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from catalog.models import Brand, Model
from catalog.serializers import BrandSerializer, ModelsSerializer, ModelByBrandQuerySerializer


class BrandListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)


class BrandDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, brand_id):
        brand = get_object_or_404(Brand, id=brand_id)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)


class ModelListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        models = Model.objects.all().select_related('brand')
        serializer = ModelsSerializer(models, many=True)
        return Response(serializer.data)


class ModelDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, model_id):
        queryset = Model.objects.select_related('brand')
        model = get_object_or_404(queryset, id=model_id)
        serializer = ModelsSerializer(model)
        return Response(serializer.data)


class ModelByBrandAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query_serializer = ModelByBrandQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        brand_id = query_serializer.validated_data['brand_id']

        models = Model.objects.select_related('brand').filter(brand_id=brand_id)
        serializer = ModelsSerializer(models, many=True)
        return Response(serializer.data)
