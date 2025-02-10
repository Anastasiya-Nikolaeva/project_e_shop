from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Load test data for products and categories'

    def handle(self, *args, **kwargs):
        # Удаляем все существующие данные
        self.stdout.write(self.style.WARNING('Deleting existing data...'))
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Loading fixtures...'))
        call_command('loaddata', 'categories_products.json')  # Замените на имя вашего файла

        self.stdout.write(self.style.SUCCESS('Successfully loaded test data'))
