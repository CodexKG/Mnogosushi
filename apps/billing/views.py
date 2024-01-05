from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.db import transaction
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from io import BytesIO
import asyncio

from apps.settings.models import Setting
from apps.carts.models import Cart, CartItem
from apps.tables.models import Table, TableOrder, TableOrderItem
from apps.billing.models import Billing, BillingProduct
from apps.telegram.views import send_post_billing, send_post_billing_menu
from apps.billing.admin import export_to_excel

# Create your views here.
@staff_member_required
def export_billings_to_excel_view(request):
    queryset = Billing.objects.all()
    return export_to_excel(None, request, queryset)

def confirm(request, address, phone, payment_code):
    setting = Setting.objects.latest('id')
    billing = Billing.objects.get(payment_code=payment_code)
    try:
        products = BillingProduct.objects.filter(billing=billing.id)
    except Exception as error:
        print("Error:", error)
    result = {'address':address, 'phone':phone, 'payment_code':payment_code}
    return render(request, 'billing/confirm.html', locals())

def confirm_menu(request, payment_code, table_number):
    setting = Setting.objects.latest('id')
    table = Table.objects.get(number=table_number)
    result = {'payment_code':payment_code}
    billing = Billing.objects.get(payment_code=payment_code)
    try:
        products = BillingProduct.objects.filter(billing=billing.id)
    except Exception as error:
        print("Error:", error)
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
    delivery_price = request.POST.get('delivery_price') or 0

    with transaction.atomic():
        # Создаем объект Billing
        billing = Billing.objects.create(
            billing_receipt_type=billing_receipt_type,
            total_price=total_price,
            address=address,
            phone=phone,
            payment_method=payment_method,
            delivery_price=delivery_price
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

        # Товары в список
        item_descriptions = [f"{item.product} ({item.quantity} шт)" for item in billing_products]
        formatted_items = "\n".join(item_descriptions)

        # Отправляем уведомление в группу telegram
        asyncio.run(send_post_billing(
            id=billing.id,
            products=formatted_items,
            payment_method=billing.payment_method,
            payment_code=billing.payment_code,
            address=billing.address,
            phone=billing.phone,
            delivery_price=billing.delivery_price,
            total_price=billing.total_price,
            billing_receipt_type=billing.billing_receipt_type
        ))

        return redirect('confirm', billing.address, billing.phone, billing.payment_code)
    
def create_billing_from_order(request):
    total_price = request.POST.get('total_price')
    payment_method = request.POST.get('payment_method')
    table_uuid = request.POST.get('table_uuid')
    table_title = request.POST.get('table_title')
    print("TABLE:", table_uuid)
    with transaction.atomic():
        # Создаем объект Billing
        billing = Billing.objects.create(
            billing_receipt_type='Меню',
            total_price=total_price,
            address='​Токтогула 90 (Меню)',
            phone='Заказ из меню',
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
            billing_product = BillingProduct.objects.create(
                billing=billing,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.total
            )
            billing_products.append(billing_product)

        # Опционально: Очищаем корзину пользователя после создания заказа
        delete_cart = TableOrder.objects.get(session_key=session_key)
        delete_cart.delete()

        # Товары в список
        item_descriptions = [f"{item.product} ({item.quantity} шт)" for item in billing_products]
        formatted_items = "\n".join(item_descriptions)

        #Отправляем уведомление в группу telegram
        asyncio.run(send_post_billing_menu(
            id=billing.id,
            table_uuid=table_uuid,
            table_title=table_title,
            products=formatted_items,
            payment_method=billing.payment_method,
            payment_code=billing.payment_code,
            total_price=billing.total_price
        ))

        # return redirect('confirm', billing.address, billing.phone, billing.payment_code)
        return redirect('confirm_menu', billing.payment_code, table_uuid)
    
def order_receipt(request, payment_code):
    setting = Setting.objects.latest('id')
    try:
        billing = Billing.objects.get(payment_code=payment_code)
        products = BillingProduct.objects.filter(billing=billing.id)
    except Exception as error:
        print(error)
    return render(request, 'billing/order_receipt.html', locals())

def generate_pdf(request, payment_code):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{payment_code}.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    billing = Billing.objects.get(payment_code=payment_code)

    # Добавляем изображение в PDF
    image_path = 'https://img.freepik.com/premium-vector/blank-bank-check-checkbook-cheque-pay-template_8071-12524.jpg'
    image = Image(image_path, width=300, height=200)
    elements.append(image)

    # Создаем абзац для текста о биллинге
    billing_text = f"""
    Вид получения товара: {billing.billing_receipt_type}
    Итоговая цена товаров: {billing.total_price} руб.
    Адрес доставки: {billing.address}
    Номер телефона: {billing.phone}
    Способ оплаты: {billing.payment_method}
    Код оплаты биллинга: {billing.payment_code}
    Статус заказа: {billing.status}
    Дата создания биллинга: {billing.created}
    """.encode('utf-8')

    billing_paragraph = Paragraph(billing_text, styles['Normal'])
    elements.append(billing_paragraph)

    # Создаем абзац для продуктов биллинга
    products_text = "Продукты биллинга:\n"
    for product in BillingProduct.objects.filter(billing=billing):
        products_text += f"{product.product} - {product.quantity} шт.\n"
    products_paragraph = Paragraph(products_text.encode('utf-8'), styles['Normal'])
    elements.append(products_paragraph)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response