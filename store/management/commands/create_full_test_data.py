from django.core.management.base import BaseCommand
from store.models import (
    Category, Product, ProductAttribute, ProductImage,
    Banner, Sponsor, FAQCategory, FAQ,
    CompanyInfo, Advantage, ContactMessage
)
from decimal import Decimal
import os
from django.core.files import File
from PIL import Image
import io


class Command(BaseCommand):
    help = 'Создает полные тестовые данные для всех моделей магазина'

    def create_image_file(self, width=800, height=600, color=(200, 200, 200), text=''):
        """Создает тестовое изображение"""
        img = Image.new('RGB', (width, height), color=color)
        if text:
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            # Центрируем текст
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((width - text_width) // 2, (height - text_height) // 2)
            draw.text(position, text, fill=(100, 100, 100), font=font)
        
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        return File(img_io, name=f'test_{text.replace(" ", "_")}.jpg')

    def handle(self, *args, **options):
        self.stdout.write('Создание полных тестовых данных...')
        
        # 1. CompanyInfo
        self.stdout.write('Создание информации о компании...')
        try:
            company_info = CompanyInfo.objects.get(pk=1)
            created = False
            self.stdout.write('Информация о компании уже существует, обновляю...')
        except CompanyInfo.DoesNotExist:
            company_info = CompanyInfo()
            company_info.pk = 1
            created = True
        
        if created or not company_info.logo:
            company_info.name = 'Мебельный Дом "Комфорт"'
            company_info.about_text = 'Мы - ведущий интернет-магазин мебели и товаров для дома. Работаем с 2010 года, предлагая качественную продукцию по доступным ценам. Наша миссия - сделать ваш дом уютным и комфортным.'
            company_info.mission = 'Предоставлять качественную мебель и товары для дома, создавая комфорт и уют в каждом доме.'
            company_info.values = 'Качество, Надежность, Клиентоориентированность, Инновации'
            company_info.history = 'Основанная в 2010 году, наша компания выросла из небольшого магазина в крупный интернет-ритейлер. Мы гордимся тем, что обслужили более 100,000 довольных клиентов.'
            company_info.email = 'info@mebel-comfort.ru'
            company_info.phone = '+7 (495) 123-45-67'
            company_info.address = 'г. Москва, ул. Торговая, д. 15, офис 201'
            company_info.city = 'Москва'
            company_info.postal_code = '123456'
            company_info.working_hours = 'Пн-Пт: 9:00 - 20:00, Сб-Вс: 10:00 - 18:00'
            company_info.map_url = 'https://yandex.ru/maps/-/CCUqMZqH0C'
            company_info.latitude = Decimal('55.7558')
            company_info.longitude = Decimal('37.6173')
            company_info.facebook = 'https://facebook.com/mebel-comfort'
            company_info.instagram = 'https://instagram.com/mebel_comfort'
            company_info.twitter = 'https://twitter.com/mebel_comfort'
            company_info.telegram = 'https://t.me/mebel_comfort'
            
            if not company_info.logo:
                # Создаем логотип
                logo_file = self.create_image_file(400, 200, (40, 167, 69), 'LOGO')
                company_info.logo.save('company_logo.jpg', logo_file, save=False)
            
            company_info.save()
            self.stdout.write(self.style.SUCCESS('✓ Информация о компании создана/обновлена'))

        # 2. Banners
        self.stdout.write('Создание баннеров...')
        banners_data = [
            {
                'title': 'Новинки сезона',
                'description': 'Скидки до 50% на новую коллекцию мебели',
                'color': (255, 100, 100),
                'text': 'НОВИНКИ -50%'
            },
            {
                'title': 'Распродажа',
                'description': 'Большая распродажа мебели и товаров для дома',
                'color': (100, 150, 255),
                'text': 'РАСПРОДАЖА'
            },
            {
                'title': 'Бесплатная доставка',
                'description': 'Бесплатная доставка при заказе от 5000₽',
                'color': (100, 255, 150),
                'text': 'БЕСПЛАТНАЯ ДОСТАВКА'
            },
        ]
        
        Banner.objects.all().delete()
        for i, banner_data in enumerate(banners_data):
            banner = Banner.objects.create(
                title=banner_data['title'],
                description=banner_data['description'],
                order=i,
                is_active=True
            )
            banner_image = self.create_image_file(1200, 400, banner_data['color'], banner_data['text'])
            banner.image.save(f'banner_{i+1}.jpg', banner_image, save=True)
            self.stdout.write(f'✓ Создан баннер: {banner_data["title"]}')

        # 3. Sponsors
        self.stdout.write('Создание спонсоров...')
        sponsors_data = [
            {'name': 'IKEA', 'website': 'https://www.ikea.com'},
            {'name': 'Леруа Мерлен', 'website': 'https://leroymerlin.ru'},
            {'name': 'OBI', 'website': 'https://www.obi.ru'},
            {'name': 'Castorama', 'website': 'https://www.castorama.ru'},
            {'name': 'Мебель России', 'website': 'https://mebel-russia.ru'},
        ]
        
        Sponsor.objects.all().delete()
        for i, sponsor_data in enumerate(sponsors_data):
            sponsor = Sponsor.objects.create(
                name=sponsor_data['name'],
                website=sponsor_data['website'],
                order=i,
                is_active=True
            )
            logo_image = self.create_image_file(200, 100, (240, 240, 240), sponsor_data['name'])
            sponsor.logo.save(f'sponsor_{sponsor_data["name"].lower().replace(" ", "_")}.jpg', logo_image, save=True)
            self.stdout.write(f'✓ Создан спонсор: {sponsor_data["name"]}')

        # 4. Advantages
        self.stdout.write('Создание преимуществ...')
        advantages_data = [
            {
                'title': 'Быстрая доставка',
                'description': 'Доставляем заказы по всей стране в течение 3-5 дней',
                'icon': 'fas fa-shipping-fast'
            },
            {
                'title': 'Гарантия качества',
                'description': 'Все товары проходят строгий контроль качества перед отправкой',
                'icon': 'fas fa-shield-alt'
            },
            {
                'title': 'Лучшие цены',
                'description': 'Предлагаем конкурентные цены и регулярные акции',
                'icon': 'fas fa-tags'
            },
            {
                'title': 'Профессиональная поддержка',
                'description': 'Наша служба поддержки работает 24/7 для вашего удобства',
                'icon': 'fas fa-headset'
            },
            {
                'title': 'Широкий ассортимент',
                'description': 'Более 10,000 товаров в каталоге на любой вкус и бюджет',
                'icon': 'fas fa-boxes'
            },
            {
                'title': 'Удобная оплата',
                'description': 'Принимаем различные способы оплаты, включая рассрочку',
                'icon': 'fas fa-credit-card'
            },
        ]
        
        Advantage.objects.all().delete()
        for i, adv_data in enumerate(advantages_data):
            Advantage.objects.create(
                title=adv_data['title'],
                description=adv_data['description'],
                icon=adv_data['icon'],
                order=i,
                is_active=True
            )
            self.stdout.write(f'✓ Создано преимущество: {adv_data["title"]}')

        # 5. FAQ Categories
        self.stdout.write('Создание категорий FAQ...')
        faq_categories_data = [
            {'name': 'Доставка', 'order': 0},
            {'name': 'Оплата', 'order': 1},
            {'name': 'Гарантия и возврат', 'order': 2},
            {'name': 'О компании', 'order': 3},
        ]
        
        faq_categories = {}
        FAQCategory.objects.all().delete()
        for cat_data in faq_categories_data:
            category = FAQCategory.objects.create(
                name=cat_data['name'],
                order=cat_data['order']
            )
            faq_categories[cat_data['name']] = category
            self.stdout.write(f'✓ Создана категория FAQ: {cat_data["name"]}')

        # 6. FAQ
        self.stdout.write('Создание вопросов FAQ...')
        faqs_data = [
            {
                'category': 'Доставка',
                'question': 'Как осуществляется доставка?',
                'answer': 'Доставка осуществляется курьерской службой по всей России. В крупных городах возможна доставка в день заказа. Стоимость доставки рассчитывается индивидуально в зависимости от веса и габаритов товара.',
                'order': 0
            },
            {
                'category': 'Доставка',
                'question': 'Сколько стоит доставка?',
                'answer': 'При заказе от 5000₽ доставка бесплатная. Для заказов на меньшую сумму стоимость доставки составляет от 300₽ в зависимости от региона и веса товара.',
                'order': 1
            },
            {
                'category': 'Доставка',
                'question': 'Сколько времени занимает доставка?',
                'answer': 'В Москве и Санкт-Петербурге доставка занимает 1-2 дня. В другие города России - 3-7 дней в зависимости от удаленности региона.',
                'order': 2
            },
            {
                'category': 'Оплата',
                'question': 'Какие способы оплаты вы принимаете?',
                'answer': 'Мы принимаем оплату банковскими картами (Visa, MasterCard, МИР), наличными курьеру, банковским переводом, а также предоставляем возможность оплаты в рассрочку.',
                'order': 0
            },
            {
                'category': 'Оплата',
                'question': 'Безопасна ли оплата картой?',
                'answer': 'Да, все платежи обрабатываются через защищенный платежный шлюз. Мы не храним данные ваших банковских карт.',
                'order': 1
            },
            {
                'category': 'Гарантия и возврат',
                'question': 'Какой срок гарантии на товары?',
                'answer': 'Гарантийный срок зависит от категории товара. На мебель предоставляется гарантия от 12 до 24 месяцев. Подробную информацию о гарантии вы найдете в описании каждого товара.',
                'order': 0
            },
            {
                'category': 'Гарантия и возврат',
                'question': 'Можно ли вернуть товар?',
                'answer': 'Да, в соответствии с законом о защите прав потребителей, вы можете вернуть товар надлежащего качества в течение 14 дней с момента покупки, если он не подошел по форме, габаритам или другим параметрам.',
                'order': 1
            },
            {
                'category': 'О компании',
                'question': 'Как давно вы работаете?',
                'answer': 'Наша компания работает с 2010 года. За это время мы обслужили более 100,000 довольных клиентов и зарекомендовали себя как надежный поставщик качественной мебели и товаров для дома.',
                'order': 0
            },
        ]
        
        FAQ.objects.all().delete()
        for faq_data in faqs_data:
            FAQ.objects.create(
                category=faq_categories[faq_data['category']],
                question=faq_data['question'],
                answer=faq_data['answer'],
                order=faq_data['order'],
                is_active=True
            )
            self.stdout.write(f'✓ Создан вопрос FAQ: {faq_data["question"][:50]}...')

        # 7. Product Attributes (для существующих товаров)
        self.stdout.write('Создание характеристик товаров...')
        products = Product.objects.all()[:10]  # Берем первые 10 товаров
        
        # Общие характеристики для разных категорий
        attributes_templates = {
            'обогреватель': [
                {'name': 'Мощность', 'value': '900W'},
                {'name': 'Площадь обогрева', 'value': 'до 20 м²'},
                {'name': 'Тип', 'value': 'Электрический'},
                {'name': 'Уровень шума', 'value': 'Низкий'},
            ],
            'бритва': [
                {'name': 'Тип', 'value': 'Электрическая'},
                {'name': 'Количество лезвий', 'value': '3'},
                {'name': 'Водонепроницаемость', 'value': 'Да'},
                {'name': 'Время работы', 'value': 'до 60 минут'},
            ],
            'мультиварка': [
                {'name': 'Объем', 'value': '5 литров'},
                {'name': 'Мощность', 'value': '900W'},
                {'name': 'Количество программ', 'value': '12'},
                {'name': 'Материал чаши', 'value': 'Антипригарное покрытие'},
            ],
            'смартфон': [
                {'name': 'Память', 'value': '128GB'},
                {'name': 'Экран', 'value': '6.5" Full HD'},
                {'name': 'Камера', 'value': '48 МП'},
                {'name': 'Батарея', 'value': '4000 мАч'},
            ],
        }
        
        ProductAttribute.objects.all().delete()
        for product in products:
            # Определяем тип товара по названию
            product_type = None
            for key in attributes_templates.keys():
                if key.lower() in product.name.lower():
                    product_type = key
                    break
            
            if product_type:
                attributes = attributes_templates[product_type]
            else:
                # Общие характеристики по умолчанию
                attributes = [
                    {'name': 'Материал', 'value': 'Высококачественный'},
                    {'name': 'Гарантия', 'value': '12 месяцев'},
                    {'name': 'Страна производства', 'value': 'Россия'},
                ]
            
            for i, attr_data in enumerate(attributes):
                ProductAttribute.objects.create(
                    product=product,
                    name=attr_data['name'],
                    value=attr_data['value'],
                    order=i
                )
            self.stdout.write(f'✓ Добавлены характеристики для: {product.name}')

        # 8. Product Images (дополнительные изображения для товаров)
        self.stdout.write('Создание дополнительных изображений товаров...')
        products_with_images = Product.objects.all()[:10]  # Для первых 10 товаров
        
        for product in products_with_images:
            # Создаем 2 дополнительных изображения, если их еще нет
            existing_images_count = product.images.count()
            if existing_images_count < 2:
                for i in range(2 - existing_images_count):
                    img_file = self.create_image_file(800, 600, (220, 220, 220), f'{product.name[:15]} {i+1}')
                    ProductImage.objects.create(
                        product=product,
                        image=img_file
                    )
                self.stdout.write(f'✓ Добавлены изображения для: {product.name}')

        # 9. Contact Messages (тестовые сообщения)
        self.stdout.write('Создание тестовых сообщений...')
        messages_data = [
            {
                'name': 'Иван Петров',
                'email': 'ivan@example.com',
                'phone': '+7 (999) 111-22-33',
                'subject': 'Вопрос о доставке',
                'message': 'Здравствуйте! Хотел бы узнать, возможна ли доставка в мой город?'
            },
            {
                'name': 'Мария Сидорова',
                'email': 'maria@example.com',
                'phone': '+7 (999) 222-33-44',
                'subject': 'Гарантия на товар',
                'message': 'Интересует информация о гарантийном обслуживании.'
            },
            {
                'name': 'Алексей Иванов',
                'email': 'alex@example.com',
                'phone': '',
                'subject': 'Сотрудничество',
                'message': 'Хотел бы обсудить возможность сотрудничества.'
            },
        ]
        
        ContactMessage.objects.all().delete()
        for msg_data in messages_data:
            ContactMessage.objects.create(**msg_data)
            self.stdout.write(f'✓ Создано сообщение от: {msg_data["name"]}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('✓ Все тестовые данные успешно созданы!'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        self.stdout.write('Создано:')
        self.stdout.write(f'  - Информация о компании: 1')
        self.stdout.write(f'  - Баннеры: {Banner.objects.count()}')
        self.stdout.write(f'  - Спонсоры: {Sponsor.objects.count()}')
        self.stdout.write(f'  - Преимущества: {Advantage.objects.count()}')
        self.stdout.write(f'  - Категории FAQ: {FAQCategory.objects.count()}')
        self.stdout.write(f'  - Вопросы FAQ: {FAQ.objects.count()}')
        self.stdout.write(f'  - Характеристики товаров: {ProductAttribute.objects.count()}')
        self.stdout.write(f'  - Дополнительные изображения: {ProductImage.objects.count()}')
        self.stdout.write(f'  - Сообщения: {ContactMessage.objects.count()}')
        self.stdout.write('')
        self.stdout.write('Теперь вы можете:')
        self.stdout.write('  1. Зайти в админ-панель и проверить созданные данные')
        self.stdout.write('  2. Добавить реальные изображения вместо тестовых')
        self.stdout.write('  3. Отредактировать информацию о компании')

