from django.shortcuts import render

from apps.settings.models import Setting, FAQ
from apps.categories.models import Category
from apps.products.models import Product
from apps.carts.models import CartItem
from django.db.models import Sum

# Create your views here.
def category_index(request):
    setting = Setting.objects.latest('id')
    categories = Category.objects.all()
    faqs = FAQ.objects.all().order_by('?')[:3]
    return render(request, 'category/index.html', locals())

def category_detail(request, slug):
    setting = Setting.objects.latest('id')
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category, iiko_image__isnull=False)
    faqs = FAQ.objects.all().order_by('?')[:3]
    return render(request, 'category/detail.html', locals())