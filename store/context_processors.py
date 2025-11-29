from .models import Cart, Category, CompanyInfo


def cart(request):
    cart_items_count = 0
    cart_total = 0
    
    if request.session.session_key:
        try:
            cart = Cart.objects.get(session_key=request.session.session_key)
            cart_items_count = cart.total_items
            cart_total = cart.total_price
        except Cart.DoesNotExist:
            pass
    
    # Получаем категории для навигации (только с slug, первые 5)
    categories = Category.objects.filter(parent=None).exclude(slug='')[:5]
    
    # Получаем текущий язык и регион из сессии
    current_language = request.session.get('language', 'ru')
    current_region = request.session.get('region', 'RU')
    
    # Получаем информацию о компании
    try:
        company_info = CompanyInfo.load()
    except Exception:
        company_info = None
    
    return {
        'cart_items_count': cart_items_count,
        'cart_total': cart_total,
        'categories': categories,
        'current_language': current_language,
        'current_region': current_region,
        'company_info': company_info,
    }
