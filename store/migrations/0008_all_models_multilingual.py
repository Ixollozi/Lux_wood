# Generated manually for multilingual support for all models

from django.db import migrations, models


def migrate_category_data(apps, schema_editor):
    """Переносит данные Category"""
    Category = apps.get_model('store', 'Category')
    for obj in Category.objects.all():
        if hasattr(obj, 'name') and obj.name:
            obj.name_ru = obj.name
        obj.save()


def migrate_product_data(apps, schema_editor):
    """Переносит данные Product"""
    Product = apps.get_model('store', 'Product')
    for obj in Product.objects.all():
        if hasattr(obj, 'name') and obj.name:
            obj.name_ru = obj.name
        if hasattr(obj, 'description') and obj.description:
            obj.description_ru = obj.description
        obj.save()


def migrate_banner_data(apps, schema_editor):
    """Переносит данные Banner"""
    Banner = apps.get_model('store', 'Banner')
    for obj in Banner.objects.all():
        if hasattr(obj, 'title') and obj.title:
            obj.title_ru = obj.title
        if hasattr(obj, 'description') and obj.description:
            obj.description_ru = obj.description
        obj.save()


def migrate_sponsor_data(apps, schema_editor):
    """Переносит данные Sponsor"""
    Sponsor = apps.get_model('store', 'Sponsor')
    for obj in Sponsor.objects.all():
        if hasattr(obj, 'name') and obj.name:
            obj.name_ru = obj.name
        obj.save()


def migrate_faqcategory_data(apps, schema_editor):
    """Переносит данные FAQCategory"""
    FAQCategory = apps.get_model('store', 'FAQCategory')
    for obj in FAQCategory.objects.all():
        if hasattr(obj, 'name') and obj.name:
            obj.name_ru = obj.name
        obj.save()


def migrate_faq_data(apps, schema_editor):
    """Переносит данные FAQ"""
    FAQ = apps.get_model('store', 'FAQ')
    for obj in FAQ.objects.all():
        if hasattr(obj, 'question') and obj.question:
            obj.question_ru = obj.question
        if hasattr(obj, 'answer') and obj.answer:
            obj.answer_ru = obj.answer
        obj.save()


def migrate_companyinfo_data(apps, schema_editor):
    """Переносит данные CompanyInfo"""
    CompanyInfo = apps.get_model('store', 'CompanyInfo')
    for obj in CompanyInfo.objects.all():
        if hasattr(obj, 'name') and obj.name:
            obj.name_ru = obj.name
        if hasattr(obj, 'about_text') and obj.about_text:
            obj.about_text_ru = obj.about_text
        if hasattr(obj, 'mission') and obj.mission:
            obj.mission_ru = obj.mission
        if hasattr(obj, 'values') and obj.values:
            obj.values_ru = obj.values
        if hasattr(obj, 'history') and obj.history:
            obj.history_ru = obj.history
        if hasattr(obj, 'address') and obj.address:
            obj.address_ru = obj.address
        if hasattr(obj, 'city') and obj.city:
            obj.city_ru = obj.city
        if hasattr(obj, 'working_hours') and obj.working_hours:
            obj.working_hours_ru = obj.working_hours
        obj.save()


def migrate_advantage_data(apps, schema_editor):
    """Переносит данные Advantage"""
    Advantage = apps.get_model('store', 'Advantage')
    for obj in Advantage.objects.all():
        if hasattr(obj, 'title') and obj.title:
            obj.title_ru = obj.title
        if hasattr(obj, 'description') and obj.description:
            obj.description_ru = obj.description
        obj.save()


def migrate_productattribute_data(apps, schema_editor):
    """Переносит данные ProductAttribute"""
    ProductAttribute = apps.get_model('store', 'ProductAttribute')
    for obj in ProductAttribute.objects.all():
        if hasattr(obj, 'name') and obj.name:
            obj.name_ru = obj.name
        if hasattr(obj, 'value') and obj.value:
            obj.value_ru = obj.value
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_contact_multilingual'),
    ]

    operations = [
        # Category - добавляем многоязычные поля
        migrations.AddField(
            model_name='category',
            name='name_en',
            field=models.CharField(blank=True, db_index=True, max_length=200, verbose_name='Название (EN)'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_uz',
            field=models.CharField(blank=True, db_index=True, max_length=200, verbose_name='Название (UZ)'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ru',
            field=models.CharField(db_index=True, max_length=200, null=True, verbose_name='Название (RU)'),
        ),
        
        # Product - добавляем многоязычные поля
        migrations.AddField(
            model_name='product',
            name='name_en',
            field=models.CharField(blank=True, db_index=True, max_length=300, verbose_name='Название (EN)'),
        ),
        migrations.AddField(
            model_name='product',
            name='name_uz',
            field=models.CharField(blank=True, db_index=True, max_length=300, verbose_name='Название (UZ)'),
        ),
        migrations.AddField(
            model_name='product',
            name='name_ru',
            field=models.CharField(db_index=True, max_length=300, null=True, verbose_name='Название (RU)'),
        ),
        migrations.AddField(
            model_name='product',
            name='description_en',
            field=models.TextField(blank=True, verbose_name='Описание (EN)'),
        ),
        migrations.AddField(
            model_name='product',
            name='description_uz',
            field=models.TextField(blank=True, verbose_name='Описание (UZ)'),
        ),
        migrations.AddField(
            model_name='product',
            name='description_ru',
            field=models.TextField(null=True, verbose_name='Описание (RU)'),
        ),
        
        # ProductAttribute - добавляем многоязычные поля
        migrations.AddField(
            model_name='productattribute',
            name='name_en',
            field=models.CharField(blank=True, max_length=200, verbose_name='Название характеристики (EN)'),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='name_uz',
            field=models.CharField(blank=True, max_length=200, verbose_name='Название характеристики (UZ)'),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='name_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Название характеристики (RU)'),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='value_en',
            field=models.CharField(blank=True, max_length=500, verbose_name='Значение (EN)'),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='value_uz',
            field=models.CharField(blank=True, max_length=500, verbose_name='Значение (UZ)'),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='value_ru',
            field=models.CharField(max_length=500, null=True, verbose_name='Значение (RU)'),
        ),
        
        # Banner - добавляем многоязычные поля
        migrations.AddField(
            model_name='banner',
            name='title_en',
            field=models.CharField(blank=True, max_length=200, verbose_name='Заголовок (EN)'),
        ),
        migrations.AddField(
            model_name='banner',
            name='title_uz',
            field=models.CharField(blank=True, max_length=200, verbose_name='Заголовок (UZ)'),
        ),
        migrations.AddField(
            model_name='banner',
            name='title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок (RU)'),
        ),
        migrations.AddField(
            model_name='banner',
            name='description_en',
            field=models.TextField(blank=True, verbose_name='Описание (EN)'),
        ),
        migrations.AddField(
            model_name='banner',
            name='description_uz',
            field=models.TextField(blank=True, verbose_name='Описание (UZ)'),
        ),
        migrations.AddField(
            model_name='banner',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Описание (RU)'),
        ),
        
        # Sponsor - добавляем многоязычные поля
        migrations.AddField(
            model_name='sponsor',
            name='name_en',
            field=models.CharField(blank=True, max_length=200, verbose_name='Название (EN)'),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='name_uz',
            field=models.CharField(blank=True, max_length=200, verbose_name='Название (UZ)'),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='name_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Название (RU)'),
        ),
        
        # FAQCategory - добавляем многоязычные поля
        migrations.AddField(
            model_name='faqcategory',
            name='name_en',
            field=models.CharField(blank=True, max_length=200, verbose_name='Название (EN)'),
        ),
        migrations.AddField(
            model_name='faqcategory',
            name='name_uz',
            field=models.CharField(blank=True, max_length=200, verbose_name='Название (UZ)'),
        ),
        migrations.AddField(
            model_name='faqcategory',
            name='name_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Название (RU)'),
        ),
        
        # FAQ - добавляем многоязычные поля
        migrations.AddField(
            model_name='faq',
            name='question_en',
            field=models.CharField(blank=True, max_length=500, verbose_name='Вопрос (EN)'),
        ),
        migrations.AddField(
            model_name='faq',
            name='question_uz',
            field=models.CharField(blank=True, max_length=500, verbose_name='Вопрос (UZ)'),
        ),
        migrations.AddField(
            model_name='faq',
            name='question_ru',
            field=models.CharField(max_length=500, null=True, verbose_name='Вопрос (RU)'),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_en',
            field=models.TextField(blank=True, verbose_name='Ответ (EN)'),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_uz',
            field=models.TextField(blank=True, verbose_name='Ответ (UZ)'),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_ru',
            field=models.TextField(null=True, verbose_name='Ответ (RU)'),
        ),
        
        # CompanyInfo - добавляем многоязычные поля
        migrations.AddField(
            model_name='companyinfo',
            name='name_en',
            field=models.CharField(blank=True, default='LuxWood', max_length=200, verbose_name='Название компании (EN)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='name_uz',
            field=models.CharField(blank=True, default='LuxWood', max_length=200, verbose_name='Название компании (UZ)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='name_ru',
            field=models.CharField(default='LuxWood', max_length=200, null=True, verbose_name='Название компании (RU)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='about_text_en',
            field=models.TextField(blank=True, default='', verbose_name='Текст о компании (EN)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='about_text_uz',
            field=models.TextField(blank=True, default='', verbose_name='Текст о компании (UZ)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='about_text_ru',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Текст о компании (RU)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='mission_en',
            field=models.TextField(blank=True, verbose_name='Миссия (EN)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='mission_uz',
            field=models.TextField(blank=True, verbose_name='Миссия (UZ)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='mission_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Миссия (RU)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='values_en',
            field=models.TextField(blank=True, verbose_name='Ценности (EN)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='values_uz',
            field=models.TextField(blank=True, verbose_name='Ценности (UZ)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='values_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Ценности (RU)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='history_en',
            field=models.TextField(blank=True, verbose_name='История (EN)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='history_uz',
            field=models.TextField(blank=True, verbose_name='История (UZ)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='history_ru',
            field=models.TextField(blank=True, null=True, verbose_name='История (RU)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='address_en',
            field=models.TextField(blank=True, default='', verbose_name='Адрес (EN)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='address_uz',
            field=models.TextField(blank=True, default='', verbose_name='Адрес (UZ)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='address_ru',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Адрес (RU)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='city_en',
            field=models.CharField(blank=True, default='Moscow', max_length=100, verbose_name='Город (EN)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='city_uz',
            field=models.CharField(blank=True, default='Moskva', max_length=100, verbose_name='Город (UZ)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='city_ru',
            field=models.CharField(default='Москва', max_length=100, null=True, verbose_name='Город (RU)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='working_hours_en',
            field=models.CharField(blank=True, default='Mon-Fri: 9:00 - 18:00', max_length=200, verbose_name='График работы (EN)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='working_hours_uz',
            field=models.CharField(blank=True, default='Dush-Juma: 9:00 - 18:00', max_length=200, verbose_name='График работы (UZ)'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='working_hours_ru',
            field=models.CharField(default='Пн-Пт: 9:00 - 18:00', max_length=200, null=True, verbose_name='График работы (RU)'),
        ),
        
        # Advantage - добавляем многоязычные поля
        migrations.AddField(
            model_name='advantage',
            name='title_en',
            field=models.CharField(blank=True, max_length=200, verbose_name='Заголовок (EN)'),
        ),
        migrations.AddField(
            model_name='advantage',
            name='title_uz',
            field=models.CharField(blank=True, max_length=200, verbose_name='Заголовок (UZ)'),
        ),
        migrations.AddField(
            model_name='advantage',
            name='title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок (RU)'),
        ),
        migrations.AddField(
            model_name='advantage',
            name='description_en',
            field=models.TextField(blank=True, verbose_name='Описание (EN)'),
        ),
        migrations.AddField(
            model_name='advantage',
            name='description_uz',
            field=models.TextField(blank=True, verbose_name='Описание (UZ)'),
        ),
        migrations.AddField(
            model_name='advantage',
            name='description_ru',
            field=models.TextField(null=True, verbose_name='Описание (RU)'),
        ),
        
        # Переносим данные
        migrations.RunPython(migrate_category_data, migrations.RunPython.noop),
        migrations.RunPython(migrate_product_data, migrations.RunPython.noop),
        migrations.RunPython(migrate_banner_data, migrations.RunPython.noop),
        migrations.RunPython(migrate_sponsor_data, migrations.RunPython.noop),
        migrations.RunPython(migrate_faqcategory_data, migrations.RunPython.noop),
        migrations.RunPython(migrate_faq_data, migrations.RunPython.noop),
        migrations.RunPython(migrate_companyinfo_data, migrations.RunPython.noop),
        migrations.RunPython(migrate_advantage_data, migrations.RunPython.noop),
        migrations.RunPython(migrate_productattribute_data, migrations.RunPython.noop),
        
        # Делаем русские поля обязательными
        migrations.AlterField(
            model_name='category',
            name='name_ru',
            field=models.CharField(db_index=True, max_length=200, verbose_name='Название (RU)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_ru',
            field=models.CharField(db_index=True, max_length=300, verbose_name='Название (RU)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_ru',
            field=models.TextField(verbose_name='Описание (RU)'),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='name_ru',
            field=models.CharField(max_length=200, verbose_name='Название характеристики (RU)'),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='value_ru',
            field=models.CharField(max_length=500, verbose_name='Значение (RU)'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='title_ru',
            field=models.CharField(max_length=200, verbose_name='Заголовок (RU)'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='description_ru',
            field=models.TextField(blank=True, verbose_name='Описание (RU)'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='name_ru',
            field=models.CharField(max_length=200, verbose_name='Название (RU)'),
        ),
        migrations.AlterField(
            model_name='faqcategory',
            name='name_ru',
            field=models.CharField(max_length=200, verbose_name='Название (RU)'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='question_ru',
            field=models.CharField(max_length=500, verbose_name='Вопрос (RU)'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='answer_ru',
            field=models.TextField(verbose_name='Ответ (RU)'),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='name_ru',
            field=models.CharField(default='LuxWood', max_length=200, verbose_name='Название компании (RU)'),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='about_text_ru',
            field=models.TextField(blank=True, default='', verbose_name='Текст о компании (RU)'),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='mission_ru',
            field=models.TextField(blank=True, verbose_name='Миссия (RU)'),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='values_ru',
            field=models.TextField(blank=True, verbose_name='Ценности (RU)'),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='history_ru',
            field=models.TextField(blank=True, verbose_name='История (RU)'),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='address_ru',
            field=models.TextField(blank=True, default='', verbose_name='Адрес (RU)'),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='city_ru',
            field=models.CharField(default='Москва', max_length=100, verbose_name='Город (RU)'),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='working_hours_ru',
            field=models.CharField(default='Пн-Пт: 9:00 - 18:00', max_length=200, verbose_name='График работы (RU)'),
        ),
        migrations.AlterField(
            model_name='advantage',
            name='title_ru',
            field=models.CharField(max_length=200, verbose_name='Заголовок (RU)'),
        ),
        migrations.AlterField(
            model_name='advantage',
            name='description_ru',
            field=models.TextField(verbose_name='Описание (RU)'),
        ),
        
        # Удаляем старые поля
        migrations.RemoveField(
            model_name='category',
            name='name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='name',
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='value',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='title',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='description',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='name',
        ),
        migrations.RemoveField(
            model_name='faqcategory',
            name='name',
        ),
        migrations.RemoveField(
            model_name='faq',
            name='question',
        ),
        migrations.RemoveField(
            model_name='faq',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='companyinfo',
            name='name',
        ),
        migrations.RemoveField(
            model_name='companyinfo',
            name='about_text',
        ),
        migrations.RemoveField(
            model_name='companyinfo',
            name='mission',
        ),
        migrations.RemoveField(
            model_name='companyinfo',
            name='values',
        ),
        migrations.RemoveField(
            model_name='companyinfo',
            name='history',
        ),
        migrations.RemoveField(
            model_name='companyinfo',
            name='address',
        ),
        migrations.RemoveField(
            model_name='companyinfo',
            name='city',
        ),
        migrations.RemoveField(
            model_name='companyinfo',
            name='working_hours',
        ),
        migrations.RemoveField(
            model_name='advantage',
            name='title',
        ),
        migrations.RemoveField(
            model_name='advantage',
            name='description',
        ),
        
        # Обновляем ordering
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name_ru'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='productattribute',
            options={'ordering': ['order', 'name_ru'], 'verbose_name': 'Характеристика товара', 'verbose_name_plural': 'Характеристики товаров'},
        ),
        migrations.AlterModelOptions(
            name='sponsor',
            options={'ordering': ['order', 'name_ru'], 'verbose_name': 'Спонсор', 'verbose_name_plural': 'Спонсоры'},
        ),
        migrations.AlterModelOptions(
            name='faqcategory',
            options={'ordering': ['order', 'name_ru'], 'verbose_name': 'Категория FAQ', 'verbose_name_plural': 'Категории FAQ'},
        ),
        migrations.AlterModelOptions(
            name='faq',
            options={'ordering': ['order', 'question_ru'], 'verbose_name': 'FAQ', 'verbose_name_plural': 'FAQ'},
        ),
        migrations.AlterModelOptions(
            name='advantage',
            options={'ordering': ['order', 'title_ru'], 'verbose_name': 'Преимущество', 'verbose_name_plural': 'Преимущества'},
        ),
    ]

