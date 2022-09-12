import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import tensorflow as tf
from tensorflow import keras
import numpy as np
from scipy.signal import find_peaks

lstm_model = keras.models.load_model('models/lstm_model')

model_outputs = []


def normalize(array):
    return (array - array.mean()) / array.std()


def model_input_from_data(data, bin_size, offset=0):
    data_bins = []

    for i in range((len(data) + offset) // bin_size + 1):
        pos = i * bin_size - offset
        data_bins.append(data[max(pos, 0):pos + bin_size])

    normalised_data_bins = []

    for section in data_bins:
        normalised_data_bins.append(normalize(np.array(section)))

    normalised_data_bins[0] = np.append(offset * [0], normalised_data_bins[0])
    normalised_data_bins[-1] = np.append(normalised_data_bins[-1], (1000 - len(data_bins[-1])) * [0])

    model_input = np.array(normalised_data_bins)
    model_input = np.expand_dims(model_input, 2)
    return model_input


def detect_r_peaks(data):
    for offset in (0, 500):
        model_input = model_input_from_data(data, 1000, offset)

        model_output = lstm_model.predict(x=model_input)

        model_output = np.reshape(model_output, (-1))
        model_output = model_output[offset:]
        model_output = model_output[:len(data)]
        model_outputs.append(model_output)

        # plot_data_vs_pred(data, model_output)

    model_output_max = []

    for r in np.transpose(model_outputs):
        model_output_max.append(max(r))
    r_peaks = find_peaks(model_output_max, height=0.5, distance=20)
    return r_peaks[0]
