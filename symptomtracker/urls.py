from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tracker', views.tracker,  name='tracker'),
    path('login', views.loginuser,  name='login'),
    path('logout', views.logoutuser,  name='logout'),
    path('register', views.register,  name='register'),
]