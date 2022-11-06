from os import path
from urllib.request import urlopen
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings 
import tensorflow as tf
from tensorflow.compat.v1.keras.backend import set_session
import keras
print(keras.__version__)
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from keras.applications.imagenet_utils import decode_predictions
import numpy as np
# from keras.applications import vgg16
import datetime
import traceback
from PIL import Image, ImageOps #Install pillow instead of PIL
import numpy as np
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from os import path
from urllib.request import urlopen
from django.shortcuts import redirect, render
from payments import models
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.views.decorators.http import require_POST
from io import BytesIO
import base64
from registration.models import Person
from .models import Item, PaymentRecord


@login_required(login_url="/signin")
def accept_payment(request):
    food_items = [food_item.item for food_item in Item.objects.all()]
    context = {'signed_in': request.user.is_authenticated, 'food_items': food_items}
    return render(request, "payments/select_food.html", context=context)


@login_required(login_url="/signin")
@require_POST
def authenticate_face(request):
    context = {'signed_in': request.user.is_authenticated, 'food_item': request.POST["food_item"]}
    if request.method == 'POST':
        try:
            file_url = request.POST["img_url"]

            # get model
            vgg16 = keras.models.load_model("classify/model.savedmodel")

            # f=request.FILES['sentFile'] # here you get the files needed
            response = {}
            # file_name = "pic.jpg"
            # file_name_2 = default_storage.save(file_name, f)
            file_url = file_url.split("base64,")[1]
            print(file_url)
            # file_url = file_url[1:]
            # original = load_img(file_url, target_size=(224, 224))
            # numpy_image = img_to_array(original)
            
            # class_names = open('classify/labels.txt', 'r').readlines()
            # class_names = [person for person in Person._meta.get_fields()]
            people = Person.objects.all()
            class_names = []
            for person in people:
                if person.label_number != -1:
                    class_names.append(person.first_name)
            

            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

            # Replace this with the path to your image
            # image = Image.open(file_url).convert('RGB')
            image = Image.open(BytesIO(base64.b64decode(file_url)))
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

            # Load the image into the array
            data[0] = normalized_image_array

            # run the inference
            prediction = vgg16.predict(data)
            index = np.argmax(prediction)
            predictions = class_names[index]
            confidence_score = prediction[0][index]

            # image_batch = np.expand_dims(numpy_image, axis=0)
            # # prepare the image for the VGG model
            # processed_image = vgg16.preprocess_input(image_batch.copy())
            
            # # get the predicted probabilities for each class
            # with settings.GRAPH1.as_default():
            #     set_session(settings.SESS)
            #     predictions=settings.VGG_MODEL.predict(processed_image)
        
            # label = decode_predictions(predictions)
            # label = list(label)[0]
            
            # accept accuracy greater than of equal to 95%
            print(str(confidence_score))
            print(str(predictions))
            if confidence_score > 0.85 and predictions not in ["invalid", "blank"]:
                response['name'] = str(predictions)
                print(context['food_item'])

                student = Person.objects.get(first_name=response['name'])
                item = Item.objects.get(item=context['food_item'])
                purchase = PaymentRecord(student_number=student.student_number, item=item.item, price_in_cents_cad=item.price_in_cents_cad)
                purchase.save() # save purchase

                return render(request, "payments/verify.html", response)
            else:
                food_items = [food_item.item for food_item in Item.objects.all()]
                return render(request, "payments/select_food.html", context={'error' : True, 'food_items': food_items})
        except:
            pass
        return render(request, "payments/payments.html", context=context)
        
    return render(request, "payments/payments.html", context=context)