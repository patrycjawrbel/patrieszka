import keras.preprocessing.image
import numpy as np

def preprocess_image(image, target_size):
    image = image.resize(target_size)
    image = keras.preprocessing.image.img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image /= 255.
    return image