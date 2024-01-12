from django.contrib import admin

from apps.settings.models import Setting, Contact, FAQ, Promotions

# Register your models here.
@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')

@admin.register(Promotions)
class PromotionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'url')