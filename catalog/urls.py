from django.urls import path
from catalog.views import (
    BrandListAPIView, BrandDetailAPIView,
    ModelListAPIView, ModelDetailAPIView, ModelByBrandAPIView
)

urlpatterns = [
    path('brands/', BrandListAPIView.as_view(), name='brand-list'),
    path('brands/<int:brand_id>/', BrandDetailAPIView.as_view(), name='brand-detail'),
    path('models/', ModelListAPIView.as_view(), name='model-list'),
    path('models/<int:model_id>/', ModelDetailAPIView.as_view(), name='model-detail'),
    path('models/by-brand/', ModelByBrandAPIView.as_view(), name='model-by-brand'),
]

