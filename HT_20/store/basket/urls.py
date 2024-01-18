from django.urls import path

from basket import views

app_name = 'basket'

urlpatterns = [
    path('', views.show_basket, name='show_basket'),
    path('add/<int:product_id>/', views.basket_add, name='add_basket'),
    path('remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
    path('clear/', views.basket_clear, name='basket_clear'),
    path('change_quantity/<int:product_id>/', views.change_basket_quantity, name='change_basket_quantity'),
]