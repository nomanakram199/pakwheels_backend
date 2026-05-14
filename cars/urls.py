from django.urls import path
from .views import CarListView, CarDetailView, CarByModelView, MyCarListView

urlpatterns = [
    path('', CarListView.as_view(), name='car-list'),
    path('<int:car_id>/', CarDetailView.as_view(), name='car-detail'),
    path('by-model/', CarByModelView.as_view(), name='car-by-model'),
    path('my-cars/', MyCarListView.as_view(), name='my-cars'),
]
