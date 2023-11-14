from django.contrib import admin
from django.contrib.admin import AdminSite
from django.apps import apps

# Register your models here.
class CustomAdminSite(AdminSite):
    # Устанавливаем кастомные заголовки
    site_header = 'Mnogosushi'
    site_title = 'Mnogosushi Admin'
    index_title = 'Mnogosushi Welcome'
    index_template = 'admin/custom_index.html'
    app_index_template = 'admin/app_index.html'
    login_template = 'admin/app_login.html'
    logout_template = 'admin/logout.html'
    password_change_template = 'admin/password_change.html'
    password_change_done_template = 'admin/password_change_done.html'

    def index(self, request, extra_context=None):
        # Получаем список всех приложений и моделей
        all_apps = apps.get_app_configs()
        app_list = []
        for app in all_apps:
            models = app.get_models()
            model_list = []
            for model in models:
                if model.__module__.startswith('apps.'):
                    model_list.append({
                        'name': model._meta.verbose_name_plural,
                        'admin_url': f'/custom/{app.label}/{model._meta.model_name}/'
                    })
            if model_list:
                app_list.append({
                    'name': app.verbose_name,
                    'models': model_list
                })

        # Если extra_context не передан, инициализируем его как пустой словарь
        if extra_context is None:
            extra_context = {}

        # Добавляем app_list к extra_context
        extra_context['app_list'] = app_list

        # Вызываем оригинальный метод index с обновленным extra_context
        return super(CustomAdminSite, self).index(request, extra_context)

custom_admin_site = CustomAdminSite(name='custom_admin')