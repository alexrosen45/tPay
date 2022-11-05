from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout


def signin(request):
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        # create user object from form data
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # send user to page after valid signin
            # send username and password for automatic signin in new directory
            return redirect('home')
        else:
            return render(request, "authentication/signin.html", context={
                'is_error': True,
                'error': "Invalid credentials"
            })

    return render(request, "authentication/signin.html")