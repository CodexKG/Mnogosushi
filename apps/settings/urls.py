from django.urls import path 

from apps.settings.views import index, contact, confirm_contact, check_order

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('confirm_contact/<str:name>/<str:phone>/', confirm_contact, name='confirm_contact'),
    path('check/', check_order, name='check_order')
]