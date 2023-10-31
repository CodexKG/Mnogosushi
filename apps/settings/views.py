from django.shortcuts import render, redirect

from apps.settings.models import Setting, Contact
from apps.products.models import Product

# Create your views here.
def index(request):
    setting = Setting.objects.latest('id')
    products = Product.objects.all()
    footer_products = Product.objects.filter(title__startswith='Крылышки')
    return render(request, 'index.html', locals())

def contact(request):
    setting = Setting.objects.latest('id')
    footer_products = Product.objects.filter(title__startswith='Крылышки')
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        if name and phone and message:
            contact = Contact.objects.create(
                name=name,
                phone=phone,
                message=message
            )
            return redirect('index')
    return render(request, 'contacts.html', locals())