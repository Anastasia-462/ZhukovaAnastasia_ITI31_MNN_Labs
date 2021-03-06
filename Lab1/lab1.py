# -*- coding: utf-8 -*-
"""Lab1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GZt-GbJYnUol0crQhysv29lIboh4s654
"""

pip install scikit-image

pip install livelossplot

from skimage import io, transform
import numpy as np
from glob import glob
from google.colab import drive
import matplotlib.pyplot as plt
from random import randint
import tensorflow as tf
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
from keras.utils import np_utils
from keras.initializers import RandomNormal, RandomUniform, Constant
from livelossplot import PlotLossesKeras

def shuffle(a, b):
    seed = randint(0, 1000000)
    rand_state = np.random.RandomState(seed)
    rand_state.shuffle(a)
    rand_state.seed(seed)
    rand_state.shuffle(b)



drive.mount("/content/gdrive")
parasitized_path = glob('/content/gdrive/My Drive/Lab1/Parasitized/*.png')
uninfected_path = glob('/content/gdrive/My Drive/Lab1/Uninfected/*.png')

width = 1024
#size = len(uninfected_path)
test_size = 100
train_size = 1000

parasitized_test_path = parasitized_path[0:test_size]
uninfected_test_path = uninfected_path[0:test_size]
parasitized_train_path = parasitized_path[test_size:test_size + train_size]
uninfected_train_path = uninfected_path[test_size:test_size + train_size]

def resizeImages(x, y, paras_path, uninf_path):
  for path in paras_path + uninf_path:
    image = io.imread(path)
    new_size = [width, width]
    img = transform.resize(image, new_size)
    x = np.append(x, img)
  x = np.reshape(x, (len(y), width * width * 3))

trainX = np.array([])
#trainY = np.array([0] * train_size + [1] * train_size)

for path in uninfected_train_path + parasitized_train_path:
    image = io.imread(path)
    new_size = [width, width]
    img = transform.resize(image, new_size)
    trainX = np.append(trainX, img)
trainX = np.reshape(trainX, (len(trainY), width * width * 3))
#resizeImages(trainX, trainY, parasitized_train_path, uninfected_train_path)

testX = np.array([])
#testY = np.array([0] * test_size + [1] * test_size)

for path in uninfected_test_path + parasitized_test_path:
    image = io.imread(path)
    new_size = [width, width]
    img = transform.resize(image, new_size)
    testX = np.append(testX, img)
testX = np.reshape(testX, (len(testY), width * width * 3))
#resizeImages(testX, testY, parasitized_test_path, uninfected_test_path)

shuffle(trainX, trainY)
shuffle(testX, testY)

print(trainY)

#trainX /= 255.0
#testX /= 255.0

model = Sequential()
model.add(Dense(200, input_dim=(width * width * 3), activation="sigmoid"))
model.add(Dense(300, activation="sigmoid"))
model.add(Dense(300, activation="sigmoid"))
model.add(Dense(300, activation="sigmoid"))
model.add(Dense(10, activation="sigmoid"))
 
model.add(Dense(1, activation="sigmoid"))

#model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
model.compile(loss=tf.keras.losses.KLD, optimizer='rmsprop', metrics=['accuracy'])

history = model.fit(trainX, trainY, batch_size=1, epochs=1000, validation_split=0.1, callbacks=[PlotLossesKeras()])

model.evaluate(testX, testY, batch_size=1,callbacks=[PlotLossesKeras()])

print(testX.shape)
print(trainX.shape)