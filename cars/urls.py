from django.urls import path

from cars.views import (
    BrandListAPIView,
    CarImageUploadAPIView,
    CarListCreateAPIView,
    CarRetrieveUpdateDestroyAPIView,
    MyCarListAPIView,
    ModelListAPIView,
)

urlpatterns = [
    path('brands/', BrandListAPIView.as_view(), name='brand_list'),
    path('models/', ModelListAPIView.as_view(), name='model_list'),
    path('my/', MyCarListAPIView.as_view(), name='my_car_list'),
    path('', CarListCreateAPIView.as_view(), name='car_list_create'),
    path('<int:pk>/images/', CarImageUploadAPIView.as_view(), name='car_image_upload'),
    path('<int:pk>/', CarRetrieveUpdateDestroyAPIView.as_view(), name='car_detail'),
]
