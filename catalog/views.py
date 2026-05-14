from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Brand, Model
from .serializers import BrandSerializer, ModelSerializer


class BrandListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)


class BrandDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, brand_id):
        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)


class ModelListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        models = Model.objects.all().select_related('brand')
        serializer = ModelSerializer(models, many=True)
        return Response(serializer.data)


class ModelDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, model_id):
        try:
            model = Model.objects.get(id=model_id).select_related('brand')
        except Model.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ModelSerializer(model)
        return Response(serializer.data)


class ModelByBrandView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        brand_id = request.query_params.get('brand_id')
        if not brand_id:
            return Response({'error': 'brand_id required'}, status=status.HTTP_400_BAD_REQUEST)

        models = Model.objects.filter(brand_id=brand_id).select_related('brand')
        serializer = ModelSerializer(models, many=True)
        return Response(serializer.data)
