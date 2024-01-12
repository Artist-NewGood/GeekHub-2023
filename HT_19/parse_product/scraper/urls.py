from django.urls import path
from scraper import views

app_name = 'scraper'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_product/', views.add_product, name='add_product'),
    path('show_all_products/<int:pk>/', views.product_data, name='product_data'),
    path('show_all_products/', views.show_all_products, name='show_all_products'),
    path('scraper/', views.scraper_data, name='scraper_data'),
    path('login/', views.login, name='login'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.show_cart, name='show_cart'),
    path('baskets/remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
    path('baskets/clear/', views.basket_clear, name='basket_clear'),
    path('change-basket-quantity/<int:product_id>/', views.change_basket_quantity, name='change_basket_quantity'),
]
