from django.test import TestCase
from cars.models import Brand, CarModel
# Create your tests here.

class BrandTestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Toyota')

    def test_brand_creation(self):
        self.assertEqual(self.brand.name, 'Toyota')
        self.assertIsNotNone(self.brand.created_at)
        self.assertIsNotNone(self.brand.updated_at)

    def test_brand_unique_name(self):
        with self.assertRaises(Exception):
            Brand.objects.create(name='Toyota')

class CarModelTestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Honda')
        self.car_model = CarModel.objects.create(
            brand=self.brand,
            name='Civic'
        )
    

    def test_car_model_creation(self):
        self.assertEqual(self.car_model.name, 'Civic')
        self.assertEqual(self.car_model.brand.name, 'Honda')
        self.assertIsNotNone(self.car_model.created_at)
        self.assertIsNotNone(self.car_model.updated_at) 

    def test_car_model_unique_per_brand(self):
        with self.assertRaises(Exception):
            CarModel.objects.create(brand=self.brand, name='Civic')

class BrandListAPITestCase(TestCase):
    def setUp(self):
        Brand.objects.create(name='Toyota')
        Brand.objects.create(name='Honda')

    def test_brand_list_api(self):
        response = self.client.get('/api/v1/cars/brands/')
        self.assertEqual(response.status_code, 200)

class CarModelListAPITestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Toyota')
        CarModel.objects.create(brand=self.brand, name='Corolla')
        CarModel.objects.create(brand=self.brand, name='Yaris')

    def test_model_list_api(self):
        response = self.client.get('/api/v1/cars/models/')
        self.assertEqual(response.status_code, 200)

    def test_model_filter_by_brand(self):
        response = self.client.get(f'/api/v1/cars/models/?brand_id={self.brand.id}')
        self.assertEqual(response.status_code, 200)
