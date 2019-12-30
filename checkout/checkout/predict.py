import keras
import tensorflow as tf
import keras.preprocessing.image
from flask import request, Flask, abort
from tensorflow.python.keras.backend import set_session
from flask import render_template, redirect, url_for
import argparse
import os
from checkout.python.get__image import get_image_from_request
from checkout.python.process_products_list import process_products_list
from checkout.python.preprocess_image import preprocess_image
from checkout.database.connection import connect_database
from checkout.database.insert_pred import insert_pred

current_path = os.path.dirname(os.path.abspath(__file__))
class BadRequestException(Exception):
    pass

app = Flask(__name__)
@app.route('/', methods=["GET"])
def get_camera():
    return render_template("camera.html")

@app.route("/", methods=["POST"])
def predict():
    global fruits
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
            conn = connect_database()
            insert_pred(conn, prediction,path)
            fruits = process_products_list(prediction)
        return redirect(url_for('get_items'))
    except BadRequestException as error:
        abort(400, str(error))
    except Exception as error:
        raise error
        abort(500, str('Coś poszło nie tak po stronie serwera'))

@app.route("/results")
def get_items():
    return render_template("list.html", var=fruits)

#@app.route("/ranking")
#def ranking():



def init_models():
    #załadowanie argumentów wiesza poleceń
    parser = argparse.ArgumentParser(description = "")
    parser.add_argument("-host", '--host', help = "Host aplikacji - domyślny to 'localhost'", required = False, default = 'localhost')
    parser.add_argument("-port", '--port', help = "Port for web app", required = False, default = 5000)
    parser.add_argument("-paths_to_models", '--paths_to_models', help = "Ścieżka do plików modeli - domyślna to '../models'", required = False, default = current_path + "\\..\\models")
    parser.add_argument("-paths_to_photos", '--paths_to_photos', help = "Scieżka gdzie mają być zapisywane przesyłane zdjęcia - domyślna to '../received_images'", required = False, default = current_path + '\\..\\' + 'received_images')
    argument = parser.parse_args()

    global host, port, weights, model
    host = argument.host
    port = argument.port
    print("**Loading model")
    global model, graph, vgg16, session
    session = tf.Session()
    set_session(session)
   # models_path = argument.paths_to_models
    model = tf.keras.models.load_model('models/fc_model1.h5')
    weights = model.load_weights('models/model_grocery.h5')
    vgg16 = keras.applications.VGG16(include_top=False, weights='imagenet')
    graph = tf.get_default_graph()
    print("**MODEL LOADED")

    # Utworzenie folderu na przychodzace zdjecia jesli nie istnieje
    global paths_to_photos
    paths_to_photos = argument.paths_to_photos
    if not os.path.exists(paths_to_photos):
        os.mkdir(paths_to_photos)
    return host, port


