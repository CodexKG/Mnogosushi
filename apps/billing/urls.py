from django.urls import path 

from apps.billing.views import create_billing_from_cart, create_billing_from_order, confirm, confirm_menu, generate_pdf, order_receipt

urlpatterns = [
    path('create/', create_billing_from_cart, name="create_billing"),
    path('create/menu/', create_billing_from_order, name="create_billing_from_order"),
    path('confirm/<str:address>/<str:phone>/<str:payment_code>/', confirm, name='confirm'),
    path('confirm/<str:payment_code>/', confirm_menu, name='confirm_menu'),
    path('generate_pdf/<int:payment_code>/', generate_pdf, name='generate_pdf'),
    path('receipt/<int:payment_code>/', order_receipt, name='order_receipt')
]