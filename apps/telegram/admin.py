from django.contrib import admin

from apps.telegram.models import TelegramUser, BillingDelivery, BillingDeliveryHistory, TechnicalSupport

# Register your models here.
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'user_id', 'user_role', 'created')
    search_fields = ('username', 'first_name', 'last_name', 'user_id', 'user_role', 'created')

class BillingDeliveryHistoryTabularInline(admin.TabularInline):
    model = BillingDeliveryHistory
    extra = 0
    
@admin.register(BillingDelivery)
class BillingDeliveryAdmin(admin.ModelAdmin):
    list_display = ('billing', 'telegram_user', 'delivery', 'created')
    inlines = [BillingDeliveryHistoryTabularInline]


@admin.register(BillingDeliveryHistory)
class BillingDeliveryHistoryAdmin(admin.ModelAdmin):
    list_display = ('delivery', 'message', 'created')

@admin.register(TechnicalSupport)
class TechnicalSupportAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_user_id', 'message', 'support_operator', 'created', 'support_assessment', 'status', 'id')

    def get_username(self, obj):
        return obj.user.username if obj.user else None
    get_username.admin_order_field  = 'user'  # Allows column order sorting
    get_username.short_description = 'Username'  # Renames column head

    def get_user_id(self, obj):
        return obj.user.user_id if obj.user else None
    get_user_id.admin_order_field  = 'user'
    get_user_id.short_description = 'User ID'