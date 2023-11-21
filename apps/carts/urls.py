from django.urls import path
from apps.carts import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]