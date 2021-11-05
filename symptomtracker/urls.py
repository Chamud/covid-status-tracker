from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import api

urlpatterns = [
    #main URLs for pages
    path('', views.home, name='home'),
    path('profile', views.profile,  name='profile'),
    path('login', views.loginuser,  name='login'),
    path('logout', views.logoutuser,  name='logout'),
    path('register', views.register,  name='register'),
    path('edit_profile', views.edit_profile,  name='edit_profile'),
    path('tracker', views.tracker,  name='tracker'),
    path('daily_session', views.daily_session,  name='daily_session'),
    path('admin_panel', views.admin_p,  name='admin_panel'),
    path('staff_panel', views.staff_p,  name='staff_panel'),

    #Password reset URLs
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "accounts/passwordreset.html"),  name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "accounts/passwordresetdone.html"),  name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "accounts/passwordresetconfirm.html"),  name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "accounts/passwordresetcomplete.html"),  name='password_reset_complete'),

    #api calls for the mobile application
    path('api', api.apis,  name='apilist'),
    path('api/home', api.home, name='apihome'),
    path('api/profile', api.profile,  name='apiprofile'),
    path('api/map', api.map,  name='apimap'),
    path('api/register', api.register,  name='apiregister'),
    path('api/login', api.loginuser,  name='apilogin'),
    path('api/logout', api.logoutuser,  name='apilogout'),
    path('api/edit_profile', api.edit_profile,  name='apiedit_profile'),
    path('api/tracker', api.tracker,  name='apitracker'),
    path('api/daily_session', api.daily_session,  name='apidaily_session'),
    path('api/admin_panel', api.admin_p,  name='apiadmin_panel'),
    path('api/staff_panel', api.staff_p,  name='apistaff_panel'),
]
 