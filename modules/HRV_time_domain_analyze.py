import numpy as np


def NN50(rr):
    return sum(abs(np.diff(rr)) > 50)


def NN20(rr):
    return sum(abs(np.diff(rr)) > 20)


def time_domain_analyze(RRints):
    """
    Computes time domain features on RR interval data

    Parameters:
    ------------
    RRints : list, shape = [n_samples,]
           RR interval data in ms



    Returns:
    ---------
    timeDomainFeats : dict
                   hrv,SDNN,SENN,SDS,pNN20,pNN50

    """
    hrv = np.sqrt(np.mean(np.square(np.diff(RRints))))
    SDNN = np.std(RRints)
    SENN = np.std(RRints) / np.sqrt(len(RRints))
    SDSD = np.std(np.diff(RRints))
    pNN50 = NN50(RRints) / len(RRints) * 100
    pNN20 = NN20(RRints) / len(RRints) * 100

    time_domain_features = {
        'hrv': hrv,
        'sdnn': SDNN,
        'senn': SENN,
        'sdsd': SDSD,
        'pnn20': pNN20,
        'pnn50': pNN50

    }

    return time_domain_features
