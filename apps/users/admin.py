from django.contrib import admin
from functools import update_wrapper
from weakref import WeakSet
from django.apps import apps
from django.conf import settings
from django.contrib.admin import ModelAdmin, actions
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import ModelBase
from django.http import Http404, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import NoReverseMatch, Resolver404, resolve, reverse
from django.utils.decorators import method_decorator
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string
from django.utils.text import capfirst
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.common import no_append_slash
from django.views.decorators.csrf import csrf_protect
from django.views.i18n import JavaScriptCatalog
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
import re

all_sites = WeakSet()

from django.contrib.auth import get_user_model
from apps.users.views import CustomLoginView
from apps.billing.models import Billing

User =get_user_model()

class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass                                                                    

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff and request.user.username and not request.user.is_superuser:
            # Если пользователь является персоналом сайта (is_staff = True)
            # и у него есть магазин, показываем только товары, связанные с его магазином
            qs = qs.filter(username=request.user.username)
        return qs

    # def save_model(self, request, obj, form, change):
    #     # Обновите существующий пароль, используя новый алгоритм хеширования
    #     obj.set_password(User.objects.make_random_password())
    #     super().save_model(request, obj, form, change)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        exclude_is_staff = ('password', 'is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions', 'promo_code')
        if not request.user.is_superuser:
            fields = [field for field in fields if field not in exclude_is_staff]
        return fields

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser and obj.is_staff:
            return ('date_joined', 'shop', 'user_role', 'last_login')  # Список полей, которые нужно сделать только для чтения
        return super().get_readonly_fields(request, obj)
    
admin.site.login = CustomLoginView.as_view()

