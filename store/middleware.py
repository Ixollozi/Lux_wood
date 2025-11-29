"""
Middleware для автоматической очистки старых корзин
"""
from pathlib import Path
from datetime import datetime
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from .models import Cart


class CartCleanupMiddleware:
    """
    Middleware для автоматической очистки корзин старше 30 дней.
    Проверяет и очищает старые корзины раз в день.
    """
    
    CACHE_KEY = 'cart_cleanup_last_run'
    CLEANUP_INTERVAL_HOURS = 24  # Проверять раз в 24 часа
    FILE_PATH = Path(settings.BASE_DIR) / 'cart_cleanup_last_run.txt'
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Проверяем, нужно ли запустить очистку (только для GET запросов, чтобы не нагружать)
        if request.method == 'GET':
            self._check_and_cleanup()
        
        response = self.get_response(request)
        return response
    
    def _get_last_run_time(self):
        """Получает время последнего запуска очистки"""
        # Пробуем получить из кеша
        try:
            last_run = cache.get(self.CACHE_KEY)
            if last_run:
                return last_run
        except Exception:
            pass
        
        # Если кеш недоступен, используем файл
        try:
            if self.FILE_PATH.exists():
                content = self.FILE_PATH.read_text().strip()
                # Пробуем прочитать в человекочитаемом формате (ISO)
                try:
                    # Парсим ISO формат: "2024-01-15 14:30:45.123456+00:00"
                    dt = datetime.fromisoformat(content.replace('Z', '+00:00'))
                    if dt.tzinfo is None:
                        dt = timezone.make_aware(dt)
                    return dt
                except ValueError:
                    # Если не получилось, пробуем старый формат (timestamp) для обратной совместимости
                    try:
                        timestamp = float(content)
                        return timezone.datetime.fromtimestamp(timestamp, tz=timezone.utc)
                    except ValueError:
                        pass
        except Exception:
            pass
        
        return None
    
    def _set_last_run_time(self, time_value):
        """Сохраняет время последнего запуска очистки"""
        # Пробуем сохранить в кеш
        try:
            cache.set(self.CACHE_KEY, time_value, timeout=86400 * 2)  # 2 дня
        except Exception:
            pass
        
        # Также сохраняем в файл для надежности в человекочитаемом формате
        try:
            # Форматируем дату в ISO формате с часовым поясом
            formatted_time = time_value.isoformat()
            self.FILE_PATH.write_text(formatted_time)
        except Exception:
            pass
    
    def _check_and_cleanup(self):
        """Проверяет, нужно ли запустить очистку, и запускает её при необходимости"""
        last_run = self._get_last_run_time()
        now = timezone.now()
        
        # Если очистка еще не запускалась или прошло более 24 часов
        if last_run is None:
            self._run_cleanup()
            self._set_last_run_time(now)
        else:
            # Проверяем, прошло ли достаточно времени
            time_diff = (now - last_run).total_seconds() / 3600  # в часах
            if time_diff >= self.CLEANUP_INTERVAL_HOURS:
                self._run_cleanup()
                self._set_last_run_time(now)
    
    def _run_cleanup(self):
        """Запускает очистку старых корзин"""
        try:
            deleted_count = Cart.cleanup_old_carts(days=30)
            if deleted_count > 0:
                # Можно добавить логирование
                pass
        except Exception:
            # Игнорируем ошибки, чтобы не нарушать работу сайта
            pass

