from django.shortcuts import render, redirect
from django.http import HttpResponseServerError
from django.db.models import Case, When, Value, IntegerField
import traceback

from apps.settings.models import Setting, Contact
from apps.products.models import Product
from apps.billing.models import Billing, BillingProduct
from apps.categories.models import Category

# Create your views here.
def index(request):
    setting = Setting.objects.latest('id')
    categories = Category.objects.annotate(
        sort_priority=Case(
            When(priority=0, then=Value(9999)),
            default='priority',
            output_field=IntegerField()
        )
    ).order_by('sort_priority')
    products = Product.objects.all()
    footer_products = Product.objects.filter(title__startswith='Крылышки')
    popular_products = Product.objects.all().order_by("?")[:6]
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

def page_404(request, exception):
    setting = Setting.objects.latest('id')
    return render(request, 'error/404.html', locals(), status=404)

def page_500(request):
    setting = Setting.objects.latest('id')
    error_log = traceback.format_exc()
    return HttpResponseServerError(render(request, 'error/500.html', {"error_log": error_log}))