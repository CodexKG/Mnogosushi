from django.shortcuts import render
from django.db.models import Q, F, ExpressionWrapper, DecimalField, Sum

from apps.settings.models import Setting
from apps.products.models import Product
from apps.carts.models import Cart, CartItem

# Create your views here.
def product_detail(request, id):
    setting = Setting.objects.latest('id')
    product = Product.objects.get(id=id)
    random_products = Product.objects.all().order_by('?')[:3]
    footer_products = Product.objects.filter(title__startswith='Крылышки')
    session_key = request.session.session_key
    cart = Cart.objects.filter(session_key=session_key).first()
    cart_items = []
    delivery_cost = 250  # стоимость доставки
    if cart:
        cart_items = CartItem.objects.filter(cart=cart).annotate(
            total_price=ExpressionWrapper(F('product__price') * F('quantity'), output_field=DecimalField())
        )
        total_price = cart_items.aggregate(total=Sum('total_price'))['total'] or 0

        if total_price < 1500:
            total_price += delivery_cost  # Добавляем стоимость доставки, если сумма заказа меньше 1500 сом
        else:
            free_delivery = True
    else:
        cart_items = []
        total_price = 0
        free_delivery = False
    return render(request, 'products/detail.html', locals())

def foods(request):
    setting = Setting.objects.latest('id')
    print("Setting", setting)
    products = Product.objects.all().order_by('?')
    footer_products = Product.objects.filter(title__startswith='Крылышки')
    return render(request, 'products/foods.html', locals())

def search(request):
    setting = Setting.objects.latest('id')
    footer_products = Product.objects.filter(title__startswith='Крылышки')
    query = request.POST.get('query', '')
    if query:
        # Используйте Q-объекты для выполнения поиска в моделях Shop и Product
        products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'products/foods.html', locals())