from django.shortcuts import render

from apps.settings.models import Setting
from apps.categories.models import Category
from apps.products.models import Product
from apps.carts.models import CartItem
from django.db.models import Sum

# Create your views here.
def category_detail(request, slug):
    setting = Setting.objects.latest('id')
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)


    return render(request, 'category/detail.html', locals())