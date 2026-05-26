from django.db import IntegrityError
from django.test import TestCase

from cars.factories import BrandFactory, CarModelFactory
from cars.models import Brand, CarModel

class BrandTestCase(TestCase):
    def setUp(self):
        self.brand = BrandFactory(name='Toyota')

    def test_brand_creation(self):
        self.assertEqual(self.brand.name, 'Toyota')
        self.assertIsNotNone(self.brand.created)
        self.assertIsNotNone(self.brand.modified)

    def test_brand_unique_name(self):
        with self.assertRaises(IntegrityError):
            BrandFactory(name='Toyota')


class CarModelTestCase(TestCase):
    def setUp(self):
        self.brand = BrandFactory(name='Honda')
        self.car_model = CarModelFactory(brand=self.brand, name='Civic')

    def test_car_model_creation(self):
        self.assertEqual(self.car_model.name, 'Civic')
        self.assertEqual(self.car_model.brand.name, 'Honda')
        self.assertIsNotNone(self.car_model.created)
        self.assertIsNotNone(self.car_model.modified)

    def test_car_model_unique_per_brand(self):
        with self.assertRaises(IntegrityError):
            CarModelFactory(brand=self.brand, name='Civic')


class BrandListAPITestCase(TestCase):
    def setUp(self):
        BrandFactory(name='Toyota')
        BrandFactory(name='Honda')

    def test_brand_list_api_success(self):
        with self.assertNumQueries(1):
            response = self.client.get('/api/v1/cars/brands/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 2)

    def test_brand_list_api_empty(self):
        Brand.objects.all().delete()
        with self.assertNumQueries(1):
            response = self.client.get('/api/v1/cars/brands/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_brand_search_by_name(self):
        with self.assertNumQueries(1):
            response = self.client.get('/api/v1/cars/brands/?search=toyota')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Toyota')

    def test_brand_search_case_insensitive(self):
        with self.assertNumQueries(1):
            response = self.client.get('/api/v1/cars/brands/?search=HONDA')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Honda')

    def test_brand_search_no_results(self):
            with self.assertNumQueries(1):
                response = self.client.get('/api/v1/cars/brands/?search=BMW')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()), 0)


class CarModelListAPITestCase(TestCase):
    def setUp(self):
        self.brand = BrandFactory(name='Toyota')
        CarModelFactory(brand=self.brand, name='Corolla')
        CarModelFactory(brand=self.brand, name='Yaris')

    def test_model_list_api_success(self):
        with self.assertNumQueries(1):
            response = self.client.get('/api/v1/cars/models/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 2)

    def test_model_list_api_empty(self):
        CarModel.objects.all().delete()
        with self.assertNumQueries(1):
            response = self.client.get('/api/v1/cars/models/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_model_filter_by_brand_success(self):
        with self.assertNumQueries(1):
            response = self.client.get(f'/api/v1/cars/models/?brand_id={self.brand.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 2)

    def test_model_filter_by_brand_no_results(self):
        other_brand = BrandFactory(name='Honda')
        with self.assertNumQueries(1):
            response = self.client.get(f'/api/v1/cars/models/?brand_id={other_brand.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_model_filter_by_invalid_brand(self):
        with self.assertNumQueries(1):
            response = self.client.get('/api/v1/cars/models/?brand_id=9999')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_model_search_by_name(self):
        with self.assertNumQueries(1):
            response = self.client.get('/api/v1/cars/models/?search=corolla')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Corolla')

    def test_model_search_case_insensitive(self):
        with self.assertNumQueries(1):
            response = self.client.get('/api/v1/cars/models/?search=YARIS')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Yaris')

    def test_model_search_no_results(self):
            with self.assertNumQueries(1):
            response = self.client.get('/api/v1/cars/models/?search=Civic')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_model_search_with_brand_filter(self):
        other_brand = BrandFactory(name='Honda')
        CarModelFactory(brand=other_brand, name='Civic')
        with self.assertNumQueries(1):
            response = self.client.get(f'/api/v1/cars/models/?brand_id={self.brand.id}&search=corolla')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Corolla')
