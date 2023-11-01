from django.shortcuts import render, redirect
from django.db.models import F, ExpressionWrapper, DecimalField, Sum

from apps.settings.models import Setting
from apps.tables.models import Table, TableOrder, TableOrderItem
from apps.tables.forms import AddToOrderForm
from apps.products.models import Product
from django.http import JsonResponse

# Create your views here.
def menu(request, table_uuid):
    table = Table.objects.get(number=table_uuid)
    setting = Setting.objects.latest('id')
    products = Product.objects.all()
    return render(request, 'menu/index.html', locals())

def add_to_order(request):
    print("add to order")
    print(request.method)
    if request.method == 'POST':
        form = AddToOrderForm(request.POST)
        if form.is_valid():
            table_uuid = form.cleaned_data['table_uuid']
            product_id = form.cleaned_data['product_id']
            print("WORK",product_id)
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            print(type(price))
            product = Product.objects.get(id=product_id)

            # Получаем или создаем корзину для текущей сессии
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key

            table_instance = Table.objects.get(number=table_uuid)
            table, _ = TableOrder.objects.get_or_create(session_key=session_key, menu_table=table_instance)

            # Получаем объект CartItem по cart и product
            table_item = TableOrderItem.objects.filter(table=table, product=product).first()

            # Если CartItem существует, обновляем его количество, иначе создаем новый объект
            if table_item:
                print(table_item.total + price)
                table_item.total += price * quantity
                table_item.quantity += quantity
                table_item.save()
            else:
                table_item = TableOrderItem.objects.create(table=table, product=product, quantity=quantity, total=price * quantity)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    return redirect('order')

def order(request):
    setting = Setting.objects.latest('id')
    session_key = request.session.session_key
    order = TableOrder.objects.filter(session_key=session_key).first()
    cart_items = []
    if order:
        cart_items = TableOrderItem.objects.filter(table=order).annotate(
            total_price=ExpressionWrapper(F('product__price') * F('quantity'), output_field=DecimalField())
        )
        total_price = cart_items.aggregate(total=Sum('total_price'))['total'] or 0
    else:
        cart_items = []
        total_price = 0
    form = AddToOrderForm()
    return render(request, 'menu/order.html', locals())

def clear_order(request):
    session_key = request.session.session_key
    if session_key:
        TableOrderItem.objects.filter(cart__session_key=session_key).delete()

    return redirect('cart')

def remove_from_order(request, product_id):
    session_key = request.session.session_key
    if session_key:
        TableOrderItem.objects.filter(cart__session_key=session_key, product__id=product_id).delete()

    return redirect('cart')