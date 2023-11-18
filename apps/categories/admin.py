from django.contrib import admin

from apps.categories.models import Category

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'iiko_image')
    search_fields = ('title', 'slug', 'iiko_image')