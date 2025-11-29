from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Исправляет пустые slug у категорий и товаров'

    def handle(self, *args, **options):
        self.stdout.write('Исправление slug...')
        
        # Исправляем категории
        categories = Category.objects.filter(slug='')
        count = 0
        for category in categories:
            category.save()  # Это вызовет метод save, который сгенерирует slug
            count += 1
            self.stdout.write(f'Исправлен slug для категории: {category.name}')
        
        self.stdout.write(f'Исправлено категорий: {count}')
        
        # Исправляем товары
        products = Product.objects.filter(slug='') | Product.objects.filter(slug__isnull=True)
        count = 0
        for product in products:
            # Принудительно генерируем slug
            if not product.slug:
                from django.utils.text import slugify
                base_slug = slugify(product.name)
                slug = base_slug
                counter = 1
                while Product.objects.filter(slug=slug).exclude(pk=product.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                product.slug = slug
                product.save(update_fields=['slug'])
                count += 1
                self.stdout.write(f'Исправлен slug для товара: {product.name}')
        
        self.stdout.write(f'Исправлено товаров: {count}')
        self.stdout.write(self.style.SUCCESS('Готово! Все slug исправлены.'))

