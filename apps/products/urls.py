from django.urls import path 

from apps.products.views import product_detail, foods, search

urlpatterns = [
    path('<int:id>/', product_detail, name='product_detail'),
    path('foods/', foods, name='foods'),
    path('search/', search, name='search'),
]