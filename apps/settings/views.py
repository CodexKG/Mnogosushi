from django.shortcuts import render, redirect
from django.core.cache import cache

from apps.settings.models import Setting, Contact
from apps.products.models import Product
from apps.billing.models import Billing, BillingProduct
from utils.iiko_menu import main

# Create your views here.
def get_cached_menu():
    cached_menu = cache.get('iiko_menu')
    if not cached_menu:
        # Загрузка данных из iiko и сохранение в кэше
        cached_menu = main() # предполагаем, что функция main() возвращает данные меню
        cache.set('iiko_menu', cached_menu, timeout=3600) # Кэширование на 1 час
    return cached_menu

def index(request):
    setting = Setting.objects.latest('id')
    products = Product.objects.all()
    # products = get_cached_menu()
    footer_products = Product.objects.filter(title__startswith='Крылышки')
    return render(request, 'index.html', locals())

def contact(request):
    setting = Setting.objects.latest('id')
    footer_products = Product.objects.filter(title__startswith='Крылышки')
    print(request.method)
    if request.method == "POST":
        print("check")
        name = request.POST.get('name')
        print(name)
        phone = request.POST.get('phone')
        print(phone)
        message = request.POST.get('message')
        if name and phone:
            print("Check")
            contact = Contact.objects.create(
                name=name,
                phone=phone,
                message=message
            )
            return redirect('confirm_contact', contact.name, contact.phone)
    return render(request, 'contacts.html', locals())

def confirm_contact(request, name, phone):
    setting = Setting.objects.latest('id')
    result = {'name':name, 'phone':phone}
    return render(request, 'billing/confirm_contact.html', locals())

def check_order(request):
    setting = Setting.objects.latest('id')
    footer_products = Product.objects.filter(title__startswith='Крылышки')
    print(request.method)
    if request.method == "POST":
        payment_code = request.POST.get('payment_code')
        try:
            billing = Billing.objects.get(payment_code=payment_code)
            try:
                products = BillingProduct.objects.filter(billing=billing.id)
            except Exception as error:
                print("Error:", error)
        except Exception as error:
            print(f"Error: {error}")
            billing = {'title':'Error'}
    return render(request, 'billing/check.html', locals())