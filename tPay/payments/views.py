from os import path
from urllib.request import urlopen
from django.shortcuts import redirect, render
from .models import Image
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile


@login_required(login_url="/signin")
def accept_payment(request):
    context = {'signed_in': request.user.is_authenticated}
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