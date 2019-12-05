import base64
from PIL import Image
import numpy as np
import io
import keras
import tensorflow as tf
import keras.preprocessing.image
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
import keras.backend as K
import cv2
import sys
import matplotlib.pyplot as plt
from flask import request, jsonify, Flask, abort
from tensorflow.python.keras.backend import set_session
from flask import render_template
import argparse
import os
import operator
import re

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

def heatmap():
    model = VGG16('/content/drive/My Drive/models/weights_model2611.h5')
    img_path = '/content/drive/My Drive/Dane/singleTest/Tomato/20191017_195023.jpg'
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    class_idx = np.argmax(preds[0])
    class_output = model.output[:, class_idx]
    last_conv_layer = model.get_layer("block5_conv3")

    grads = K.gradients(class_output, last_conv_layer.output)[0]
    pooled_grads = K.mean(grads, axis=(0, 1, 2))
    iterate = K.function([model.input], [pooled_grads, last_conv_layer.output[0]])
    pooled_grads_value, conv_layer_output_value = iterate([x])
    for i in range(512):
        conv_layer_output_value[:, :, i] *= pooled_grads_value[i]

    heatmap = np.mean(conv_layer_output_value, axis=-1)
    heatmap = np.maximum(heatmap, 0)
    heatmap /= np.max(heatmap)

    img = cv2.imread(img_path)
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    superimposed_img = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)

    plt.figure(figsize=(12, 10))
    plt.imshow(img)
    plt.imshow(superimposed_img, cmap='viridis')
    plt.grid(False)
    plt.show()
    plt.savefig('/content/drive/My Drive/Dane/foo.png')
    cm = plt.get_cmap('viridis')
    img = Image.fromarray(((superimposed_img)[:, :, :3] * 255).astype(np.uint8))
    img.save('/content/drive/My Drive/Dane/image.png')

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

def processProductsList(products):
    for i in range(len(fruits)):
        fruits[i]["prediction"] = round(products[0][i]*100,2)
        # sortowanie listy predykcji
    fruits.sort(key=operator.itemgetter('prediction'), reverse=True)
    for i in range(len(fruits)):
        list = [fruits[i]['fruit'], fruits[i]['prediction']]
        print("class: {}, prediction: {}%".format(*list))
    return fruits

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


