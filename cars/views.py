
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from cars.models import Car
from catalog.models import Model as CarModel
from cars.serializers import CarListSerializer, CarDetailSerializer, CarCreateUpdateSerializer


def get_active_cars(filters=None):
    query = Car.objects.filter(is_deleted=False).select_related('model', 'seller')
    if filters:
        query = query.filter(**filters)
    return query


class CarListAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        cars = get_active_cars()
        serializer = CarListSerializer(cars, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CarCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarDetailAPIView(APIView):
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


class CarByModelAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        model_id = request.query_params.get('model_id')
        if not model_id:
            return Response({'error': 'model_id required'}, status=status.HTTP_400_BAD_REQUEST)

        if not CarModel.objects.filter(id=model_id).exists():
            raise NotFound("Model not found.")

        cars = get_active_cars({'model_id': model_id})
        serializer = CarListSerializer(cars, many=True)
        return Response(serializer.data)


class MyCarListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cars = get_active_cars({'seller': request.user})
        serializer = CarListSerializer(cars, many=True)
        return Response(serializer.data)


