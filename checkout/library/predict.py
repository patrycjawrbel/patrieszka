import base64
from PIL import Image
import numpy as np
import io
import keras
import tensorflow as tf
import keras.preprocessing.image
from flask import request, jsonify, Flask
from tensorflow.python.keras.backend import set_session
from flask import render_template
import re


class BadRequestException(Exception):
    pass

app = Flask(__name__)


def preprocess_image(image, target_size):
    image = image.resize(target_size)
    image = keras.preprocessing.image.img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image /= 255.
    return image

def get_image_from_request(request):
    message = request.get_json(force=True)
    encoded = message.get('image', None)
    if encoded != None:
        # Usunięcie zbędnych danych przesyłanych przez przegladarke i sprawdzenie typu mime
        encoded, replacements_count = re.subn('^data:image/.+;base64,', '', encoded)
        if replacements_count == 0:
            # Błędny typ mime przesłanego pliku - inny niż "image/*"
            raise BadRequestException('Nieobsługiwany typ pliku. Obsługiwane są jedynie pliki obrazów.')
        else:
            decoded = base64.standard_b64decode(encoded)
            image = Image.open(io.BytesIO(decoded))
            if image.mode != "RGB":
                image = image.convert("RGB")
            return image
    else:
        raise BadRequestException('Nie wysłano żadnego pliku')


@app.route("/hello", methods=["POST"])
def predict():
    image = get_image_from_request(request)
    processed_image = preprocess_image(image, target_size=(224, 224))

    prediction = None
    with graph.as_default():
        set_session(session)
        bt_prediction = vgg16.predict(processed_image)
        prediction = model.predict(bt_prediction).tolist()
        print(prediction)

    return render_template('index.html')

def get_model():
    print("get_model")
    global model, graph, vgg16, session
    model = tf.keras.models.load_model('fc_model1.h5')
    model.load_weights('model_grocery.h5')
    vgg16 = keras.applications.VGG16(include_top=False, weights='imagenet')
    graph = tf.get_default_graph
    print("** Model loaded!")

get_model()
predict()