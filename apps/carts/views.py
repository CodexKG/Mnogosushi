from django.shortcuts import render, redirect
from django.db.models import F, ExpressionWrapper, DecimalField, Sum

from apps.settings.models import Setting
from apps.products.models import Product
from apps.carts.models import Cart, CartItem
from apps.carts.forms import AddToCartForm

# Create your views here.
def add_to_cart(request):
    print(request)
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        print(form)
        print(form.is_valid())
        print(form.data)
        # if form.is_valid():
        if True:
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

            return redirect('cart')
    
    return redirect('cart')  # Если метод запроса не POST или форма не прошла валидацию

def cart(request):
    setting = Setting.objects.latest('id')
    session_key = request.session.session_key
    cart = Cart.objects.filter(session_key=session_key).first()
    cart_items = []
    if cart:
        cart_items = CartItem.objects.filter(cart=cart).annotate(
            total_price=ExpressionWrapper(F('product__price') * F('quantity'), output_field=DecimalField())
        )
        total_price = cart_items.aggregate(total=Sum('total_price'))['total'] or 0
    else:
        cart_items = []
        total_price = 0
    # form = BillingForm()
    return render(request, 'cart/index.html', locals())

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