from django.contrib import admin
from django.urls import path, include
from . import views

# urls for networks
urlpatterns = [
    path('home', views.home, name="home"),
]