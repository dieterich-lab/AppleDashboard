import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
from matplotlib import pyplot as plt


def normalize(array):
    return (array - array.mean()) / array.std()


def get_model_input_data(data):
    start = 0
    end = 1000
    offset = 1000
    data_bins = []

    for i in range(0, len(data), 1000):
        samples = data[start:end]
        start += offset
        end += offset
        data_bins.append(samples)

    normalized_data_bins = []

    for section in data_bins:
        normalized_data_bins.append(normalize(np.array(section)))

    # append zeros to the last sample to get an equal sample length of 1000
    normalized_data_bins[-1] = np.append(normalized_data_bins[-1], (1000 - len(data_bins[-1])) * [0])

    model_input = np.array(normalized_data_bins)
    model_input = np.reshape(model_input, (len(model_input), len(model_input[0]), 1))
    return model_input


def flatten_and_glue(array, length):
    array = array.reshape(len(array), -1)
    array = array.reshape(16000)
    return array


def detect_r_peaks(data):
    lstm_model = keras.models.load_model('models/lstm_model')
    model_input = get_model_input_data(data)
    model_output = lstm_model.predict(model_input)
    full_ecg_array = flatten_and_glue(model_input, len(data))
    full_lstm_pred_array = flatten_and_glue(model_output, len(data))
    plt.plot(full_ecg_array[0])
    plt.plot(full_lstm_pred_array[0], color='red')
    plt.imshow()

    return model_output
