import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from tensorflow.keras.layers import Bidirectional
from keras.layers import Dropout
from tensorflow.keras.layers import BatchNormalization
import numpy as np


def convlstm_model(xTrain, xTest, yTrain, yTest):
    # flatten the input and output
    n_input = np.shape(xTrain)[1] * np.shape(xTrain)[2]
    xTrain = np.reshape(xTrain, (np.shape(xTrain)[0], n_input))
    n_output = np.shape(yTrain)[1] * np.shape(yTrain)[2]
    yTrain = np.reshape(yTrain, (np.shape(yTrain)[0], n_output))

    xTest = np.reshape(xTest, (np.shape(xTest)[0], n_input))
    yTest = np.reshape(yTest, (np.shape(yTest)[0], n_output))

    # define multi-layer perceptron model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv1D(filters=32, kernel_size=5,
                               strides=1, padding="same",
                               activation="relu",
                               input_shape=[None,1]),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(256, return_sequences=True)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(256)),
        tf.keras.layers.Dense(60, activation="relu"),
        tf.keras.layers.Dense(20, activation="relu"),
        tf.keras.layers.Dense(n_output),
        #tf.keras.layers.Lambda(lambda x: x * 400)
    ])

    model.compile(optimizer='adam', loss='mse')
   #model.compile(loss=tf.keras.losses.Huber(), 
                 # optimizer='adam',
                  #optimizer=tf.keras.optimizers.SGD(learning_rate=0.0001, momentum = 0.9),
                 # metrics=['mae'])

    # fit the keras model on the dataset
    history =model.fit(xTrain, yTrain, epochs=5, verbose=1, validation_data=(xTest, yTest))

    # save the trained model
    filepath = 'convlstm_model.h5'
    model.save(filepath)

    # load trained model
    model = keras.models.load_model('convlstm_model.h5')

    # Training and validation loss plot
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model train vs validation loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper right')

    return model