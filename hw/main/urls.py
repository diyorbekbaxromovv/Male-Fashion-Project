from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path
from . import views


PasswordChangeView 




urlpatterns = [
    path('', views.index , name='index'),
    path('shop/', views.shop, name='shop'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.ProfileUserView.as_view(), name='profile'),
    path('shop/', views.shop, name='shop'),
    path('details/<int:id>', views.details, name='details'),
    path('category/<int:id>', views.category, name='category'),
    path('password-change/', views.UserPasswordChangeView.as_view(), name='password-change'),
    path('password-change/', PasswordChangeDoneView.as_view(template_name='main/password_change_done.html'), name='password_change_done'),
    path('about/', views.about, name='about'),
    
]
