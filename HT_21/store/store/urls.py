"""
URL configuration for store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

from basket import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls', namespace='products')),
    path('basket/', include('basket.urls', namespace='basket')),
    path('users/', include('users.urls', namespace='users')),
    path('api/v1/basket/', views.BasketListCreateView.as_view(), name='api_basket_list'),
    path('api/v1/basket/<int:pk>/', views.BasketDetailView.as_view(), name='api_basket_detail'),
    path('api/v1/basket/clear/', views.BasketClearView.as_view(), name='api_basket_clear'),
]
