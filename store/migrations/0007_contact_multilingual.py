# Generated manually for multilingual support

from django.db import migrations, models


def migrate_contact_data(apps, schema_editor):
    """Переносит данные из старых полей в новые многоязычные поля"""
    Contact = apps.get_model('store', 'Contact')
    for contact in Contact.objects.all():
        # Переносим данные в русские поля (основной язык)
        if hasattr(contact, 'name') and contact.name:
            contact.name_ru = contact.name
        if hasattr(contact, 'address') and contact.address:
            contact.address_ru = contact.address
        if hasattr(contact, 'city') and contact.city:
            contact.city_ru = contact.city
        if hasattr(contact, 'working_hours') and contact.working_hours:
            contact.working_hours_ru = contact.working_hours
        contact.save()


def reverse_migrate_contact_data(apps, schema_editor):
    """Обратный перенос данных из многоязычных полей в старые"""
    Contact = apps.get_model('store', 'Contact')
    for contact in Contact.objects.all():
        if hasattr(contact, 'name_ru') and contact.name_ru:
            contact.name = contact.name_ru
        if hasattr(contact, 'address_ru') and contact.address_ru:
            contact.address = contact.address_ru
        if hasattr(contact, 'city_ru') and contact.city_ru:
            contact.city = contact.city_ru
        if hasattr(contact, 'working_hours_ru') and contact.working_hours_ru:
            contact.working_hours = contact.working_hours_ru
        contact.save()


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_contact_alter_advantage_icon_and_more'),
    ]

    operations = [
        # Шаг 1: Добавляем новые многоязычные поля как nullable
        migrations.AddField(
            model_name='contact',
            name='name_ru',
            field=models.CharField(max_length=200, null=True, blank=True, verbose_name='Название (RU)', help_text='Например: Главный офис, Филиал в Москве'),
        ),
        migrations.AddField(
            model_name='contact',
            name='address_ru',
            field=models.TextField(null=True, blank=True, verbose_name='Адрес (RU)'),
        ),
        migrations.AddField(
            model_name='contact',
            name='city_ru',
            field=models.CharField(max_length=100, null=True, blank=True, default='Москва', verbose_name='Город (RU)'),
        ),
        migrations.AddField(
            model_name='contact',
            name='working_hours_ru',
            field=models.CharField(max_length=200, null=True, blank=True, default='Пн-Пт: 9:00 - 18:00', verbose_name='График работы (RU)'),
        ),
        migrations.AddField(
            model_name='contact',
            name='name_en',
            field=models.CharField(max_length=200, blank=True, verbose_name='Название (EN)', help_text='Например: Main Office, Moscow Branch'),
        ),
        migrations.AddField(
            model_name='contact',
            name='address_en',
            field=models.TextField(blank=True, verbose_name='Адрес (EN)'),
        ),
        migrations.AddField(
            model_name='contact',
            name='city_en',
            field=models.CharField(max_length=100, blank=True, default='Moscow', verbose_name='Город (EN)'),
        ),
        migrations.AddField(
            model_name='contact',
            name='working_hours_en',
            field=models.CharField(max_length=200, blank=True, default='Mon-Fri: 9:00 - 18:00', verbose_name='График работы (EN)'),
        ),
        migrations.AddField(
            model_name='contact',
            name='name_uz',
            field=models.CharField(max_length=200, blank=True, verbose_name='Название (UZ)', help_text='Например: Asosiy ofis, Moskva filiali'),
        ),
        migrations.AddField(
            model_name='contact',
            name='address_uz',
            field=models.TextField(blank=True, verbose_name='Адрес (UZ)'),
        ),
        migrations.AddField(
            model_name='contact',
            name='city_uz',
            field=models.CharField(max_length=100, blank=True, default='Moskva', verbose_name='Город (UZ)'),
        ),
        migrations.AddField(
            model_name='contact',
            name='working_hours_uz',
            field=models.CharField(max_length=200, blank=True, default='Dush-Juma: 9:00 - 18:00', verbose_name='График работы (UZ)'),
        ),
        
        # Шаг 2: Переносим данные
        migrations.RunPython(migrate_contact_data, reverse_migrate_contact_data),
        
        # Шаг 3: Делаем русские поля обязательными
        migrations.AlterField(
            model_name='contact',
            name='name_ru',
            field=models.CharField(max_length=200, verbose_name='Название (RU)', help_text='Например: Главный офис, Филиал в Москве'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='address_ru',
            field=models.TextField(verbose_name='Адрес (RU)'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='city_ru',
            field=models.CharField(max_length=100, default='Москва', verbose_name='Город (RU)'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='working_hours_ru',
            field=models.CharField(max_length=200, default='Пн-Пт: 9:00 - 18:00', verbose_name='График работы (RU)'),
        ),
        
        # Шаг 4: Удаляем старый индекс перед удалением полей (SQLite требует этого)
        migrations.RemoveIndex(
            model_name='contact',
            name='store_conta_city_6216d7_idx',
        ),
        
        # Шаг 5: Удаляем старые поля
        migrations.RemoveField(
            model_name='contact',
            name='name',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='address',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='city',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='working_hours',
        ),
        
        # Шаг 6: Добавляем новый индекс
        migrations.AddIndex(
            model_name='contact',
            index=models.Index(fields=['city_ru'], name='store_conta_city_ru_idx'),
        ),
        
        # Шаг 6: Обновляем ordering
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['order', 'name_ru'], 'verbose_name': 'Контакт', 'verbose_name_plural': 'Контакты'},
        ),
    ]

