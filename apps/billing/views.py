from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import F
import asyncio

from apps.settings.models import Setting
from apps.carts.models import Cart, CartItem
from apps.tables.models import TableOrder, TableOrderItem
from apps.billing.models import Billing, BillingProduct, BillingMenu, BillingMenuProduct
from apps.telegram.views import send_post_billing, send_post_billing_menu

# Create your views here.
def confirm(request, address, phone, payment_code):
    setting = Setting.objects.latest('id')
    result = {'address':address, 'phone':phone, 'payment_code':payment_code}
    return render(request, 'billing/confirm.html', locals())

def confirm_menu(request, payment_code):
    setting = Setting.objects.latest('id')
    result = {'payment_code':payment_code}
    return render(request, 'billing/confirm_menu.html', locals())

def create_billing_from_cart(request):
    user_cart = request.POST.get('user_cart')
    billing_receipt_type = request.POST.get('billing_receipt_type')
    print(request.POST)
    print(billing_receipt_type)
    total_price = request.POST.get('total_price')
    print(total_price)
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    payment_method = request.POST.get('payment_method')
    with transaction.atomic():
        # Создаем объект Billing
        billing = Billing.objects.create(
            billing_receipt_type=billing_receipt_type,
            total_price=total_price,
            address=address,
            phone=phone,
            payment_method=payment_method
            # Другие поля Billing могут быть заполнены здесь
        )
        # Получаем или создаем корзину для текущей сессии
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        print("MIDDLE")

        # Получаем товары из корзины пользователя
        cart = Cart.objects.get_or_create(session_key=session_key)
        print(cart)

        # Создаем BillingProduct для каждого товара в корзине
        billing_products = []
        cart_products = CartItem.objects.filter(cart__session_key=session_key)
        print(cart_products)
        for cart_item in cart_products:
            print(cart_item)
            billing_product = BillingProduct.objects.create(
                billing=billing,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.total
            )
            billing_products.append(billing_product)

        # Опционально: Очищаем корзину пользователя после создания заказа
        delete_cart = Cart.objects.get(session_key=session_key)
        delete_cart.delete()

        #Товары в список
        item_names = ", ".join([str(item.product) for item in billing_products])

        #Отправляем уведомление в группу telegram
        asyncio.run(send_post_billing(
            id=billing.id,
            products=item_names,
            payment_method=billing.payment_method,
            payment_code=billing.payment_code,
            address=billing.address,
            phone=billing.phone,
            total_price=billing.total_price
        ))

        return redirect('confirm', billing.address, billing.phone, billing.payment_code)
    
def create_billing_from_cart(request):
    user_order = request.POST.get('user_order')
    total_price = request.POST.get('total_price')
    payment_method = request.POST.get('payment_method')
    with transaction.atomic():
        # Создаем объект Billing
        billing = BillingMenu.objects.create(
            total_price=total_price,
            payment_method=payment_method
            # Другие поля Billing могут быть заполнены здесь
        )
        # Получаем или создаем корзину для текущей сессии
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        print("MIDDLE")

        # Получаем товары из корзины пользователя
        table_order = TableOrder.objects.get_or_create(session_key=session_key)
        print(table_order)

        # Создаем BillingProduct для каждого товара в корзине
        billing_products = []
        table_products = TableOrderItem.objects.filter(table__session_key=session_key)
        for cart_item in table_products:
            billing_product = BillingMenuProduct.objects.create(
                billing=billing,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.total
            )
            billing_products.append(billing_product)

        # Опционально: Очищаем корзину пользователя после создания заказа
        delete_cart = TableOrder.objects.get(session_key=session_key)
        delete_cart.delete()

        #Товары в список
        item_names = ", ".join([str(item.product) for item in billing_products])

        #Отправляем уведомление в группу telegram
        asyncio.run(send_post_billing_menu(
            id=billing.id,
            products=item_names,
            payment_method=billing.payment_method,
            payment_code=billing.payment_code,
            total_price=billing.total_price
        ))

        # return redirect('confirm', billing.address, billing.phone, billing.payment_code)
        return redirect('confirm_menu', billing.payment_code)