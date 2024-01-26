from django.contrib import admin

from apps.settings.models import Setting, SettingCity, Contact, FAQ, Promotions, PromoCode

# Register your models here.
class SettingCityTabularInline(admin.TabularInline):
    model = SettingCity
    extra = 1

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    inlines = (SettingCityTabularInline, )

@admin.register(SettingCity)
class SettingCityAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')

@admin.register(Promotions)
class PromotionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'url')

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'quantity', 'amount', 'title')
    search_fields = ('code', 'quantity', 'amount', 'title')