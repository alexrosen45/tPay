from django.shortcuts import render


def home(request):
    return render(request, "homepage/index.html", context={'signed_in': request.user.is_authenticated})