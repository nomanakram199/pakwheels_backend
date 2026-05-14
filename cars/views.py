from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Car
from .serializers import CarListSerializer, CarDetailSerializer, CarCreateUpdateSerializer


class CarListView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        cars = Car.objects.filter(is_deleted=False).select_related('model', 'seller')
        serializer = CarListSerializer(cars, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CarCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, car_id):
        try:
            car = Car.objects.select_related('model', 'seller').get(id=car_id, is_deleted=False)
        except Car.DoesNotExist:
            return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CarDetailSerializer(car)
        return Response(serializer.data)

    def put(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id, seller=request.user, is_deleted=False)
        except Car.DoesNotExist:
            return Response({'error': 'Not your car'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CarCreateUpdateSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id, seller=request.user, is_deleted=False)
        except Car.DoesNotExist:
            return Response({'error': 'Not your car'}, status=status.HTTP_403_FORBIDDEN)

        car.is_deleted = True
        car.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CarByModelView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        model_id = request.query_params.get('model_id')
        if not model_id:
            return Response({'error': 'model_id required'}, status=status.HTTP_400_BAD_REQUEST)

        cars = Car.objects.filter(model_id=model_id, is_deleted=False).select_related('model', 'seller')
        serializer = CarListSerializer(cars, many=True)
        return Response(serializer.data)


class MyCarListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cars = Car.objects.filter(seller=request.user, is_deleted=False).select_related('model', 'seller')
        serializer = CarListSerializer(cars, many=True)
        return Response(serializer.data)
