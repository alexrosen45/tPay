from django.shortcuts import redirect, render
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings 
import tensorflow.compat.v1 as tf
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
from payments.models import Image
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.views.decorators.http import require_POST


@require_POST
@login_required(login_url="/signin")
def verify(request):
    context = {'signed_in': request.user.is_authenticated, 'food_item': 'pasta'} #request.POST["food_item"]
    if  request.method == "POST":
        vgg16 = keras.models.load_model("classify/keras_model.h5")

        # f=request.FILES['sentFile'] # here you get the files needed
        response = {}
        # file_name = "pic.jpg"
        # file_name_2 = default_storage.save(file_name, f)
        file_url = request.POST["img_url"]
        # file_url = file_url[1:]
        original = load_img(file_url, target_size=(224, 224))
        numpy_image = img_to_array(original)
        
        class_names = open('classify/labels.txt', 'r').readlines()
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Replace this with the path to your image
        image = Image.open(file_url).convert('RGB')
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
        
        # accept accuracy greater than of equal to 65%
        if confidence_score > 0.65:
            response['name'] = str(predictions)
            return render(request, "payments/verify.html", response)
        else:
            return redirect("home")
    else:
        return render(request, "payments/verify.html")