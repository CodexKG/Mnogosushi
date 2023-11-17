from django.contrib import admin
from rangefilter.filter import DateRangeFilter

from apps.billing.admin import CustomDateFieldListFilter
from apps.products.models import Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'image', 'created')
    search_fields = ('title', 'description', 'created')
    list_filter = (('created', DateRangeFilter), ('created', CustomDateFieldListFilter),)  # Добавляем фильтр по дате