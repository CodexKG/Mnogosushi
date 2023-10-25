from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from datetime import date, timedelta
from django.utils.translation import gettext as _
from django.db.models import Sum, Count, F
from mptt.admin import MPTTModelAdmin

from apps.billing.models import Billing, BillingProduct, SaleSummary, BillingMenu, BillingMenuProduct

# Register your models here.
class CustomDateFieldListFilter(admin.DateFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.title = _('Дата')
        self.links = (
            (_('Сегодня'), {
                self.lookup_kwarg_since: str(date.today()),
            }),
            (_('Вчера'), {
                self.lookup_kwarg_since: str(date.today() - timedelta(days=1)),
                self.lookup_kwarg_until: str(date.today() - timedelta(days=1)),
            }),
            (_('Последние 7 дней'), {
                self.lookup_kwarg_since: str(date.today() - timedelta(days=7)),
            }),
            (_('Последние 30 дней'), {
                self.lookup_kwarg_since: str(date.today() - timedelta(days=30)),
            }),
        )


class ProductTabularInline(admin.TabularInline):
    model = BillingProduct
    extra = 0


@admin.register(SaleSummary)
class SaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/sale_summary_change_list.html'
    date_hierarchy = 'created'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'title': F('billing_products__product__title'),  # Замените 'billing__title' на фактический путь к полю 'title' в модели BillingProduct
            'total': F('billing_products__quantity'),
            'total_sales': Sum('billing_products__price'),
            'payment_method': F('payment_method'),
        }

        response.context_data['summary'] = list(
            qs.values('billing_products').annotate(**metrics).order_by('-created')
        )
        print(response)
        print(metrics)

        ################################
        total_metrics = {
            'title': Sum('billing_products__product__title'),  # Замените 'billing__title' на фактический путь к полю 'title' в модели BillingProduct
            'total': Sum('billing_products__quantity'),
            'total_sales': Sum('billing_products__price'),
            'payment_method': Count('payment_method'),
        }

        response.context_data['summary_total'] = dict(
            qs.aggregate(**total_metrics)
        )

        return response
    
    def get_next_in_date_hierarchy(request, date_hierarchy):
        if date_hierarchy + '__day' in request.GET:
            return 'hour'

        if date_hierarchy + '__month' in request.GET:
            return 'day'

        if date_hierarchy + '__year' in request.GET:
            return 'week'

        return 'month'


@admin.register(Billing)
class BillingAdmin(MPTTModelAdmin):
    list_display = ('id', 'total_price', 'address', 'payment_method', 'phone', 'billing_receipt_type', 'payment_code', 'created', 'status')
    search_fields = ('id', 'total_price', 'address', 'payment_method', 'phone', 'billing_receipt_type', 'payment_code', 'created', 'status')
    inlines = [ProductTabularInline]
    list_filter = (('created', DateRangeFilter), ('created', CustomDateFieldListFilter),)  # Добавляем фильтр по дате


@admin.register(BillingProduct)
class BillingProductAdmin(admin.ModelAdmin):
    list_display = ('billing', 'product', 'quantity', 'price', 'status')
    list_filter = (('created', DateRangeFilter), ('created', CustomDateFieldListFilter),)  # Добавляем фильтр по дате

class BillingProductTabularInline(admin.TabularInline):
    model = BillingMenuProduct
    extra = 0

@admin.register(BillingMenu)
class BillingMenuAdmin(MPTTModelAdmin):
    list_display = ('id', 'total_price', 'payment_method', 'payment_code', 'created', 'status')
    search_fields = ('id', 'total_price', 'payment_method', 'payment_code', 'created', 'status')
    inlines = [BillingProductTabularInline]
    list_filter = (('created', DateRangeFilter), ('created', CustomDateFieldListFilter),)  # Добавляем фильтр по дате


@admin.register(BillingMenuProduct)
class BillingMenuProductAdmin(admin.ModelAdmin):
    list_display = ('billing', 'product', 'quantity', 'price', 'status')
    list_filter = (('created', DateRangeFilter), ('created', CustomDateFieldListFilter),)  # Добавляем фильтр по дате
