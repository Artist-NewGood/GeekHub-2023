from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('users/login/', views.login_view, name='login'),
    path('users/logout/', views.logout, name='logout'),
]
