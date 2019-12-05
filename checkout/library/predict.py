import base64
from PIL import Image
import numpy as np
import io
import keras
import tensorflow as tf
import keras.preprocessing.image
from flask import request, jsonify, Flask, abort
from tensorflow.python.keras.backend import set_session
from flask import render_template
import argparse
import os
import operator
import re
import uuid

current_path = os.path.dirname(os.path.abspath(__file__))
print (f"current path: {current_path}")
class BadRequestException(Exception):
    pass

app = Flask(__name__)

fruits = [{"fruit": "Jablko", "prediction": 0, "image": "static/images/apple.png"},
          {"fruit": "Banan", "prediction": 0, "image": "static/images/banana.png"},
          {"fruit": "Cytryna", "prediction": 0, "image": "static/images/lemon.png"},
          {"fruit": "Pomarańcza", "prediction": 0, "image": "static/images/orange.png"},
          {"fruit": "Gruszka", "prediction": 0, "image": "static/images/pear.png"},
          {"fruit": "Marchewka", "prediction": 0, "image": "static/images/carrot.png"},
          {"fruit": "Ogórek", "prediction": 0, "image": "static/images/cucumber.png"},
          {"fruit": "Papryka", "prediction": 0, "image": "static/images/pepper.png"},
          {"fruit": "Ziemniak", "prediction": 0, "image": "static/images/potato.png"},
          {"fruit": "Pomidor", "prediction": 0, "image": "static/images/tomato.png"}
]

@app.route('/', methods=["GET"])
def get_camera():
    return render_template("camera.html")


def preprocess_image(image, target_size):
    image = image.resize(target_size)
    image = keras.preprocessing.image.img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image /= 255.
    return image

def stringProcess(oldValue):
    for elem in oldValue:
        if(elem == '.' or elem ==':' or elem ==' ' or elem ==','):
           oldValue = oldValue.replace(elem, '_')
    newString = oldValue + ".jpg"
    return newString

def get_image_from_request(request):
    message = request.get_json(force=True)
    imageName = message.get('name', None)
    imageName = stringProcess(imageName)
    print(imageName)
    encoded = message.get('imageData', None)
    if encoded != None:
        encoded, replacements_count = re.subn('^data:image/.+;base64,', '', encoded)
        if replacements_count == 0:
            raise BadRequestException('Nieobsługiwany typ pliku. Obsługiwane są jedynie pliki obrazów.')
        else:
            decoded = base64.standard_b64decode(encoded)
            image = Image.open(io.BytesIO(decoded))
            if image.mode != "RGB":
                image = image.convert("RGB")
            return image, imageName
    else:
        raise BadRequestException('Nie wysłano żadnego pliku')

def processProductsList(products):
    for i in range(len(fruits)):
        fruits[i]["prediction"] = round(products[0][i]*100,2)
        # sortowanie listy predykcji
    fruits.sort(key=operator.itemgetter('prediction'), reverse=True)
    for i in range(len(fruits)):
        list = [fruits[i]['fruit'], fruits[i]['prediction']]
        print("class: {}, prediction: {}%".format(*list))
    return fruits

@app.route("/", methods=["POST"])
def predict():
    try:
        image, imageName = get_image_from_request(request)
        # Zapisanie przesłanego pliku
        path = 'C:/Users/Agnieszka/Desktop/patrieszka/checkout/images/' + imageName
        image.save(path)
        processed_image = preprocess_image(image, target_size=(224, 224))
        prediction = None
        with graph.as_default():
            set_session(session)
            bt_prediction = vgg16.predict(processed_image)
            prediction = model.predict(bt_prediction).tolist()
            fruits = processProductsList(prediction)
        return render_template("list.html", predictions=fruits)
    except BadRequestException as error:
        abort(400, str(error))
    except Exception as error:
        raise error
        abort(500, str('Coś poszło nie tak po stronie serwera'))

def init_models():
    #załadowanie argumentów wiesza poleceń
    parser = argparse.ArgumentParser(description = "")
    parser.add_argument("-host", '--host', help = "Host aplikacji - domyślny to 'localhost'", required = False, default = 'localhost')
    parser.add_argument("-port", '--port', help = "Port for web app", required = False, default = 5000)
    parser.add_argument("-paths_to_models", '--paths_to_models', help = "Ścieżka do plików modeli - domyślna to '../models'", required = False, default = current_path + "\\..\\models")
    parser.add_argument("-paths_to_photos", '--paths_to_photos', help = "Scieżka gdzie mają być zapisywane przesyłane zdjęcia - domyślna to '../received_images'", required = False, default = current_path + '\\..\\' + 'received_images')
    argument = parser.parse_args()

    global host, port
    host = argument.host
    port = argument.port
    print("**Loading model")
    global model, graph, vgg16, session
    session = tf.Session()
    set_session(session)
   # models_path = argument.paths_to_models
    model = tf.keras.models.load_model('models/fc_model1.h5')
    model.load_weights('models/model_grocery.h5')
    vgg16 = keras.applications.VGG16(include_top=False, weights='imagenet')
    graph = tf.get_default_graph()
    print("**MODEL LOADED")

    # Utworzenie folderu na przychodzace zdjecia jesli nie istnieje
    global paths_to_photos
    paths_to_photos = argument.paths_to_photos
    if not os.path.exists(paths_to_photos):
        os.mkdir(paths_to_photos)
    return host, port


