import cv2
import keras.backend as K
import keras.preprocessing.image
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from keras.applications.vgg16 import preprocess_input


def preprocess_image(image, target_size):
    image = image.resize(target_size)
    image = keras.preprocessing.image.img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image /= 255.
    return image


def get_heatmap(path, model_vgg, current_path):
    img = keras.preprocessing.image.load_img(path, target_size=(224, 224))
    x = keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model_vgg.predict(x)
    class_idx = np.argmax(preds[0])
    class_output = model_vgg.output[:, class_idx]
    last_conv_layer = model_vgg.get_layer("block5_conv3")

    grads = K.gradients(class_output, last_conv_layer.output)[0]
    pooled_grads = K.mean(grads, axis=(0, 1, 2))
    iterate = K.function([model_vgg.input], [pooled_grads, last_conv_layer.output[0]])
    pooled_grads_value, conv_layer_output_value = iterate([x])
    for i in range(512):
        conv_layer_output_value[:, :, i] *= pooled_grads_value[i]

    heatmap = np.mean(conv_layer_output_value, axis=-1)
    heatmap = np.maximum(heatmap, 0)
    heatmap /= np.max(heatmap)

    img = cv2.imread(path)
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    superimposed_img = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)

    cm = plt.get_cmap('viridis')
    img = Image.fromarray(((superimposed_img)[:, :, :3] * 255).astype(np.uint8))
    heatmap_path = current_path + '\\checkout\\static\\images\\heatmap.jpg'
    img.save(current_path + '\\checkout\\static\\images\\heatmap.jpg')
    return heatmap_path
