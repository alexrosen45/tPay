from os import path
from urllib.request import urlopen
from django.shortcuts import redirect, render
from .models import Image
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.views.decorators.http import require_POST


@login_required(login_url="/signin")
def accept_payment(request):
    return render(request, "payments/select_food.html")


@login_required(login_url="/signin")
@require_POST
def authenticate_face(request):
    context = {'signed_in': request.user.is_authenticated, 'food_item': request.POST["food_item"]}
    if request.method == 'POST':
        try:
            username = request.POST["username"]
            image_path = request.POST["src"]
            image = NamedTemporaryFile()
            image.write(urlopen(path).read())
            image.flush()
            image = File(image)
            name = str(image.name).split('\\')[-1]
            name += '.jpg'  # store image in jpeg format
            image.name = name
            if image is not None:
                obj = Image.objects.create(username=username, image=image)  # create a object of Image type defined in model
                obj.save()
                context["path"] = obj.image.url
                context["username"] = obj.username
            else :
                return redirect('/')
            return redirect('home')
        except:
            pass
    return render(request, "payments/payments.html", context=context)