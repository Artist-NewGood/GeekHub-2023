from django.urls import path

from basket import views
from basket import api_views

app_name = 'basket'

urlpatterns = [
    path('basket/', views.show_basket, name='show_basket'),
    path('basket/add/<int:product_id>/', views.basket_add, name='add_basket'),
    path('basket/remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
    path('basket/clear/', views.basket_clear, name='basket_clear'),
    path('basket/change_quantity/<int:product_id>/', views.change_basket_quantity, name='change_basket_quantity'),
    path('api/basket/', api_views.BasketListCreateView.as_view(), name='api_basket_list'),
    path('api/basket/<int:pk>/', api_views.BasketDetailView.as_view(), name='api_basket_detail'),
    path('api/basket/clear/', api_views.BasketClearView.as_view(), name='api_basket_clear'),
]
