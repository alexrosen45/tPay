from django.shortcuts import render

def registration(request):
    return render(request, "registration/registration.html")