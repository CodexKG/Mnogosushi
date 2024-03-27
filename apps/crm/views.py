from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.contrib import admin
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime, timedelta, date
import traceback

from apps.billing.models import Billing
from apps.settings.models import Setting

# Create your views here.
@staff_member_required(login_url='/admin/login/')
def crm_index(request):
    setting = Setting.objects.latest('id')
    today = datetime.today().date()  # Сегодняшняя дата без времени
    end_date = today  # Конец интервала — сегодняшний день
    start_date = today - timedelta(days=6)  # Начало интервала — 7 дней назад от сегодняшнего дня

    date_range = request.GET.get('CRMDateRange', '')
    if date_range:
        # Парсим дату с учетом текущего года
        dates = [datetime.strptime(date + f" {today.year}", '%b %d %Y').date() for date in date_range.split(' to ')]
        start_date = dates[0]
        end_date = dates[1] if len(dates) > 1 else end_date
    
    # Проверка, что дата начала не позднее даты окончания
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    billing_queryset = Billing.objects.filter(created__date__range=(start_date, end_date))
    total_billing_price = billing_queryset.aggregate(total=Sum('total_price'))['total'] or 0
    total_billings_count = billing_queryset.count()

    # Расчет для предыдущего периода (за 7 дней до выбранного диапазона)
    previous_start_date = start_date - timedelta(days=7)
    previous_end_date = start_date - timedelta(days=1)  # День перед началом текущего периода

    # Получаем данные за предыдущий период
    previous_billing_queryset = Billing.objects.filter(created__date__range=(previous_start_date, previous_end_date))
    total_billing_price_previous = previous_billing_queryset.aggregate(total=Sum('total_price'))['total'] or 0

    # Расчет процентного изменения
    percentage_change = (total_billing_price - total_billing_price_previous) / total_billing_price_previous * 100 if total_billing_price_previous else 0

    # Форматирование дат для отображения
    default_start_date = start_date.strftime('%b %d')
    default_end_date = end_date.strftime('%b %d')
    
    return render(request, 'crm/index.html', locals())

def crm_login(request):
    setting = Setting.objects.latest('id')  
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('crm_index')
        else:
            return redirect('user_not_found')
    return render(request, 'crm/user/login.html', locals())

@staff_member_required(login_url='/admin/login/')
def crm_index_billings(request):
    setting = Setting.objects.latest('id')
    return render(request, 'crm/billing/index.html', {'setting': setting})

def get_list_display(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    # Определяем модель Billing
    model_admin = admin.site._registry[Billing]
    
    # Получаем текущие значения list_display
    list_display = model_admin.get_list_display(request)
    
    return JsonResponse({'list_display': list_display})
    
def get_billing_data(request):
    try:
        # Определяем поля, которые мы хотим отправить
        fields = ['total_price', 'first_name', 'last_name', 'payment_code', 'billing_receipt_type', 'status']
        # Получаем данные биллингов
        billings = Billing.objects.all().values(*fields)
        # Также отправляем список полей для отображения
        return JsonResponse({
            'billings': list(billings),
            'fields': fields,
            'field_names': {  # Передаем переводы полей на фронд
                'total_price': 'Итоговая цена',
                'first_name': 'Имя',
                'last_name': 'Фамилия',
                'payment_code': 'Код оплаты',
                'billing_receipt_type': 'Тип квитанции',
                'status': 'Статус',
            }
        })
    except Exception as e:
        print("Error", e)
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)