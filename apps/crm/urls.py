from django.urls import path 

from apps.crm import views

urlpatterns = [
    path('', views.crm_index, name="crm_index"),
    path('tasks/', views.crm_tasks, name="crm_tasks"),
    path('login/', views.crm_login, name="crm_login"),
    #billing
    path('billing/', views.crm_index_billings, name='crm_index_billings'),
    path('billing/add/', views.crm_add_billings, name='crm_add_billings'),
    path('billing/detail/<int:id>/', views.crm_detail_billings, name="crm_detail_billings"),
    #product
    path('product/', views.crm_products, name="crm_products"),

    path('get_list_display/', views.get_list_display, name='get_list_display'),
    path('get_billing_data/', views.get_billing_data, name='get_billing_data'),
]