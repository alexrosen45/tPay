from django.contrib import admin
from django.urls import path, include
from . import views

# urls for networks
urlpatterns = [
    path('accept_payment', views.accept_payment, name="accept_payment"),
    path('authenticate_face', views.authenticate_face, name="authenticate_face"),
]