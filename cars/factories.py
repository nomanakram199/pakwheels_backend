import factory

from cars.models import Brand, CarModel


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: f'Brand {n}')


class CarModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarModel

    brand = factory.SubFactory(BrandFactory)
    name = factory.Sequence(lambda n: f'Model {n}')
