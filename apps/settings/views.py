from django.shortcuts import render, redirect
from django.core.cache import cache

from apps.settings.models import Setting, Contact
from apps.products.models import Product
from apps.billing.models import Billing, BillingProduct
from apps.categories.models import Category

# Create your views here.
def index(request):
    setting = Setting.objects.latest('id')
    categories = Category.objects.all().order_by("?")
    products = Product.objects.all()
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