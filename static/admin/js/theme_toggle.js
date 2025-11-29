/**
 * LuxWood Admin - Theme Toggle
 * Переключение между темной и светлой темой
 */

(function() {
    'use strict';
    
    // Получаем текущую тему из localStorage или используем системную
    function getTheme() {
        const savedTheme = localStorage.getItem('admin-theme');
        if (savedTheme) {
            return savedTheme;
        }
        
        // Проверяем системную тему
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        
        return 'light';
    }
    
    // Применяем тему
    function applyTheme(theme) {
        const html = document.documentElement;
        if (theme === 'dark') {
            html.setAttribute('data-theme', 'dark');
            updateThemeIcon('dark');
        } else {
            html.setAttribute('data-theme', 'light');
            updateThemeIcon('light');
        }
        localStorage.setItem('admin-theme', theme);
    }
    
    // Обновляем иконку переключателя
    function updateThemeIcon(theme) {
        const icon = document.getElementById('theme-icon');
        if (icon) {
            icon.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    }
    
    // Переключаем тему
    function toggleTheme() {
        const currentTheme = getTheme();
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(newTheme);
    }
    
    // Инициализация при загрузке страницы
    document.addEventListener('DOMContentLoaded', function() {
        // Применяем сохраненную тему
        const theme = getTheme();
        applyTheme(theme);
        
        // Добавляем обработчик на кнопку переключения
        const toggleButton = document.getElementById('theme-toggle');
        if (toggleButton) {
            toggleButton.addEventListener('click', toggleTheme);
        }
        
        // Слушаем изменения системной темы (только если тема не была сохранена)
        if (window.matchMedia && !localStorage.getItem('admin-theme')) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', function(e) {
                if (!localStorage.getItem('admin-theme')) {
                    applyTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    });
    
    // Применяем тему сразу (до загрузки DOM) для избежания мерцания
    const theme = getTheme();
    if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
})();


