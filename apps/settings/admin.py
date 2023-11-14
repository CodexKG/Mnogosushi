from django.contrib import admin

from apps.settings.models import Setting, Contact

# Register your models here.
@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    change_form_template = 'admin/settings.html'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created')