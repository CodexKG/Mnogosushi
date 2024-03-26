from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.contrib import admin
import traceback

from apps.billing.models import Billing
from apps.users.models import User
from apps.settings.models import Setting

# Create your views here.
def crm_index(request):
    setting = Setting.objects.latest('id')
    if not request.user.is_authenticated:
        return redirect('crm_login')
    return render(request, 'crm/index.html')

def crm_login(request):
    setting = Setting.objects.latest('id')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('crm_index')
        except:
            return redirect('user_not_found')
    return render(request, 'crm/user/login.html', locals())

@staff_member_required
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