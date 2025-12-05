from django.core.management.base import BaseCommand
from store.models import Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Создает тестовые данные для магазина'

    def handle(self, *args, **options):
        self.stdout.write('Создание тестовых данных...')
        
        # Очистка существующих данных
        Product.objects.all().delete()
        Category.objects.all().delete()
        
        # Создание категорий
        categories_data = [
            {'name': 'Все для дома', 'children': ['Мебель', 'Текстиль', 'Освещение', 'Декор']},
            {'name': 'Красота', 'children': ['Косметика', 'Парфюмерия', 'Уход за кожей', 'Макияж']},
            {'name': 'Здоровье', 'children': ['Витамины', 'Медицинские приборы', 'Спорт', 'Здоровое питание']},
            {'name': 'Бытовая техника', 'children': ['Кухонная техника', 'Климатическая техника', 'Уборочная техника', 'Мелкая техника']},
            {'name': 'Смартфоны', 'children': ['Смартфоны', 'Аксессуары', 'Чехлы', 'Зарядные устройства']},
            {'name': 'Авто', 'children': ['Автозапчасти', 'Аксессуары', 'Инструменты', 'Уход за авто']},
            {'name': 'Ремонт', 'children': ['Инструменты', 'Крепеж', 'Электроинструменты', 'Расходные материалы']},
            {'name': 'Строительство', 'children': ['Материалы', 'Инструменты', 'Сантехника', 'Электрика']},
        ]
        
        categories = {}
        for cat_data in categories_data:
            parent, created = Category.objects.get_or_create(
                name_ru=cat_data['name'],
                defaults={'parent': None}
            )
            if created:
                categories[cat_data['name']] = parent
                self.stdout.write(f'Создана категория: {cat_data["name"]}')
            else:
                categories[cat_data['name']] = parent
            
            for child_name in cat_data['children']:
                # Используем уникальный ключ для дочерних категорий
                child_key = f"{cat_data['name']}_{child_name}"
                child, created = Category.objects.get_or_create(
                    name_ru=child_name,
                    parent=parent,
                    defaults={}
                )
                if created:
                    categories[child_key] = child
                else:
                    categories[child_key] = child
                # Также сохраняем по имени для обратной совместимости
                if child_name not in categories:
                    categories[child_name] = child
        
        # Тестовые товары
        products_data = [
            # Все для дома
            {'name': 'Портативный обогреватель 900W', 'category': 'Климатическая техника', 'price': 2490, 'old_price': 3290, 'description': 'Компактный обогреватель для дома и офиса. Быстрый нагрев, безопасность, тихая работа. Идеально для небольших помещений.', 'stock': 50, 'rating': 4.5, 'reviews': 128, 'featured': True},
            {'name': 'HANDY HEATER - Настенный обогреватель 400W', 'category': 'Климатическая техника', 'price': 1890, 'old_price': 2490, 'description': 'Инновационный обогреватель, подключается прямо в розетку. Экономичный и безопасный.', 'stock': 75, 'rating': 4.7, 'reviews': 256, 'featured': True},
            {'name': 'Круглый портативный обогреватель', 'category': 'Климатическая техника', 'price': 2190, 'old_price': 2990, 'description': 'Современный дизайн, быстрый нагрев, таймер на 12 часов, безопасность, низкий уровень шума.', 'stock': 30, 'rating': 4.6, 'reviews': 89, 'featured': True},
            
            # Красота
            {'name': 'Quick Hair Styler - Укладка волос', 'category': 'Косметика', 'price': 3490, 'old_price': 4490, 'description': 'Профессиональная укладка волос для мужчин и женщин. Быстрая и безопасная.', 'stock': 45, 'rating': 4.8, 'reviews': 342, 'featured': True},
            {'name': 'Электрическая бритва', 'category': 'Уход за кожей', 'price': 1290, 'old_price': 1790, 'description': 'Современная электрическая бритва с 3 лезвиями. Водонепроницаемая, удобная в использовании.', 'stock': 60, 'rating': 4.4, 'reviews': 156, 'featured': False},
            
            # Здоровье
            {'name': 'EMS стимулятор мышц живота', 'category': 'Спорт', 'price': 4490, 'old_price': 5990, 'description': 'Электростимуляция мышц для тренировки пресса, рук и других групп мышц. Профессиональный уровень.', 'stock': 25, 'rating': 4.3, 'reviews': 78, 'featured': True},
            
            # Бытовая техника
            {'name': 'Мультиварка 5 литров', 'category': 'Кухонная техника', 'price': 5490, 'old_price': 6990, 'description': 'Многофункциональная мультиварка с 12 программами. Автоматическое приготовление блюд.', 'stock': 40, 'rating': 4.9, 'reviews': 512, 'featured': True},
            {'name': 'Робот-пылесос с навигацией', 'category': 'Уборочная техника', 'price': 12990, 'old_price': 16990, 'description': 'Умный робот-пылесос с лазерной навигацией, влажная уборка, управление через приложение.', 'stock': 15, 'rating': 4.7, 'reviews': 234, 'featured': True},
            {'name': 'Электрический чайник 1.7л', 'category': 'Мелкая техника', 'price': 1290, 'old_price': 1790, 'description': 'Современный электрический чайник с подсветкой, автоматическое отключение, быстрый нагрев.', 'stock': 80, 'rating': 4.6, 'reviews': 189, 'featured': False},
            
            # Смартфоны
            {'name': 'Смартфон 128GB', 'category': 'Смартфоны', 'price': 24990, 'old_price': 29990, 'description': 'Современный смартфон с отличной камерой, быстрый процессор, большой экран.', 'stock': 20, 'rating': 4.8, 'reviews': 456, 'featured': True},
            {'name': 'Беспроводные наушники TWS', 'category': 'Аксессуары', 'price': 2490, 'old_price': 3490, 'description': 'Качественный звук, шумоподавление, автономность до 6 часов, стильный дизайн.', 'stock': 100, 'rating': 4.5, 'reviews': 678, 'featured': True},
            {'name': 'Чехол для смартфона с защитой', 'category': 'Чехлы', 'price': 490, 'old_price': 790, 'description': 'Надежная защита от ударов и царапин, стильный дизайн, точная посадка.', 'stock': 200, 'rating': 4.4, 'reviews': 234, 'featured': False},
            
            # Авто
            {'name': 'Автомобильный компрессор', 'category': 'Аксессуары', 'price': 2490, 'old_price': 3290, 'description': 'Портативный компрессор для подкачки шин. Работает от прикуривателя, компактный размер.', 'stock': 35, 'rating': 4.6, 'reviews': 123, 'featured': False},
            {'name': 'Автомобильный пылесос', 'category': 'Аксессуары', 'price': 1890, 'old_price': 2490, 'description': 'Мощный пылесос для автомобиля, работает от прикуривателя, комплект насадок.', 'stock': 50, 'rating': 4.3, 'reviews': 89, 'featured': False},
            
            # Ремонт
            {'name': 'Дрель-шуруповерт аккумуляторная', 'category': 'Электроинструменты', 'price': 4490, 'old_price': 5990, 'description': 'Мощная дрель-шуруповерт с аккумулятором, комплект бит, удобная рукоятка.', 'stock': 30, 'rating': 4.7, 'reviews': 167, 'featured': True},
            {'name': 'Набор инструментов 150 предметов', 'category': 'Инструменты', 'price': 3490, 'old_price': 4490, 'description': 'Полный набор инструментов для дома и ремонта. Все необходимое в одном кейсе.', 'stock': 25, 'rating': 4.5, 'reviews': 98, 'featured': False},
            
            # Строительство
            {'name': 'Перфоратор 800W', 'category': 'Инструменты', 'price': 5490, 'old_price': 6990, 'description': 'Мощный перфоратор для работы с бетоном и кирпичом. Регулировка скорости, комплект буров.', 'stock': 18, 'rating': 4.8, 'reviews': 201, 'featured': True},
            {'name': 'Лазерный уровень', 'category': 'Инструменты', 'price': 3490, 'old_price': 4490, 'description': 'Профессиональный лазерный уровень для точной разметки. Дальность до 30 метров.', 'stock': 22, 'rating': 4.6, 'reviews': 134, 'featured': False},
        ]
        
        # Создание товаров
        for prod_data in products_data:
            category_name = prod_data['category']
            # Сначала ищем по прямому имени
            category = categories.get(category_name)
            
            # Если не найдено, ищем по составному ключу (родитель_дочерний)
            if not category:
                for key, cat_obj in categories.items():
                    if key.endswith(f"_{category_name}"):
                        category = cat_obj
                        break
            
            # Если все еще не найдено, ищем по имени в базе данных
            if not category:
                try:
                    category = Category.objects.filter(name_ru=category_name).first()
                except:
                    pass
            
            # Если категория не найдена, используем первую доступную
            if not category:
                category = Category.objects.filter(parent=None).first()
                if not category:
                    category = Category.objects.first()
            
            product = Product.objects.create(
                name_ru=prod_data['name'],
                category=category,
                description_ru=prod_data['description'],
                price=Decimal(str(prod_data['price'])),
                old_price=Decimal(str(prod_data['old_price'])) if prod_data.get('old_price') else None,
                stock=prod_data['stock'],
                rating=Decimal(str(prod_data['rating'])),
                reviews_count=prod_data['reviews'],
                featured=prod_data.get('featured', False)
            )
            
            # Создаем простое изображение-заглушку (в реальности здесь можно загрузить реальные изображения)
            # Для теста создаем пустое изображение
            self.stdout.write(f'Создан товар: {prod_data["name"]}')
        
        self.stdout.write(self.style.SUCCESS(f'Успешно создано {len(products_data)} товаров!'))
        self.stdout.write('Тестовые данные созданы. Загрузите изображения товаров через админ-панель.')

