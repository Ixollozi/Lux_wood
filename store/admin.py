from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Sum, Avg
from django.contrib import messages
from .models import (
    Category, Product, ProductImage, ProductAttribute,
    Cart, CartItem, Order, OrderItem,
    Banner, Sponsor, FAQCategory, FAQ,
    CompanyInfo, Advantage, ContactMessage
)


@admin.action(description='Пометить как прочитанные')
def mark_as_read(modeladmin, request, queryset):
    queryset.update(is_read=True)
    modeladmin.message_user(request, f'{queryset.count()} сообщений помечено как прочитанные.', messages.SUCCESS)


@admin.action(description='Пометить как непрочитанные')
def mark_as_unread(modeladmin, request, queryset):
    queryset.update(is_read=False)
    modeladmin.message_user(request, f'{queryset.count()} сообщений помечено как непрочитанные.', messages.SUCCESS)


@admin.action(description='Удалить корзины старше 30 дней')
def cleanup_old_carts_action(modeladmin, request, queryset):
    """Удаляет все корзины, которые не обновлялись более 30 дней"""
    from .models import Cart
    deleted_count = Cart.cleanup_old_carts(days=30)
    modeladmin.message_user(
        request, 
        f'Успешно удалено {deleted_count} корзин(ы), которые не обновлялись более 30 дней.', 
        messages.SUCCESS
    )


@admin.action(description='Активировать выбранные')
def activate_selected(modeladmin, request, queryset):
    queryset.update(is_active=True)
    modeladmin.message_user(request, f'{queryset.count()} элементов активировано.', messages.SUCCESS)


@admin.action(description='Деактивировать выбранные')
def deactivate_selected(modeladmin, request, queryset):
    queryset.update(is_active=False)
    modeladmin.message_user(request, f'{queryset.count()} элементов деактивировано.', messages.SUCCESS)


@admin.action(description='Пометить как рекомендуемые')
def mark_as_featured(modeladmin, request, queryset):
    queryset.update(featured=True)
    modeladmin.message_user(request, f'{queryset.count()} товаров помечено как рекомендуемые.', messages.SUCCESS)


@admin.action(description='Убрать из рекомендуемых')
def unmark_as_featured(modeladmin, request, queryset):
    queryset.update(featured=False)
    modeladmin.message_user(request, f'{queryset.count()} товаров убрано из рекомендуемых.', messages.SUCCESS)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_display', 'slug', 'parent', 'image_preview', 'products_count']
    list_filter = ['parent']
    search_fields = ['name_ru', 'name_en', 'name_uz']
    prepopulated_fields = {'slug': ('name_ru',)}
    ordering = ['name_ru']
    fieldsets = (
        ('Русский язык (RU)', {
            'fields': ('name_ru',)
        }),
        ('English (EN)', {
            'fields': ('name_en',),
            'classes': ('collapse',)
        }),
        ('O\'zbek (UZ)', {
            'fields': ('name_uz',),
            'classes': ('collapse',)
        }),
        ('Дополнительно', {
            'fields': ('slug', 'parent', 'image')
        }),
    )
    
    def name_display(self, obj):
        return format_html(
            '<strong>{}</strong><br>'
            '<span style="color: #666; font-size: 0.9em;">EN: {}</span><br>'
            '<span style="color: #666; font-size: 0.9em;">UZ: {}</span>',
            obj.name_ru,
            obj.name_en or '-',
            obj.name_uz or '-'
        )
    name_display.short_description = 'Название'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Изображение'
    
    def products_count(self, obj):
        count = obj.products.count()
        if count > 0:
            url = reverse('admin:store_product_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{}</a>', url, count)
        return 0
    products_count.short_description = 'Товаров'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return 'Изображение появится после сохранения'
    image_preview.short_description = 'Превью'


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1
    fields = ('name_ru', 'value_ru', 'order')
    verbose_name = 'Характеристика'
    verbose_name_plural = 'Характеристики'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name_display', 'category', 'price_display', 'stock', 'rating_display', 'featured_badge', 'created_at']
    list_filter = ['category', 'featured', 'created_at', 'stock']
    search_fields = ['name_ru', 'name_en', 'name_uz', 'description_ru', 'description_en', 'description_uz']
    prepopulated_fields = {'slug': ('name_ru',)}
    inlines = [ProductImageInline, ProductAttributeInline]
    ordering = ['-created_at']
    actions = [mark_as_featured, unmark_as_featured]
    list_per_page = 25
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Русский язык (RU)', {
            'fields': ('name_ru', 'description_ru')
        }),
        ('English (EN)', {
            'fields': ('name_en', 'description_en'),
            'classes': ('collapse',)
        }),
        ('O\'zbek (UZ)', {
            'fields': ('name_uz', 'description_uz'),
            'classes': ('collapse',)
        }),
        ('Основная информация', {
            'fields': ('slug', 'category', 'image', 'image_preview')
        }),
        ('Цены и наличие', {
            'fields': ('price', 'old_price', 'stock')
        }),
        ('Рейтинг и отзывы', {
            'fields': ('rating', 'reviews_count')
        }),
        ('Дополнительно', {
            'fields': ('featured',)
        }),
    )
    readonly_fields = ('image_preview',)
    
    def name_display(self, obj):
        return format_html(
            '<strong>{}</strong><br>'
            '<span style="color: #666; font-size: 0.85em;">EN: {}</span><br>'
            '<span style="color: #666; font-size: 0.85em;">UZ: {}</span>',
            obj.name_ru,
            obj.name_en or '-',
            obj.name_uz or '-'
        )
    name_display.short_description = 'Название'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px; max-width: 60px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Изображение'
    
    def price_display(self, obj):
        if obj.old_price:
            discount = obj.discount_percent
            return format_html(
                '<span style="color: #d32f2f; font-weight: bold;">{}  сум</span><br>'
                '<span style="color: #999; text-decoration: line-through; font-size: 0.9em;">{}  сум</span><br>'
                '<span style="color: #4caf50; font-size: 0.85em;">-{}%</span>',
                obj.price, obj.old_price, discount
            )
        return format_html('<span style="font-weight: bold;">{}  сум</span>', obj.price)
    price_display.short_description = 'Цена'
    
    def rating_display(self, obj):
        if obj.rating > 0:
            stars = '★' * int(obj.rating) + '☆' * (5 - int(obj.rating))
            return format_html(
                '<span style="color: #ffa726;">{}</span> {} ({})',
                stars, obj.rating, obj.reviews_count
            )
        return '-'
    rating_display.short_description = 'Рейтинг'
    
    def featured_badge(self, obj):
        if obj.featured:
            return format_html('<span style="background: #4caf50; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.85em;">★ Рекомендуемый</span>')
        return '-'
    featured_badge.short_description = 'Статус'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_key_short', 'total_items', 'total_price_display', 'created_at', 'updated_at']
    readonly_fields = ['session_key', 'created_at', 'updated_at', 'items_list']
    ordering = ['-created_at']
    list_per_page = 25
    actions = [cleanup_old_carts_action]
    list_filter = ['created_at', 'updated_at']
    
    def session_key_short(self, obj):
        return obj.session_key[:20] + '...' if len(obj.session_key) > 20 else obj.session_key
    session_key_short.short_description = 'Сессия'
    
    def total_price_display(self, obj):
        return format_html('<span style="font-weight: bold; color: #1976d2;">{}  сум</span>', obj.total_price)
    total_price_display.short_description = 'Сумма'
    
    def items_list(self, obj):
        items = obj.items.all()
        if items:
            html = '<ul style="margin: 0; padding-left: 20px;">'
            for item in items:
                html += f'<li>{item.product.get_name()} x{item.quantity} = {item.total_price} сум</li>'
            html += '</ul>'
            return format_html(html)
        return 'Корзина пуста'
    items_list.short_description = 'Товары'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'total_price_display']
    list_filter = ['cart']
    search_fields = ['product__name']
    
    def total_price_display(self, obj):
        return format_html('<span style="font-weight: bold;">{}  сум</span>', obj.total_price)
    total_price_display.short_description = 'Сумма'


@admin.action(description='Изменить статус на "В обработке"')
def set_processing(modeladmin, request, queryset):
    queryset.update(status='processing')
    modeladmin.message_user(request, f'{queryset.count()} заказов переведено в обработку.', messages.SUCCESS)


@admin.action(description='Изменить статус на "Отправлен"')
def set_shipped(modeladmin, request, queryset):
    queryset.update(status='shipped')
    modeladmin.message_user(request, f'{queryset.count()} заказов помечено как отправленные.', messages.SUCCESS)


@admin.action(description='Изменить статус на "Доставлен"')
def set_delivered(modeladmin, request, queryset):
    queryset.update(status='delivered')
    modeladmin.message_user(request, f'{queryset.count()} заказов помечено как доставленные.', messages.SUCCESS)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_info', 'contact_info', 'status_badge', 'total_price_display', 'items_count', 'created_at']
    list_filter = ['status', 'created_at', 'city']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'id']
    readonly_fields = ['created_at', 'items_list']
    ordering = ['-created_at']
    actions = [set_processing, set_shipped, set_delivered]
    list_per_page = 25
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('session_key', 'status', 'total_price', 'created_at', 'items_list')
        }),
        ('Данные получателя', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Адрес доставки', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('Комментарий', {
            'fields': ('comment',)
        }),
    )
    
    def customer_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><span style="color: #666;">{}</span>',
            f'{obj.first_name} {obj.last_name}',
            f'#{obj.id}'
        )
    customer_info.short_description = 'Клиент'
    
    def contact_info(self, obj):
        return format_html(
            '{}<br><span style="color: #666; font-size: 0.9em;">{}</span>',
            obj.email,
            obj.phone
        )
    contact_info.short_description = 'Контакты'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ff9800',
            'processing': '#2196f3',
            'shipped': '#9c27b0',
            'delivered': '#4caf50',
            'cancelled': '#f44336',
        }
        status_names = {
            'pending': 'Ожидает',
            'processing': 'В обработке',
            'shipped': 'Отправлен',
            'delivered': 'Доставлен',
            'cancelled': 'Отменен',
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.85em; font-weight: 500;">{}</span>',
            color, status_names.get(obj.status, obj.status)
        )
    status_badge.short_description = 'Статус'
    
    def total_price_display(self, obj):
        return format_html('<span style="font-weight: bold; color: #1976d2; font-size: 1.1em;">{}  сум</span>', obj.total_price)
    total_price_display.short_description = 'Сумма'
    
    def items_count(self, obj):
        count = obj.items.count()
        return format_html('<span style="color: #666;">{} шт.</span>', count)
    items_count.short_description = 'Товаров'
    
    def items_list(self, obj):
        items = obj.items.all()
        if items:
            html = '<div style="margin-top: 10px;"><strong>Товары в заказе:</strong><ul style="margin: 10px 0; padding-left: 20px;">'
            for item in items:
                html += f'<li>{item.product.get_name()} x{item.quantity} = {item.total_price} сум</li>'
            html += '</ul></div>'
            return format_html(html)
        return 'Нет товаров'
    items_list.short_description = 'Состав заказа'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order_link', 'product', 'quantity', 'price', 'total_price_display']
    list_filter = ['order']
    search_fields = ['product__name', 'order__id']
    
    def order_link(self, obj):
        url = reverse('admin:store_order_change', args=[obj.order.pk])
        return format_html('<a href="{}">Заказ #{}</a>', url, obj.order.id)
    order_link.short_description = 'Заказ'
    
    def total_price_display(self, obj):
        return format_html('<span style="font-weight: bold;">{}  сум</span>', obj.total_price)
    total_price_display.short_description = 'Сумма'


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'title_display', 'order', 'is_active_badge', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title_ru', 'title_en', 'title_uz', 'description_ru', 'description_en', 'description_uz']
    ordering = ['order', '-created_at']
    actions = [activate_selected, deactivate_selected]
    fieldsets = (
        ('Русский язык (RU)', {
            'fields': ('title_ru', 'description_ru')
        }),
        ('English (EN)', {
            'fields': ('title_en', 'description_en'),
            'classes': ('collapse',)
        }),
        ('O\'zbek (UZ)', {
            'fields': ('title_uz', 'description_uz'),
            'classes': ('collapse',)
        }),
        ('Дополнительно', {
            'fields': ('image', 'link', 'order', 'is_active')
        }),
    )
    
    def title_display(self, obj):
        return format_html(
            '<strong>{}</strong><br>'
            '<span style="color: #666; font-size: 0.85em;">EN: {}</span><br>'
            '<span style="color: #666; font-size: 0.85em;">UZ: {}</span>',
            obj.title_ru,
            obj.title_en or '-',
            obj.title_uz or '-'
        )
    title_display.short_description = 'Заголовок'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px; max-width: 100px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Изображение'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background: #4caf50; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.85em;">Активен</span>')
        return format_html('<span style="background: #999; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.85em;">Неактивен</span>')
    is_active_badge.short_description = 'Статус'


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['logo_preview', 'name_display', 'order', 'is_active_badge', 'website_link']
    list_filter = ['is_active']
    search_fields = ['name_ru', 'name_en', 'name_uz']
    ordering = ['order', 'name_ru']
    actions = [activate_selected, deactivate_selected]
    fieldsets = (
        ('Русский язык (RU)', {
            'fields': ('name_ru',)
        }),
        ('English (EN)', {
            'fields': ('name_en',),
            'classes': ('collapse',)
        }),
        ('O\'zbek (UZ)', {
            'fields': ('name_uz',),
            'classes': ('collapse',)
        }),
        ('Дополнительно', {
            'fields': ('logo', 'website', 'order', 'is_active')
        }),
    )
    
    def name_display(self, obj):
        return format_html(
            '<strong>{}</strong><br>'
            '<span style="color: #666; font-size: 0.85em;">EN: {}</span><br>'
            '<span style="color: #666; font-size: 0.85em;">UZ: {}</span>',
            obj.name_ru,
            obj.name_en or '-',
            obj.name_uz or '-'
        )
    name_display.short_description = 'Название'
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px; object-fit: contain; border-radius: 4px;" />', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Логотип'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background: #4caf50; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.85em;">Активен</span>')
        return format_html('<span style="background: #999; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.85em;">Неактивен</span>')
    is_active_badge.short_description = 'Статус'
    
    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank">Открыть</a>', obj.website)
        return '-'
    website_link.short_description = 'Сайт'


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['name_display', 'order']
    search_fields = ['name_ru', 'name_en', 'name_uz']
    ordering = ['order', 'name_ru']
    fieldsets = (
        ('Русский язык (RU)', {
            'fields': ('name_ru',)
        }),
        ('English (EN)', {
            'fields': ('name_en',),
            'classes': ('collapse',)
        }),
        ('O\'zbek (UZ)', {
            'fields': ('name_uz',),
            'classes': ('collapse',)
        }),
        ('Дополнительно', {
            'fields': ('order',)
        }),
    )
    
    def name_display(self, obj):
        return format_html(
            '<strong>{}</strong><br>'
            '<span style="color: #666; font-size: 0.85em;">EN: {}</span><br>'
            '<span style="color: #666; font-size: 0.85em;">UZ: {}</span>',
            obj.name_ru,
            obj.name_en or '-',
            obj.name_uz or '-'
        )
    name_display.short_description = 'Название'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_short', 'category', 'order', 'is_active_badge']
    list_filter = ['category', 'is_active']
    search_fields = ['question_ru', 'question_en', 'question_uz', 'answer_ru', 'answer_en', 'answer_uz']
    ordering = ['order', 'question_ru']
    actions = [activate_selected, deactivate_selected]
    fieldsets = (
        ('Русский язык (RU)', {
            'fields': ('question_ru', 'answer_ru')
        }),
        ('English (EN)', {
            'fields': ('question_en', 'answer_en'),
            'classes': ('collapse',)
        }),
        ('O\'zbek (UZ)', {
            'fields': ('question_uz', 'answer_uz'),
            'classes': ('collapse',)
        }),
        ('Дополнительно', {
            'fields': ('category', 'order', 'is_active')
        }),
    )
    
    def question_short(self, obj):
        question = obj.question_ru
        if len(question) > 60:
            return question[:60] + '...'
        return question
    question_short.short_description = 'Вопрос'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background: #4caf50; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.85em;">Активен</span>')
        return format_html('<span style="background: #999; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.85em;">Неактивен</span>')
    is_active_badge.short_description = 'Статус'


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Русский язык (RU)', {
            'fields': ('name_ru', 'about_text_ru', 'mission_ru', 'values_ru', 'history_ru', 'address_ru', 'city_ru', 'working_hours_ru')
        }),
        ('English (EN)', {
            'fields': ('name_en', 'about_text_en', 'mission_en', 'values_en', 'history_en', 'address_en', 'city_en', 'working_hours_en'),
            'classes': ('collapse',)
        }),
        ('O\'zbek (UZ)', {
            'fields': ('name_uz', 'about_text_uz', 'mission_uz', 'values_uz', 'history_uz', 'address_uz', 'city_uz', 'working_hours_uz'),
            'classes': ('collapse',)
        }),
        ('Контакты (общие)', {
            'fields': ('logo', 'email', 'phone', 'postal_code')
        }),
        ('Карта', {
            'fields': ('map_url', 'latitude', 'longitude')
        }),
        ('Социальные сети', {
            'fields': ('facebook', 'instagram', 'twitter', 'telegram')
        }),
    )
    
    def has_add_permission(self, request):
        # Разрешаем только одну запись
        return not CompanyInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    list_display = ['title_display', 'icon_display', 'order', 'is_active_badge']
    list_filter = ['is_active']
    search_fields = ['title_ru', 'title_en', 'title_uz', 'description_ru', 'description_en', 'description_uz']
    ordering = ['order', 'title_ru']
    actions = [activate_selected, deactivate_selected]
    
    fieldsets = (
        ('Русский язык (RU)', {
            'fields': ('title_ru', 'description_ru')
        }),
        ('English (EN)', {
            'fields': ('title_en', 'description_en'),
            'classes': ('collapse',)
        }),
        ('O\'zbek (UZ)', {
            'fields': ('title_uz', 'description_uz'),
            'classes': ('collapse',)
        }),
        ('Дополнительно', {
            'fields': ('icon', 'order', 'is_active')
        }),
    )
    
    def title_display(self, obj):
        return format_html(
            '<strong>{}</strong><br>'
            '<span style="color: #666; font-size: 0.85em;">EN: {}</span><br>'
            '<span style="color: #666; font-size: 0.85em;">UZ: {}</span>',
            obj.title_ru,
            obj.title_en or '-',
            obj.title_uz or '-'
        )
    title_display.short_description = 'Заголовок'
    
    class Media:
        css = {
            'all': ('admin/css/icon_helper.css',)
        }
        js = ('admin/js/icon_helper.js',)
    
    def icon_display(self, obj):
        if obj.icon:
            return format_html('<i class="{}" style="font-size: 1.5em;"></i>', obj.icon)
        return '-'
    icon_display.short_description = 'Иконка'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background: #4caf50; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.85em;">Активен</span>')
        return format_html('<span style="background: #999; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.85em;">Неактивен</span>')
    is_active_badge.short_description = 'Статус'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Добавляем визуальную подсказку с иконками
        if 'icon' in form.base_fields:
            form.base_fields['icon'].help_text = self._get_icon_help_text()
        return form
    
    def _get_icon_help_text(self):
        """Генерирует HTML с примерами иконок"""
        icons = [
            ('fas fa-star', 'Звезда'),
            ('fas fa-shipping-fast', 'Доставка'),
            ('fas fa-shield-alt', 'Защита'),
            ('fas fa-headset', 'Поддержка'),
            ('fas fa-trophy', 'Трофей'),
            ('fas fa-gift', 'Подарок'),
            ('fas fa-clock', 'Время'),
            ('fas fa-check-circle', 'Галочка'),
            ('fas fa-heart', 'Сердце'),
            ('fas fa-thumbs-up', 'Лайк'),
            ('fas fa-award', 'Награда'),
            ('fas fa-certificate', 'Сертификат'),
            ('fas fa-medal', 'Медаль'),
            ('fas fa-handshake', 'Рукопожатие'),
            ('fas fa-users', 'Пользователи'),
            ('fas fa-truck', 'Грузовик'),
            ('fas fa-box', 'Коробка'),
            ('fas fa-credit-card', 'Карта'),
            ('fas fa-lock', 'Замок'),
            ('fas fa-fire', 'Огонь'),
        ]
        
        html = '<div class="icon-helper-container">'
        html += '<p><strong>Популярные иконки Font Awesome:</strong></p>'
        html += '<div class="icon-helper-grid">'
        for icon_class, description in icons:
            html += format_html(
                '<div class="icon-helper-item" data-icon="{}">'
                '<i class="{}"></i>'
                '<span class="icon-helper-name">{}</span>'
                '<span class="icon-helper-class">{}</span>'
                '</div>',
                icon_class, icon_class, description, icon_class
            )
        html += '</div>'
        html += '<p class="icon-helper-note">Нажмите на иконку, чтобы скопировать класс в поле выше</p>'
        html += '</div>'
        return format_html(html)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject_short', 'is_read_badge', 'phone', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message', 'phone']
    readonly_fields = ['created_at', 'formatted_message']
    ordering = ['-created_at']
    actions = [mark_as_read, mark_as_unread]
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Информация о сообщении', {
            'fields': ('name', 'email', 'phone', 'subject', 'created_at', 'is_read')
        }),
        ('Сообщение', {
            'fields': ('formatted_message',)
        }),
    )
    
    def subject_short(self, obj):
        if len(obj.subject) > 40:
            return obj.subject[:40] + '...'
        return obj.subject
    subject_short.short_description = 'Тема'
    
    def is_read_badge(self, obj):
        if obj.is_read:
            return format_html('<span style="background: #4caf50; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.85em;">✓ Прочитано</span>')
        return format_html('<span style="background: #ff9800; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.85em;">● Новое</span>')
    is_read_badge.short_description = 'Статус'
    
    def formatted_message(self, obj):
        return format_html('<div style="padding: 15px; background: #f5f5f5; border-radius: 4px; white-space: pre-wrap;">{}</div>', obj.message)
    formatted_message.short_description = 'Текст сообщения'


# Настройка админ-панели
admin.site.site_header = 'LuxWood - Панель управления'
admin.site.site_title = 'LuxWood Admin'
admin.site.index_title = 'Добро пожаловать в панель управления'

# Переопределяем index для добавления статистики
original_index = admin.site.index

def custom_index(request, extra_context=None):
    extra_context = extra_context or {}
    
    # Основная статистика
    extra_context['total_products'] = Product.objects.count()
    extra_context['total_orders'] = Order.objects.count()
    extra_context['unread_messages'] = ContactMessage.objects.filter(is_read=False).count()
    extra_context['featured_products'] = Product.objects.filter(featured=True).count()
    
    # Дополнительная статистика
    extra_context['total_categories'] = Category.objects.count()
    extra_context['total_banners'] = Banner.objects.filter(is_active=True).count()
    extra_context['total_sponsors'] = Sponsor.objects.filter(is_active=True).count()
    extra_context['total_faqs'] = FAQ.objects.filter(is_active=True).count()
    extra_context['total_advantages'] = Advantage.objects.filter(is_active=True).count()
    extra_context['total_carts'] = Cart.objects.count()
    
    # Статистика заказов по статусам
    extra_context['pending_orders'] = Order.objects.filter(status='pending').count()
    extra_context['processing_orders'] = Order.objects.filter(status='processing').count()
    extra_context['delivered_orders'] = Order.objects.filter(status='delivered').count()
    extra_context['cancelled_orders'] = Order.objects.filter(status='cancelled').count()
    
    # Общая сумма заказов
    total_revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0
    extra_context['total_revenue'] = total_revenue
    
    # Товары с низким остатком
    extra_context['low_stock_products'] = Product.objects.filter(stock__lt=10, stock__gt=0).count()
    extra_context['out_of_stock_products'] = Product.objects.filter(stock=0).count()
    
    # Последние записи
    extra_context['recent_orders'] = Order.objects.all()[:5]
    extra_context['recent_messages'] = ContactMessage.objects.all()[:5]
    extra_context['recent_products'] = Product.objects.all()[:5]
    extra_context['recent_categories'] = Category.objects.all()[:5]
    extra_context['recent_banners'] = Banner.objects.all()[:5]
    extra_context['recent_faqs'] = FAQ.objects.all()[:5]
    
    return original_index(request, extra_context)

admin.site.index = custom_index
