from django.core.management.base import BaseCommand
from cars.models import Brand, CarModel

class Command(BaseCommand):
    help = 'Seed the database with car brands and models'
    def handle(self, *args, **kwargs):

       data={
        'toyota':["Corolla", "Yaris"],
        'honda':["Civic", "BRV"],
        'suzuki':["Alto", "Mehran"],
        'daihatsu':["Mira"],
        'nissan':["Leaf"],
       }

       for brand_name, models in data.items():
           brand, created = Brand.objects.get_or_create(name=brand_name)
           for model_name in models:
                CarModel.objects.get_or_create(brand=brand, name=model_name)

       self.stdout.write(self.style.SUCCESS('Successfully seeded car brands and models'))
