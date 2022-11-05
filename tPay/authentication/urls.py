from django.contrib import admin
from django.urls import path, include
from . import views

# urls for networks
urlpatterns = [
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
]