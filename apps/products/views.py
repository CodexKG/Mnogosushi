from django.shortcuts import render
from django.db.models import Q

from apps.settings.models import Setting
from apps.products.models import Product

# Create your views here.
def product_detail(request, id):
    setting = Setting.objects.latest('id')
    product = Product.objects.get(id=id)
    return render(request, 'products/detail.html', locals())

def foods(request):
    setting = Setting.objects.latest('id')
    print("Setting", setting)
    products = Product.objects.all().order_by('?')
    return render(request, 'products/foods.html', locals())

def search(request):
    setting = Setting.objects.latest('id')
    query = request.POST.get('query', '')

    if query:
        # Используйте Q-объекты для выполнения поиска в моделях Shop и Product
        products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'products/foods.html', locals())