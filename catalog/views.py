from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from catalog.models import Brand, Model as CarModel
from catalog.serializers import BrandSerializer, ModelsSerializer


class BrandListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)


class BrandDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, brand_id):
        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)


class ModelListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        models = CarModel.objects.all().select_related('brand')
        serializer = ModelsSerializer(models, many=True)
        return Response(serializer.data)


class ModelDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, model_id):
        try:
            model = CarModel.objects.select_related('brand').get(id=model_id)
        except CarModel.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ModelsSerializer(model)
        return Response(serializer.data)


class ModelByBrandAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        brand_id = request.query_params.get('brand_id')
        if not brand_id:
            return Response({'error': 'brand_id required'}, status=status.HTTP_400_BAD_REQUEST)

        models = CarModel.objects.select_related('brand').filter(brand_id=brand_id)
        serializer = ModelsSerializer(models, many=True)
        return Response(serializer.data)

