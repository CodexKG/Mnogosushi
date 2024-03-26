from django.shortcuts import render, redirect
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json

from apps.settings.models import Setting, PromoCode, FAQ
from apps.products.models import Product
from apps.carts.models import Cart, CartItem
from apps.carts.forms import AddToCartForm

# Create your views here.
@require_http_methods(["POST"])
def apply_promo_code(request):
    data = {'success': False}
    promo_code_str = request.POST.get('promo_code')
    try:
        promo_code = PromoCode.objects.get(code=promo_code_str, quantity__gt=0)
        
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        cart.discount_amount = promo_code.amount
        cart.promo_code = True
        cart.save()
        promo_code.quantity -= 1  # Decrement the available quantity
        promo_code.save()

        # Recalculate total price after applying the promo code
        cart_items = CartItem.objects.filter(cart=cart).annotate(
            total_price=ExpressionWrapper(F('product__price') * F('quantity'), output_field=DecimalField())
        )
        total_price_before_discount = cart_items.aggregate(total=Sum('total_price'))['total'] or 0
        total_price_after_discount = total_price_before_discount - cart.discount_amount
        
        data['success'] = True
        data['discount_amount'] = promo_code.amount
        data['total_price'] = total_price_after_discount
    except PromoCode.DoesNotExist:
        data['error'] = "Промокод не существует либо закончились"
    
    return JsonResponse(data)

def add_to_cart(request):
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
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
    faqs = FAQ.objects.all().order_by('?')[:3]
    session_key = request.session.session_key
    cart = Cart.objects.filter(session_key=session_key).first()
    cart_items = []
    delivery_cost = 250  # стоимость доставки
    if cart:
        cart_items = CartItem.objects.filter(cart=cart).annotate(
            total_price=ExpressionWrapper(F('product__price') * F('quantity'), output_field=DecimalField())
        )
        total_price = cart_items.aggregate(total=Sum('total_price'))['total'] or 0

        total_price -= cart.discount_amount

        if total_price < 1500:
            total_price += delivery_cost  # Добавляем стоимость доставки, если сумма заказа меньше 1500 сом
        else:
            free_delivery = True
        promo_code_error = None
        if request.method == "POST":
            promo_code_str = request.POST.get('promo_code')
            try:
                promo_code = PromoCode.objects.get(code=promo_code_str, quantity__gt=0)
                if cart:
                    cart.promo_code = True
                    cart.save()
                    promo_code.quantity -= 1
                    promo_code.save()
                total_price -= promo_code.amount
            except PromoCode.DoesNotExist:
                promo_code_error = "Invalid or expired promo code."
                print(promo_code_error)
    else:
        cart_items = []
        total_price = 0
        free_delivery = False
    return render(request, 'cart/index.html', locals())

def update_cart_item(request):
    try:
        data = json.loads(request.body)
        print(data)
        # Проверка на пустые данные
        if not data:
            return JsonResponse({'error': 'Empty request data'}, status=400)

        productId = data.get('productId')
        action = data.get('action')
        # Проверка на отсутствие необходимых ключей в данных
        if not productId or not action:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        cart = Cart.objects.filter(session_key=request.session.session_key).first()
        if not cart:
            return JsonResponse({'error': 'Cart not found'}, status=404)

        cartItem = CartItem.objects.get(cart=cart, product_id=productId)

        if action == "increase":
            cartItem.quantity += 1
        elif action == "decrease" and cartItem.quantity > 1:
            cartItem.quantity -= 1

        cartItem.save()
        total_price = cartItem.total_price()  

        # Рассчитываем итоговую цену всей корзины
        cart_items = CartItem.objects.filter(cart=cart).annotate(
            total_price=ExpressionWrapper(F('product__price') * F('quantity'), output_field=DecimalField())
        )
        cart_total_price = cart_items.aggregate(total=Sum('total_price'))['total'] or 0

        delivery_cost = 250  # Пример стоимости доставки

        if total_price < 1500:
            total_price += delivery_cost  # Добавляем стоимость доставки, если сумма заказа меньше 1500 сом
        else:
            delivery_cost = 0
            
        # Рассчитываем итоговую сумму с учетом доставки
        final_total_price = cart_total_price + delivery_cost
        return JsonResponse({
            'success': True,
            'quantity': cartItem.quantity,
            'total_price': str(total_price),
            'cart_total_price': str(cart_total_price),
            'delivery_cost': str(delivery_cost),
            'final_total_price': str(final_total_price)
        })
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Item not found in cart'}, status=404)
    except Exception as e:
        print("Error", e)
        return JsonResponse({'error': str(e)}, status=500)

def clear_cart(request):
    session_key = request.session.session_key
    if session_key:
        CartItem.objects.filter(cart__session_key=session_key).delete()

    return redirect('cart')

def remove_from_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('productId')
        session_key = request.session.session_key
        success = False
        if session_key:
            CartItem.objects.filter(cart__session_key=session_key, product__id=product_id).delete()
            success = True

        return JsonResponse({'success': success})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_items_count_processor(request):
    session_key = request.session.session_key
    if not session_key:
        return {'cart_items_count': 0}

    count = CartItem.objects.filter(cart__session_key=session_key).count()
    return {'cart_items_count': count}