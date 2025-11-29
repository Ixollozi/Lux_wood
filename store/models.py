from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta


class SlugMixin:
    """Миксин для автоматической генерации slug"""
    def generate_unique_slug(self, base_slug, model_class):
        """Генерирует уникальный slug"""
        slug = base_slug
        counter = 1
        while model_class.objects.filter(slug=slug).exclude(pk=self.pk if self.pk else None).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug


class Category(SlugMixin, models.Model):
    name = models.CharField(max_length=200, verbose_name='Название', db_index=True)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name='Изображение')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='Родительская категория', db_index=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = self.generate_unique_slug(base_slug, Category)
        super().save(*args, **kwargs)


class Product(SlugMixin, models.Model):
    name = models.CharField(max_length=300, verbose_name='Название', db_index=True)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', db_index=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Старая цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория', db_index=True)
    image = models.ImageField(upload_to='products/', verbose_name='Основное изображение')
    stock = models.IntegerField(default=0, verbose_name='Остаток на складе', db_index=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Рейтинг', db_index=True)
    reviews_count = models.IntegerField(default=0, verbose_name='Количество отзывов')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    featured = models.BooleanField(default=False, verbose_name='Рекомендуемый', db_index=True)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', 'featured']),
            models.Index(fields=['-rating', '-reviews_count']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['stock']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = self.generate_unique_slug(base_slug, Product)
        super().save(*args, **kwargs)
    
    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0
    
    @property
    def is_in_stock(self):
        """Проверка наличия товара"""
        return self.stock > 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар', db_index=True)
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    
    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        indexes = [
            models.Index(fields=['product']),
        ]


class Cart(models.Model):
    session_key = models.CharField(max_length=40, verbose_name='Ключ сессии', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        indexes = [
            models.Index(fields=['session_key']),
            models.Index(fields=['updated_at']),
        ]
        # Убираем unique, так как один пользователь может иметь несколько корзин (например, при очистке старых)
    
    def __str__(self):
        return f'Корзина {self.session_key[:20]}...'
    
    @property
    def total_price(self):
        """Общая стоимость корзины"""
        return sum(item.total_price for item in self.items.all())
    
    @property
    def total_items(self):
        """Общее количество товаров в корзине"""
        return sum(item.quantity for item in self.items.all())
    
    def is_empty(self):
        """Проверка, пуста ли корзина"""
        return self.items.count() == 0
    
    def is_expired(self):
        """Проверка, истекла ли корзина (старше 30 дней)"""
        expiration_date = timezone.now() - timedelta(days=30)
        return self.updated_at < expiration_date
    
    @classmethod
    def cleanup_old_carts(cls, days=30):
        """Удаляет корзины, которые не обновлялись более указанного количества дней"""
        expiration_date = timezone.now() - timedelta(days=days)
        old_carts = cls.objects.filter(updated_at__lt=expiration_date)
        count = old_carts.count()
        old_carts.delete()
        return count


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина', db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', db_index=True)
    quantity = models.IntegerField(default=1, verbose_name='Количество')
    
    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = [['cart', 'product']]
        indexes = [
            models.Index(fields=['cart', 'product']),
        ]
    
    def __str__(self):
        return f'{self.product.name} x{self.quantity}'
    
    @property
    def total_price(self):
        """Общая стоимость позиции"""
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    
    session_key = models.CharField(max_length=40, verbose_name='Ключ сессии', db_index=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email', db_index=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', db_index=True)
    address = models.TextField(verbose_name='Адрес')
    city = models.CharField(max_length=100, verbose_name='Город', db_index=True)
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый индекс', blank=True)
    comment = models.TextField(blank=True, verbose_name='Комментарий к заказу')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус', db_index=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_index=True)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
        ]
    
    def __str__(self):
        return f'Заказ #{self.id} - {self.first_name} {self.last_name}'
    
    @property
    def full_name(self):
        """Полное имя клиента"""
        return f'{self.first_name} {self.last_name}'
    
    @property
    def items_count(self):
        """Количество товаров в заказе"""
        return self.items.count()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ', db_index=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар', db_index=True)
    quantity = models.IntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    
    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
        indexes = [
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        return f'{self.product.name} x{self.quantity}'
    
    @property
    def total_price(self):
        """Общая стоимость позиции"""
        return self.price * self.quantity


class ProductAttribute(models.Model):
    """Характеристики товара"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes', verbose_name='Товар', db_index=True)
    name = models.CharField(max_length=200, verbose_name='Название характеристики')
    value = models.CharField(max_length=500, verbose_name='Значение')
    order = models.IntegerField(default=0, verbose_name='Порядок отображения', db_index=True)
    
    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товаров'
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['product', 'order']),
        ]
    
    def __str__(self):
        return f'{self.product.name} - {self.name}: {self.value}'


class Banner(models.Model):
    """Баннеры для главной страницы"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='banners/', verbose_name='Изображение')
    link = models.URLField(blank=True, null=True, verbose_name='Ссылка')
    order = models.IntegerField(default=0, verbose_name='Порядок отображения', db_index=True)
    is_active = models.BooleanField(default=True, verbose_name='Активен', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['is_active', 'order']),
        ]
    
    def __str__(self):
        return self.title


class Sponsor(models.Model):
    """Спонсоры/партнеры"""
    name = models.CharField(max_length=200, verbose_name='Название')
    logo = models.ImageField(upload_to='sponsors/', verbose_name='Логотип')
    website = models.URLField(blank=True, null=True, verbose_name='Сайт')
    order = models.IntegerField(default=0, verbose_name='Порядок отображения', db_index=True)
    is_active = models.BooleanField(default=True, verbose_name='Активен', db_index=True)
    
    class Meta:
        verbose_name = 'Спонсор'
        verbose_name_plural = 'Спонсоры'
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['is_active', 'order']),
        ]
    
    def __str__(self):
        return self.name


class FAQCategory(models.Model):
    """Категории FAQ"""
    name = models.CharField(max_length=200, verbose_name='Название')
    order = models.IntegerField(default=0, verbose_name='Порядок отображения', db_index=True)
    
    class Meta:
        verbose_name = 'Категория FAQ'
        verbose_name_plural = 'Категории FAQ'
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        return self.name


class FAQ(models.Model):
    """Часто задаваемые вопросы"""
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs', verbose_name='Категория', null=True, blank=True, db_index=True)
    question = models.CharField(max_length=500, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    order = models.IntegerField(default=0, verbose_name='Порядок отображения', db_index=True)
    is_active = models.BooleanField(default=True, verbose_name='Активен', db_index=True)
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['order', 'question']
        indexes = [
            models.Index(fields=['category', 'is_active', 'order']),
        ]
    
    def __str__(self):
        return self.question


class CompanyInfo(models.Model):
    """Информация о компании (singleton)"""
    name = models.CharField(max_length=200, verbose_name='Название компании', default='LuxWood')
    logo = models.ImageField(upload_to='company/', blank=True, null=True, verbose_name='Логотип')
    about_text = models.TextField(blank=True, default='', verbose_name='Текст о компании')
    mission = models.TextField(blank=True, verbose_name='Миссия')
    values = models.TextField(blank=True, verbose_name='Ценности')
    history = models.TextField(blank=True, verbose_name='История')
    email = models.EmailField(verbose_name='Email', default='info@luxwood.com')
    phone = models.CharField(max_length=20, verbose_name='Телефон', default='+7 (999) 123-45-67')
    address = models.TextField(blank=True, default='', verbose_name='Адрес')
    city = models.CharField(max_length=100, verbose_name='Город', default='Москва')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='Почтовый индекс')
    working_hours = models.CharField(max_length=200, verbose_name='График работы', default='Пн-Пт: 9:00 - 18:00')
    map_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на карту')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Долгота')
    facebook = models.URLField(blank=True, null=True, verbose_name='Facebook')
    instagram = models.URLField(blank=True, null=True, verbose_name='Instagram')
    twitter = models.URLField(blank=True, null=True, verbose_name='Twitter')
    telegram = models.URLField(blank=True, null=True, verbose_name='Telegram')
    
    class Meta:
        verbose_name = 'Информация о компании'
        verbose_name_plural = 'Информация о компании'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Обеспечиваем, что существует только одна запись
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        """Загружает или создает единственную запись"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Advantage(models.Model):
    """Преимущества компании (Почему выбирают нас)"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    icon = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name='Иконка (Font Awesome класс)', 
        default='fas fa-star',
        help_text='Примеры: fas fa-star, fas fa-shipping-fast, fas fa-shield-alt, fas fa-headset, fas fa-trophy, fas fa-gift, fas fa-clock, fas fa-check-circle'
    )
    order = models.IntegerField(default=0, verbose_name='Порядок отображения', db_index=True)
    is_active = models.BooleanField(default=True, verbose_name='Активен', db_index=True)
    
    class Meta:
        verbose_name = 'Преимущество'
        verbose_name_plural = 'Преимущества'
        ordering = ['order', 'title']
        indexes = [
            models.Index(fields=['is_active', 'order']),
        ]
    
    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Сообщения из формы обратной связи"""
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email', db_index=True)
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    subject = models.CharField(max_length=200, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_index=True)
    is_read = models.BooleanField(default=False, verbose_name='Прочитано', db_index=True)
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_read']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f'{self.name} - {self.subject}'
    
    def mark_as_read(self):
        """Пометить сообщение как прочитанное"""
        self.is_read = True
        self.save(update_fields=['is_read'])
