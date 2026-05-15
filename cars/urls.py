from django.urls import path
from cars.views import CarListAPIView, CarDetailAPIView, CarByModelAPIView, MyCarListAPIView

urlpatterns = [
    path('', CarListAPIView.as_view(), name='car-list'),
    path('<int:car_id>/', CarDetailAPIView.as_view(), name='car-detail'),
    path('by-model/', CarByModelAPIView.as_view(), name='car-by-model'),
    path('my-cars/', MyCarListAPIView.as_view(), name='my-cars'),
]

