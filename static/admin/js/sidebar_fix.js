/**
 * LuxWood Admin - Sidebar Fix
 * Убеждаемся, что sidebar виден на главной странице
 */

(function() {
    'use strict';
    
    // Проверяем, находимся ли мы на главной странице
    function isIndexPage() {
        const path = window.location.pathname;
        const hasDashboard = document.querySelector('.dashboard-container');
        return path === '/admin/' || 
               path === '/admin' ||
               path.match(/^\/admin\/?$/) ||
               document.body.classList.contains('index') ||
               hasDashboard !== null;
    }
    
    // Открываем sidebar на главной странице
    function ensureSidebarVisible() {
        const sidebar = document.getElementById('nav-sidebar');
        const toggleButton = document.getElementById('toggle-nav-sidebar');
        
        if (!sidebar) {
            // Если sidebar еще не загружен, попробуем позже
            return false;
        }
        
        // Если мы на главной странице, принудительно открываем sidebar
        if (isIndexPage()) {
            // Добавляем класс для идентификации главной страницы
            document.body.classList.add('dashboard-page');
            
            // Удаляем класс collapsed
            sidebar.classList.remove('collapsed');
            document.body.classList.remove('sidebar-collapsed');
            document.body.classList.add('sticky-enabled');
            
            // Обновляем localStorage
            localStorage.setItem('django.admin.nav-sidebar', 'sticky');
            
            // Обновляем иконку кнопки, если она есть
            if (toggleButton) {
                const icon = toggleButton.querySelector('i');
                if (icon) {
                    icon.className = 'icon-arrow-left';
                }
                // Также обновляем aria-label
                toggleButton.setAttribute('aria-label', 'Скрыть навигацию');
            }
            
            // Принудительно показываем sidebar
            sidebar.style.display = 'block';
            sidebar.style.visibility = 'visible';
            sidebar.style.position = 'fixed';
            sidebar.style.left = '0';
            sidebar.style.top = '60px';
            sidebar.style.height = 'calc(100vh - 60px)';
            sidebar.style.zIndex = '1000';
            
            return true;
        }
        
        return false;
    }
    
    // Инициализация при загрузке страницы
    function init() {
        let attempts = 0;
        const maxAttempts = 10;
        
        function tryEnsure() {
            attempts++;
            const success = ensureSidebarVisible();
            
            if (!success && attempts < maxAttempts) {
                setTimeout(tryEnsure, 200);
            }
        }
        
        tryEnsure();
    }
    
    // Запускаем при загрузке DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Слушаем изменения в DOM (на случай динамической загрузки)
    if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver(function(mutations) {
            let shouldCheck = false;
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length) {
                    for (let i = 0; i < mutation.addedNodes.length; i++) {
                        const node = mutation.addedNodes[i];
                        if (node.id === 'nav-sidebar' || 
                            (node.nodeType === 1 && node.querySelector && node.querySelector('#nav-sidebar'))) {
                            shouldCheck = true;
                            break;
                        }
                    }
                }
                // Также проверяем изменения классов
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    shouldCheck = true;
                }
            });
            if (shouldCheck) {
                ensureSidebarVisible();
            }
        });
        
        // Начинаем наблюдение за изменениями в body
        if (document.body) {
            observer.observe(document.body, {
                childList: true,
                subtree: true,
                attributes: true,
                attributeFilter: ['class']
            });
        }
    }
    
    // Перехватываем клики по кнопке переключения на главной странице
    document.addEventListener('click', function(e) {
        const toggleButton = document.getElementById('toggle-nav-sidebar');
        if (e.target === toggleButton || toggleButton?.contains(e.target)) {
            if (isIndexPage()) {
                // На главной странице не позволяем закрыть sidebar
                e.preventDefault();
                e.stopPropagation();
                ensureSidebarVisible();
                return false;
            }
        }
    }, true);
})();

