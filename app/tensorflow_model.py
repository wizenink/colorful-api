import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import skimage.io
from skimage import img_as_ubyte
import base64
import os

def load2(image_b64):
    image_b64 += '=' * (-len(image_b64) % 4)  # restore stripped '='s
    image_string = tf.io.decode_base64(image_b64)
    image = tf.image.decode_image(image_string)
    image = tf.cast(image,tf.float32)
    image = tf.divide(image,255.0)
    image = tf.image.resize_with_crop_or_pad(image,256,256)
    image = tf.image.rgb_to_yuv(image)
    input_image = tf.expand_dims(image[:,:,0],-1)
    real_image = image[:,:,1:3]
    return input_image,real_image

def load(image_file):
    image = tf.io.read_file(image_file)
    image = tf.image.decode_jpeg(image)
    image = tf.cast(image,tf.float32)
    image = tf.divide(image,255.0)
    image = tf.image.resize_with_crop_or_pad(image,256,256)
    image = tf.image.rgb_to_yuv(image)  

    image = tf.image.random_flip_left_right(image)
    #image = tf.image.random_flip_up_down(image)
    #channels = tf.unstack(image,axis=-1)
    #image = tf.stack([channels[2],channels[1],channels[0]],axis=-1)
    input_image = tf.expand_dims(image[:,:,0],-1)
    real_image = image[:,:,1:3]

    #input_image = tf.cast(input_image,tf.float32)
    #input_image = tf.divide(input_image,255.0)
    #real_image = tf.cast(real_image,tf.float32)
    #real_image = tf.divide(real_image,255.0)

    
    return input_image,real_image


def getModels():
    return os.listdir("models")

def getModel(model):
    return  tf.keras.models.load_model(f"models/{model}")
    #return tf.keras.models.Model()

def predict(model,image_base64):
    input_image,real_image = load2(image_base64)
    print(input_image.shape)
    image = tf.expand_dims(input_image,0)
    noise = np.random.normal(size=(1,image.shape[1],image.shape[2],1))
    result = model.predict([image,noise],use_multiprocessing=False,verbose=1)
    image = np.concatenate([image,result],axis=-1)
    res = tf.image.yuv_to_rgb(image)
    return np.clip(res.numpy()[0],0.0,1.0)


