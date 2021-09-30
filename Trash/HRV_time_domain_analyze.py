import numpy as np


def NN50(rr):
    return sum(abs(np.diff(rr)) > 50)


def NN20(rr):
    return sum(abs(np.diff(rr)) > 20)


def time_domain_analyze(RRints):

    hrvOwn = np.sqrt(np.mean(np.square(np.diff(RRints))))
    SDNN = np.std(RRints)
    SENN = np.std(RRints) / np.sqrt(len(RRints))
    SDSD = np.std(np.diff(RRints))
    pNN50 = NN50(RRints) / len(RRints) * 100
    pNN20 = NN20(RRints) / len(RRints) * 100

    time_domain_features = {
        'hrvOwn': hrvOwn,
        'SDNN': SDNN,
        'SENN': SENN,
        'SDSD': SDSD,
        'pNN20': pNN20,
        'pNN50': pNN50

    }

    return time_domain_features