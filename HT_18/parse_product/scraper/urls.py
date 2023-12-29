from django.urls import path
from scraper import views

app_name = 'scraper'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_product/', views.add_product, name='add_product'),
    path('show_all_products/<int:pk>/', views.product_data, name='product_data'),
    path('show_all_products/', views.show_all_products, name='show_all_products'),
    path('scraper/', views.scraper_data, name='scraper_data'),
    path('cart/', views.cart, name='cart'),
    path('login/', views.login, name='login'),
]
