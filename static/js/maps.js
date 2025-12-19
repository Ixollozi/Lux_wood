/**
 * Maps Integration Script
 * Поддержка Яндекс.Карт и Google Maps
 */

(function() {
    'use strict';

    /**
     * Конвертирует ссылку Яндекс.Карт в embed формат
     * @param {string} url - Ссылка на Яндекс.Карты
     * @returns {string} - Embed URL для iframe
     */
    function convertYandexMapUrl(url) {
        // Если уже embed формат
        if (url.includes('/map-widget/')) {
            // Убеждаемся, что есть нужные параметры
            if (!url.includes('width=')) {
                url += (url.includes('?') ? '&' : '?') + 'width=100%25&height=400&lang=ru_RU&scroll=true';
            }
            return url;
        }

        // Извлекаем координаты или ID места из URL
        // Формат: https://yandex.ru/maps/-/CCUqMZqH0C
        // Или: https://yandex.ru/maps/?pt=37.6173,55.7558&z=15&l=map
        
        if (url.includes('/maps/-/')) {
            // Новый формат с ID (например: https://yandex.ru/maps/-/CCUqMZqH0C)
            const match = url.match(/\/maps\/-\/([A-Za-z0-9]+)/);
            if (match) {
                const mapId = match[1];
                return `https://yandex.ru/map-widget/v1/-/${mapId}?width=100%25&height=400&lang=ru_RU&scroll=true`;
            }
        }
        
        // Формат с координатами через параметр pt
        if (url.includes('pt=')) {
            const ptMatch = url.match(/pt=([\d.]+),([\d.]+)/);
            if (ptMatch) {
                const lon = ptMatch[1];
                const lat = ptMatch[2];
                // Извлекаем zoom если есть
                const zoomMatch = url.match(/[?&]z=(\d+)/);
                const zoom = zoomMatch ? zoomMatch[1] : '15';
                return `https://yandex.ru/map-widget/v1/?ll=${lon},${lat}&z=${zoom}&l=map&pt=${lon},${lat}&width=100%25&height=400&lang=ru_RU&scroll=true`;
            }
        }
        
        // Формат с координатами через параметр ll
        if (url.includes('ll=')) {
            const llMatch = url.match(/ll=([\d.]+),([\d.]+)/);
            if (llMatch) {
                const lon = llMatch[1];
                const lat = llMatch[2];
                const zoomMatch = url.match(/[?&]z=(\d+)/);
                const zoom = zoomMatch ? zoomMatch[1] : '15';
                return `https://yandex.ru/map-widget/v1/?ll=${lon},${lat}&z=${zoom}&l=map&pt=${lon},${lat}&width=100%25&height=400&lang=ru_RU&scroll=true`;
            }
        }

        // Если не удалось распознать, пробуем использовать прямую ссылку
        // Яндекс.Карты могут работать и без конвертации в некоторых случаях
        console.warn('Не удалось конвертировать ссылку Яндекс.Карт:', url);
        return url;
    }

    /**
     * Конвертирует ссылку Google Maps в embed формат
     * @param {string} url - Ссылка на Google Maps
     * @returns {string} - Embed URL для iframe
     */
    function convertGoogleMapUrl(url) {
        // Если уже embed формат
        if (url.includes('/embed')) {
            return url;
        }

        // Конвертируем обычную ссылку в embed
        // Формат: https://www.google.com/maps?q=55.7558,37.6173
        if (url.includes('maps?q=')) {
            const match = url.match(/maps\?q=([\d.]+),([\d.]+)/);
            if (match) {
                const lat = match[1];
                const lng = match[2];
                return `https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2000!2d${lng}!3d${lat}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNTXCsDQ1JzIwLjkiTiAzN8KwMzcnMDIuMyJF!5e0!3m2!1sru!2sru!4v1234567890123!5m2!1sru!2sru`;
            }
        }

        // Если не удалось распознать, возвращаем оригинальную ссылку
        return url;
    }

    /**
     * Инициализирует карту на странице
     */
    function initMaps() {
        // Находим все контейнеры с картами
        const mapContainers = document.querySelectorAll('.map-container');
        
        mapContainers.forEach(function(container) {
            const iframe = container.querySelector('iframe[data-map-url]');
            if (!iframe) return;

            const originalUrl = iframe.getAttribute('data-map-url');
            let embedUrl = originalUrl;

            // Определяем тип карты и конвертируем URL
            if (originalUrl.includes('yandex.ru/maps')) {
                embedUrl = convertYandexMapUrl(originalUrl);
            } else if (originalUrl.includes('google.com/maps') || originalUrl.includes('maps.google.com')) {
                embedUrl = convertGoogleMapUrl(originalUrl);
            }

            // Устанавливаем src для iframe
            iframe.src = embedUrl;
        });
    }

    // Инициализация при загрузке DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMaps);
    } else {
        initMaps();
    }

    // Экспортируем функции для использования в других скриптах
    window.MapsHelper = {
        convertYandexMapUrl: convertYandexMapUrl,
        convertGoogleMapUrl: convertGoogleMapUrl
    };
})();

