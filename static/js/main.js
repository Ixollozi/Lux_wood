// Add to Cart functionality
document.addEventListener('DOMContentLoaded', function() {
    // Handle add to cart buttons
    const addToCartButtons = document.querySelectorAll('.btn-add-cart, .add-to-cart-btn');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.getAttribute('data-product-id');
            const quantity = document.getElementById('product-quantity') 
                ? parseInt(document.getElementById('product-quantity').value) 
                : 1;
            
            addToCart(productId, quantity);
        });
    });
    
    // Catalog dropdown menu
    const catalogBtn = document.getElementById('catalogBtn');
    const catalogMenu = document.getElementById('catalogMenu');
    
    if (catalogBtn && catalogMenu) {
        catalogBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            catalogMenu.classList.toggle('show');
            catalogBtn.classList.toggle('active');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!catalogBtn.contains(e.target) && !catalogMenu.contains(e.target)) {
                catalogMenu.classList.remove('show');
                catalogBtn.classList.remove('active');
            }
        });
        
        // Close menu when clicking on a link
        const catalogLinks = catalogMenu.querySelectorAll('a');
        catalogLinks.forEach(link => {
            link.addEventListener('click', function() {
                catalogMenu.classList.remove('show');
                catalogBtn.classList.remove('active');
            });
        });
    }
});

function addToCart(productId, quantity = 1) {
    const formData = new FormData();
    formData.append('quantity', quantity);
    
    fetch(`/cart/add/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update cart count
            const cartCount = document.querySelector('.cart-count');
            if (cartCount) {
                if (data.cart_items_count > 0) {
                    cartCount.textContent = data.cart_items_count;
                    cartCount.style.display = 'flex';
                } else {
                    cartCount.textContent = '';
                    cartCount.style.display = 'none';
                }
            } else if (data.cart_items_count > 0) {
                // Create cart count badge if it doesn't exist and there are items
                const cartIcon = document.querySelector('.cart-icon');
                if (cartIcon) {
                    const badge = document.createElement('span');
                    badge.className = 'cart-count';
                    badge.textContent = data.cart_items_count;
                    cartIcon.appendChild(badge);
                }
            }
            
            // Show success message
            showMessage('Товар добавлен в корзину!', 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Ошибка при добавлении товара', 'error');
    });
}

function updateCartItem(itemId, delta) {
    const quantityInput = document.getElementById(`qty-${itemId}`);
    const currentQuantity = parseInt(quantityInput.value);
    const newQuantity = Math.max(1, currentQuantity + delta);
    
    const formData = new FormData();
    formData.append('quantity', newQuantity);
    
    fetch(`/cart/update/${itemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            quantityInput.value = newQuantity;
            
            // Update item total
            const itemTotal = document.querySelector(`[data-item-id="${itemId}"] .item-total-price`);
            if (itemTotal) {
                itemTotal.textContent = data.item_total.toFixed(2) + '₽';
            }
            
            // Update cart total
            const cartTotal = document.getElementById('cart-total');
            if (cartTotal) {
                cartTotal.textContent = data.cart_total.toFixed(2) + '₽';
            }
            
            // Update total items
            const totalItems = document.getElementById('total-items');
            if (totalItems) {
                totalItems.textContent = data.cart_items_count;
            }
            
            // Update header cart count
            const cartCount = document.querySelector('.cart-count');
            if (cartCount) {
                if (data.cart_items_count > 0) {
                    cartCount.textContent = data.cart_items_count;
                    cartCount.style.display = 'flex';
                } else {
                    cartCount.textContent = '';
                    cartCount.style.display = 'none';
                }
            } else if (data.cart_items_count > 0) {
                // Create cart count badge if it doesn't exist and there are items
                const cartIcon = document.querySelector('.cart-icon');
                if (cartIcon) {
                    const badge = document.createElement('span');
                    badge.className = 'cart-count';
                    badge.textContent = data.cart_items_count;
                    cartIcon.appendChild(badge);
                }
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Ошибка при обновлении корзины', 'error');
    });
}

function removeCartItem(itemId) {
    if (!confirm('Удалить товар из корзины?')) {
        return;
    }
    
    fetch(`/cart/remove/${itemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove item from DOM
            const cartItem = document.querySelector(`[data-item-id="${itemId}"]`);
            if (cartItem) {
                cartItem.remove();
            }
            
            // Update cart total
            const cartTotal = document.getElementById('cart-total');
            if (cartTotal) {
                cartTotal.textContent = data.cart_total.toFixed(2) + '₽';
            }
            
            // Update total items
            const totalItems = document.getElementById('total-items');
            if (totalItems) {
                totalItems.textContent = data.cart_items_count;
            }
            
            // Update header cart count
            const cartCount = document.querySelector('.cart-count');
            if (cartCount) {
                if (data.cart_items_count > 0) {
                    cartCount.textContent = data.cart_items_count;
                    cartCount.style.display = 'flex';
                } else {
                    cartCount.textContent = '';
                    cartCount.style.display = 'none';
                }
            } else if (data.cart_items_count > 0) {
                // Create cart count badge if it doesn't exist and there are items
                const cartIcon = document.querySelector('.cart-icon');
                if (cartIcon) {
                    const badge = document.createElement('span');
                    badge.className = 'cart-count';
                    badge.textContent = data.cart_items_count;
                    cartIcon.appendChild(badge);
                }
            }
            
            // Check if cart is empty
            if (data.cart_items_count === 0) {
                // Hide cart count badge when cart is empty
                const cartCount = document.querySelector('.cart-count');
                if (cartCount) {
                    cartCount.style.display = 'none';
                    cartCount.textContent = '';
                }
                location.reload();
            }
            
            showMessage('Товар удален из корзины', 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Ошибка при удалении товара', 'error');
    });
}

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show message notification
function showMessage(message, type = 'success') {
    // Remove existing messages
    const existingMessages = document.querySelector('.message-notification');
    if (existingMessages) {
        existingMessages.remove();
    }
    
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `message-notification message-${type}`;
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: ${type === 'success' ? '#28a745' : '#dc3545'};
        color: white;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(messageDiv);
    
    // Remove after 3 seconds
    setTimeout(() => {
        messageDiv.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            messageDiv.remove();
        }, 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Banner Slider
document.addEventListener('DOMContentLoaded', function() {
    const bannerSlider = document.querySelector('.banner-slider');
    if (bannerSlider) {
        const slides = bannerSlider.querySelectorAll('.banner-slide');
        if (slides.length > 1) {
            let currentSlide = 0;
            
            function showSlide(index) {
                slides.forEach((slide, i) => {
                    slide.style.display = i === index ? 'block' : 'none';
                });
            }
            
            function nextSlide() {
                currentSlide = (currentSlide + 1) % slides.length;
                showSlide(currentSlide);
            }
            
            // Auto-rotate every 5 seconds
            setInterval(nextSlide, 5000);
        }
    }
    
    // Sponsors carousel auto-scroll
    const sponsorsCarousel = document.querySelector('.sponsors-carousel');
    if (sponsorsCarousel) {
        let scrollPosition = 0;
        const scrollSpeed = 1;
        const scrollWidth = sponsorsCarousel.scrollWidth;
        const clientWidth = sponsorsCarousel.clientWidth;
        
        function autoScroll() {
            scrollPosition += scrollSpeed;
            if (scrollPosition >= scrollWidth - clientWidth) {
                scrollPosition = 0;
            }
            sponsorsCarousel.scrollLeft = scrollPosition;
        }
        
        // Pause on hover
        sponsorsCarousel.addEventListener('mouseenter', function() {
            clearInterval(scrollInterval);
        });
        
        sponsorsCarousel.addEventListener('mouseleave', function() {
            scrollInterval = setInterval(autoScroll, 20);
        });
        
        let scrollInterval = setInterval(autoScroll, 20);
    }
});

