from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tracker', views.tracker,  name='tracker'),
    path('login', views.loginuser,  name='login'),
    path('logout', views.logoutuser,  name='logout'),
    path('register', views.register,  name='register'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "accounts/passwordreset.html"),  name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "accounts/passwordresetdone.html"),  name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "accounts/passwordresetconfirm.html"),  name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "accounts/passwordresetcomplete.html"),  name='password_reset_complete'),
]