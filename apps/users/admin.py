from django.contrib import admin

from apps.users.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name']

    def save_model(self, request, obj, form, change):
        # Если пароль не хэширован, установите новый случайный пароль и хешируйте его перед сохранением
        if not obj.password.startswith('pbkdf2_'):
            obj.set_password(User.objects.make_random_password())
        super().save_model(request, obj, form, change)