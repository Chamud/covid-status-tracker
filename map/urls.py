from django.urls import path
from . import views

urlpatterns = [
#URL for the map
    path('', views.map,  name='map'),
]