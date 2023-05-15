import numpy
import numpy as np
import onnxruntime as ort


def normalize(array):
    return (array - array.mean()) / array.std()


def get_model_input_data(data):
    start = 0
    end = 1000
    offset = 1000
    data_bins = []

    for i in range(len(data) // offset + 1):
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
    # use the onnx converted lstm model for predictions to lower latency
    sess = ort.InferenceSession('models/lstm_model.onnx')
    input_name = sess.get_inputs()[0].name
    output_name = sess.get_outputs()[0].name
    model_input = get_model_input_data(data).astype(numpy.float32)
    model_output = sess.run([output_name], {input_name: model_input})
    model_output = np.reshape(model_output, (-1))
    full_lstm_pred_array = model_output[:len(data)]
    full_lstm_pred_array = np.where(full_lstm_pred_array >= 0.3, 1, 0)
    r_peaks = np.where(full_lstm_pred_array == 1)
    return r_peaks[0]
