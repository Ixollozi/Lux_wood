"""
Management command для очистки старых корзин (старше 30 дней)
Использование: python manage.py cleanup_old_carts [--days=30]
"""
from django.core.management.base import BaseCommand
from store.models import Cart


class Command(BaseCommand):
    help = 'Удаляет корзины, которые не обновлялись более указанного количества дней (по умолчанию 30 дней)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Количество дней, после которых корзина считается устаревшей (по умолчанию: 30)',
        )

    def handle(self, *args, **options):
        days = options['days']
        deleted_count = Cart.cleanup_old_carts(days=days)
        
        if deleted_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Успешно удалено {deleted_count} корзин(ы), которые не обновлялись более {days} дней.'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Корзины, которые не обновлялись более {days} дней, не найдены.'
                )
            )


