from django.urls import path 

from apps.crm.views import crm_index, crm_login, crm_index_billings, get_list_display, get_billing_data

urlpatterns = [
    path('', crm_index, name="crm_index"),
    path('login/', crm_login, name="crm_login"),
    path('billing/', crm_index_billings, name='crm_index_billings'),
    path('get_list_display/', get_list_display, name='get_list_display'),
    path('get_billing_data/', get_billing_data, name='get_billing_data'),
]