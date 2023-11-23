from django.urls import path 

from apps.tables.views import menu, add_to_order, table_clear_cart, table_remove_from_cart, table_update_cart_item  , order, category_menu_detail


urlpatterns = [
    path('<int:table_uuid>/', menu, name='menu'),
    path('<int:table_uuid>/<slug:category_slug>/', category_menu_detail, name="category_menu_detail"),
    path('order/<int:table_uuid>/', order, name="order"),
    path('add_to_order/', add_to_order, name='add_to_order'),
    path('clear_cart/', table_clear_cart, name='table_clear_cart'),
    path('remove_from_cart/<int:product_id>/<int:table_uuid>/', table_remove_from_cart, name='table_remove_from_cart'),
    path('update_item/', table_update_cart_item, name='table_update_cart_item')
]