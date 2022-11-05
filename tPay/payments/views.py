from os import path
from urllib.request import urlopen
from django.shortcuts import redirect, render
from .models import Image

def accept_payment(request):
    return render(request, "payments/payments.html")


# Import these methods
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile


def accept_payment(request):
    context = dict()
    if request.method == 'POST':
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
    return render(request, "payments/payments.html", context=context)