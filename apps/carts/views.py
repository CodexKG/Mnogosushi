from django.shortcuts import render, redirect
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json

from apps.settings.models import Setting
from apps.products.models import Product
from apps.carts.models import Cart, CartItem
from apps.carts.forms import AddToCartForm


from django.shortcuts import redirect
from django.http import JsonResponse
# ... другие импорты ...

# Create your views here.
def add_to_cart(request):
    print(request.META.get('HTTP_REFERER'))
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        print(form)
        print(form.is_valid())
        print(form.data)
        if form.is_valid():
        # if True:
            product_id = form.cleaned_data['product_id']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            product = Product.objects.get(id=product_id)

            # Получаем или создаем корзину для текущей сессии
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key

            cart, _ = Cart.objects.get_or_create(session_key=session_key)

            # Получаем объект CartItem по cart и product
            cart_item = CartItem.objects.filter(cart=cart, product=product).first()

            # Если CartItem существует, обновляем его количество, иначе создаем новый объект
            if cart_item:
                cart_item.total += price * quantity
                cart_item.quantity += quantity
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity, total=price * quantity)

            total_items_count = CartItem.objects.filter(cart__session_key=session_key).count()

            if 'product' in str(request.META.get('HTTP_REFERER')):
                return redirect('cart')
            else:
                return JsonResponse({'success': True, 'total_items': total_items_count})
    
    return redirect('cart')  # Если метод запроса не POST или форма не прошла валидацию

def cart(request):
    setting = Setting.objects.latest('id')
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
    return render(request, 'cart/index.html', locals())

def update_cart_item(request):
    try:
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']

        cart = Cart.objects.filter(session_key=request.session.session_key).first()
        if not cart:
            return JsonResponse({'error': 'Cart not found'}, status=404)

        cartItem = CartItem.objects.get(cart=cart, product_id=productId)

        if action == "increase":
            cartItem.quantity += 1
        elif action == "decrease" and cartItem.quantity > 1:
            cartItem.quantity -= 1

        cartItem.save()
        return JsonResponse({'success': True})

    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Item not found in cart'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def clear_cart(request):
    session_key = request.session.session_key
    if session_key:
        CartItem.objects.filter(cart__session_key=session_key).delete()

    return redirect('cart')

def remove_from_cart(request, product_id):
    session_key = request.session.session_key
    if session_key:
        CartItem.objects.filter(cart__session_key=session_key, product__id=product_id).delete()

    return redirect('cart')

def cart_items_count_processor(request):
    session_key = request.session.session_key
    if not session_key:
        return {'cart_items_count': 0}

    count = CartItem.objects.filter(cart__session_key=session_key).count()
    return {'cart_items_count': count}