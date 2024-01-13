from django.contrib import admin

from apps.carts.models import Cart, CartItem

# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'display_items', 'discount_amount', 'promo_code', 'created')

    def display_items(self, obj):
        items = obj.items.all()  # Получаем все связанные товары
        item_names = ", ".join([item.title for item in items])  # Формируем список имен товаров
        return item_names
    display_items.short_description = 'Items'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'total', 'cart')