import os
import tensorflow as tf
from scipy.signal import find_peaks
from tensorflow import keras
import numpy as np
from matplotlib import pyplot as plt
import plotly.express as px


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


def detect_r_peaks(data):
    lstm_model = keras.models.load_model('models/lstm_model')
    model_input = get_model_input_data(data)
    model_output = lstm_model.predict(model_input)
    model_output = np.reshape(model_output, (-1))
    full_lstm_pred_array = model_output[:len(data)]
    # full_lstm_pred_array[full_lstm_pred_array >= 0.3] = 1
    # full_lstm_pred_array[full_lstm_pred_array < 0.3] = 0
    r_peaks = find_peaks(full_lstm_pred_array, height=0.3)
    # plt.rcParams["figure.figsize"] = (20, 6)
    # time = np.arange(0, len(data) / 511, 1 / 511)
    # plt.plot(time[:len(data)], data)
    # plt.scatter(x=r_peaks[0]/511, y=data[r_peaks[0]], marker='o', c='red')
    # plt.show()
    return r_peaks[0]
