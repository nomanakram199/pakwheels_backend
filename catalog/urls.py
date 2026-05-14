from django.urls import path
from .views import (
    BrandListView, BrandDetailView,
    ModelListView, ModelDetailView, ModelByBrandView
)

urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('brands/<int:brand_id>/', BrandDetailView.as_view(), name='brand-detail'),
    path('models/', ModelListView.as_view(), name='model-list'),
    path('models/<int:model_id>/', ModelDetailView.as_view(), name='model-detail'),
    path('models/by-brand/', ModelByBrandView.as_view(), name='model-by-brand'),
]
