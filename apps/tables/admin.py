from django.contrib import admin

from apps.tables.models import Table, TableOrder, TableOrderItem

# Register your models here.
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'created')

@admin.register(TableOrder)
class TableOrderAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'display_items', 'discount_amount', 'promo_code', 'created')

    def display_items(self, obj):
        items = obj.items.all()  # Получаем все связанные товары
        item_names = ", ".join([item.title for item in items])  # Формируем список имен товаров
        return item_names
    display_items.short_description = 'Items'

@admin.register(TableOrderItem)
class TableOrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'total', 'table')    