#ifndef TEST_PY
#define TEST_PY
import tensorflow as tf
import sys
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import PIL

def getModel():
    return  tf.keras.models.load_model("/home/mads/davidmaseda/dev/colorful-api/app/api/test2_pix2pix_lambda5/200")


def load(image_file):
    image = tf.io.read_file(image_file)
    image = tf.image.decode_jpeg(image)
    image = tf.cast(image,tf.float32)
    image = tf.divide(image,255.0)
    image = tf.image.rgb_to_yuv(image)
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

model = getModel()

imagepath = sys.argv[1]

inputimage,realimage = load(imagepath)
inputimage = tf.image.resize_with_crop_or_pad(inputimage,1024,1024)
inputimage = tf.expand_dims(inputimage,0)

realimage = tf.image.resize_with_crop_or_pad(realimage,1024,1024)
realimage = tf.expand_dims(realimage,0)

noise = np.random.normal(size=(1,inputimage.shape[1],inputimage.shape[2],1))
print(inputimage.shape)
print(realimage.shape)
print(noise.shape)

outputimage = model.predict([inputimage,noise])[0]

outputimage = tf.concat([inputimage[0],outputimage],axis=2)
print("output shape:",outputimage.shape," with type ",outputimage.dtype)
rgb = tf.image.yuv_to_rgb(outputimage)
#rgb = tf.multiply(rgb,255)
#rgb = tf.cast(rgb,tf.uint8)
print("rgb:",rgb)
#im = Image.fromarray(outputimage.numpy())
#im.save("result2.jpg")
tosave = np.clip(rgb.numpy(),0.0,1.0)
print("max:",np.max(rgb.numpy()))
print("min:",np.min(rgb.numpy()))
plt.imsave("result2.png",tosave)
enc = tf.io.encode_jpeg(rgb)
tf.io.write_file("result3.jpg",enc)

#endif /* TEST_PY */
