from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils.translation import activate, get_language
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    Category, Product, Cart, CartItem, Order, OrderItem,
    Banner, Sponsor, FAQ, FAQCategory, CompanyInfo, Advantage, ContactMessage
)


def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    
    # Проверяем существующую корзину и удаляем, если она истекла
    try:
        existing_cart = Cart.objects.get(session_key=request.session.session_key)
        if existing_cart.is_expired():
            existing_cart.delete()
            cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
        else:
            cart = existing_cart
    except Cart.DoesNotExist:
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    
    return cart


def home(request):
    categories = Category.objects.filter(parent=None).exclude(slug='')[:8]
    featured_products = Product.objects.filter(featured=True).exclude(slug='')[:12]
    latest_products = Product.objects.exclude(slug='')[:20]
    # Хиты продаж - товары с наибольшим рейтингом
    bestsellers = Product.objects.exclude(slug='').order_by('-rating', '-reviews_count')[:12]
    banners = Banner.objects.filter(is_active=True)
    sponsors = Sponsor.objects.filter(is_active=True)
    advantages = Advantage.objects.filter(is_active=True)
    faqs = FAQ.objects.filter(is_active=True)[:6]  # Показываем первые 6 на главной
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'latest_products': latest_products,
        'bestsellers': bestsellers,
        'banners': banners,
        'sponsors': sponsors,
        'advantages': advantages,
        'faqs': faqs,
    }
    return render(request, 'store/home.html', context)


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.exclude(slug='')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Поиск
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Фильтр по наличию
    in_stock = request.GET.get('in_stock', '')
    if in_stock == 'yes':
        products = products.filter(stock__gt=0)
    elif in_stock == 'no':
        products = products.filter(stock=0)
    
    # Фильтр по цене
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    if price_min:
        try:
            products = products.filter(price__gte=float(price_min))
        except ValueError:
            pass
    if price_max:
        try:
            products = products.filter(price__lte=float(price_max))
        except ValueError:
            pass
    
    # Сортировка
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')
    
    # Получаем все категории для сайдбара
    all_categories = Category.objects.filter(parent=None).exclude(slug='')
    
    context = {
        'category': category,
        'products': products,
        'search_query': search_query,
        'sort_by': sort_by,
        'in_stock': in_stock,
        'price_min': price_min,
        'price_max': price_max,
        'all_categories': all_categories,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id).exclude(slug='')[:8]
    attributes = product.attributes.all()
    
    context = {
        'product': product,
        'related_products': related_products,
        'attributes': attributes,
    }
    return render(request, 'store/product_detail.html', context)


def cart_view(request):
    cart = get_or_create_cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'store/cart.html', context)


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return JsonResponse({
        'success': True,
        'cart_items_count': cart.total_items,
        'message': 'Товар добавлен в корзину'
    })


@require_POST
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    cart = cart_item.cart
    return JsonResponse({
        'success': True,
        'cart_items_count': cart.total_items,
        'cart_total': float(cart.total_price),
        'item_total': float(cart_item.total_price)
    })


@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = cart_item.cart
    cart_item.delete()
    
    return JsonResponse({
        'success': True,
        'cart_items_count': cart.total_items,
        'cart_total': float(cart.total_price)
    })


def checkout(request):
    cart = get_or_create_cart(request)
    company_info = CompanyInfo.load()
    
    if cart.items.count() == 0:
        return redirect('cart')
    
    if request.method == 'POST':
        order = Order.objects.create(
            session_key=request.session.session_key,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            postal_code=request.POST.get('postal_code'),
            comment=request.POST.get('comment', ''),
            total_price=cart.total_price
        )
        
        order_items_text = []
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            order_items_text.append(f"{cart_item.product.name} x{cart_item.quantity} - {cart_item.product.price}₽")
        
        # Отправка email уведомления
        try:
            email_message = f"""
Новый заказ #{order.id}

Данные клиента:
Имя: {order.first_name} {order.last_name}
Email: {order.email}
Телефон: {order.phone}

Адрес доставки:
{order.address}
{order.city}, {order.postal_code}

Товары:
{chr(10).join(order_items_text)}

Общая сумма: {order.total_price}₽
"""
            recipient_email = company_info.email if company_info else 'noreply@shopeexpress.com'
            send_mail(
                subject=f'Новый заказ #{order.id}',
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@shopeexpress.com',
                recipient_list=[recipient_email],
                fail_silently=True,
            )
        except Exception:
            pass
        
        # Отправка Telegram уведомления (если настроен)
        try:
            telegram_bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
            telegram_chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)
            
            if telegram_bot_token and telegram_chat_id:
                import requests
                comment_text = f"\n💬 Комментарий: {order.comment}" if order.comment else ""
                telegram_message = f"""
🛒 Новый заказ #{order.id}

👤 Клиент: {order.first_name} {order.last_name}
📞 Телефон: {order.phone}
📧 Email: {order.email}

📍 Адрес: {order.address}, {order.city}

🛍️ Товары:
{chr(10).join(order_items_text)}
{comment_text}

💰 Сумма: {order.total_price}₽
"""
                requests.post(
                    f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage',
                    json={
                        'chat_id': telegram_chat_id,
                        'text': telegram_message,
                        'parse_mode': 'HTML'
                    },
                    timeout=5
                )
        except Exception:
            pass
        
        cart.delete()
        return redirect('order_success', order_id=order.id)
    
    context = {
        'cart': cart,
    }
    return render(request, 'store/checkout.html', context)


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_success.html', {'order': order})


def set_language(request):
    if request.method == 'POST':
        language = request.POST.get('language', 'ru')
        request.session['language'] = language
        activate(language)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def set_region(request):
    if request.method == 'POST':
        region = request.POST.get('region', 'RU')
        request.session['region'] = region
    return redirect(request.META.get('HTTP_REFERER', '/'))


def about(request):
    company_info = CompanyInfo.load()
    return render(request, 'store/about.html', {'company_info': company_info})


def contact(request):
    company_info = CompanyInfo.load()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        # Отправка email (если настроен)
        try:
            send_mail(
                subject=f'Новое сообщение: {subject}',
                message=f'От: {name} ({email})\nТелефон: {phone}\n\n{message}',
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else email,
                recipient_list=[company_info.email],
                fail_silently=True,
            )
        except Exception:
            pass
        
        return redirect('contact')
    
    return render(request, 'store/contact.html', {'company_info': company_info})


def faq_page(request):
    categories = FAQCategory.objects.all()
    faqs = FAQ.objects.filter(is_active=True)
    category_id = request.GET.get('category')
    
    if category_id:
        faqs = faqs.filter(category_id=category_id)
    
    context = {
        'categories': categories,
        'faqs': faqs,
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'store/faq.html', context)
