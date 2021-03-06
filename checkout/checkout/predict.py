import keras
import tensorflow as tf
import keras.preprocessing.image
from flask import request, Flask, abort
from keras.applications.vgg16 import VGG16
from tensorflow.python.keras.backend import set_session
from flask import render_template, redirect, url_for
import argparse
import os
from checkout.python.get__image import get_image_from_request
from checkout.python.process_products_list import process_products_list
from checkout.python.preprocess_image import preprocess_image, get_heatmap
from checkout.database.connection import connect_database
from checkout.database.insert_pred import insert_pred
from checkout.database.select_class import select_class
from checkout.database.select_last import select_last
from checkout.database.insert_label import insert_label

current_path = os.getcwd()


class BadRequestException(Exception):
    pass


app = Flask(__name__)

# funkcja odpowiadająca za odczytanie argumentów z linii poleceń, załadowanie modeli oraz połączenie z bazą danych
def init_models():
    # załadowanie argumentów wiesza poleceń
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-host", '--host', help="Host aplikacji - domyślny to 'localhost'", required=False,
                        default='localhost')
    parser.add_argument("-port", '--port', help="Port for web app", required=False, default=5000)
    argument = parser.parse_args()

    global host, port, weights, conn
    host = argument.host
    port = argument.port
    print("**Loading model")
    global model, graph, vgg16, session, model_vgg
    session = tf.Session()
    set_session(session)
    model = tf.keras.models.load_model('models/fc_model1.h5')
    model_vgg = VGG16('models/fc_model1.h5')
    weights = model.load_weights('models/model_grocery.h5')
    vgg16 = keras.applications.VGG16(include_top=False, weights='imagenet')
    graph = tf.get_default_graph()
    print("**MODEL LOADED")

    # połączenie z bazą danych
    conn = connect_database()
    print("**DATABASE CONNECTED**")

    # Utworzenie folderu na przychodzace zdjecia jesli nie istnieje
    global paths_to_photos
    paths_to_photos = current_path + '\\images'
    try:
        os.mkdir(paths_to_photos)
    except OSError:
        print("Creation of the directory %s failed" % paths_to_photos)
    else:
        print("Successfully created the directory %s " % paths_to_photos)
    return host, port

# endpoint zwracający html z widokiem z kamery
@app.route('/', methods=["GET"])
def get_camera():
    return render_template("camera.html")

# endpoint przyjmujący zdjęcie od klienta oraz wykonujący predykcje
@app.route("/", methods=["POST"])
def predict():
    global fruits
    try:
        image, imageName = get_image_from_request(request)
        # Zapisanie przesłanego pliku
        path = paths_to_photos + '\\' + imageName
        #print( "Current dir: " % path)
        image.save(paths_to_photos + '\\' + imageName)
        processed_image = preprocess_image(image, target_size=(224, 224))
        prediction = None
        with graph.as_default():
            set_session(session)
            bt_prediction = vgg16.predict(processed_image)
            prediction = model.predict(bt_prediction).tolist()
            insert_pred(conn, prediction, path)
            fruits = process_products_list(prediction)
            heatmap_image_path = get_heatmap(path, model_vgg, current_path)
        return redirect(url_for('get_items'))
    except BadRequestException as error:
        abort(400, str(error))
    except Exception as error:
        raise error
        abort(500, str('Coś poszło nie tak po stronie serwera'))

# endpoint zwracający html z czterema najbardziej prawdopodobnymi wynikami
@app.route("/results")
def get_items():
    return render_template("list.html", var=fruits)

# endpoint przyjmujący etykietę od klienta i dokonujący zapisu do bazy
@app.route("/saveLabel", methods=['POST'])
def ranking():
    message = request.get_json(force=True)
    labelName = message.get('fruitName', None)
    print(labelName)
    #zapis do bazy
    id_label = select_class(conn, labelName)
    id_current_pred = select_last(conn)
    insert_label(conn, id_label, id_current_pred)
    return url_for("rank")

# endpoint zwracający html z końcowymi statystykami
@app.route("/ranking")
def rank():
    return render_template("results.html", fruits=fruits)
