from django.urls import path
from cars.views import (
    BrandListAPIView,
    ModelListAPIView,
)

urlpatterns = [
    path('brands/', BrandListAPIView.as_view(), name='brand_list'),
    path('models/', ModelListAPIView.as_view(), name='model_list'),
]
