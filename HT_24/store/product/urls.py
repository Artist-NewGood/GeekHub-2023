from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product import views
from product import api_views

app_name = 'product'

router = DefaultRouter()
router.register(r'products', api_views.ProductViewSet)
router.register(r'categories', api_views.CategoryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index, name='index'),
    path('add-product/', views.add_product, name='add_product'),
    path('scraper_product/', views.scraper_product, name='scraper_product'),
    path('show-all-products/', views.show_all_products, name='show_all_products'),
    path('show-all-products/page/<int:page_number>/', views.show_all_products, name='paginator'),
    path('category/<str:category_name>/', views.show_all_products, name='category'),
    path('detail-product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('save-edit-product/<int:product_id>/', views.save_edit_product, name='save_edit_product'),
    path('delete/<int:product_id>/', views.del_products, name='del_products'),
]
