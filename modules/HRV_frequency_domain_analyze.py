from scipy import interpolate, signal
import numpy as np


def frequencydomain(RRints):
    """
    Computes frequency domain features on RR interval data

    Parameters:
    ------------
    RRints : list, shape = [n_samples,]
           RR interval data in ms



    Returns:
    ---------
    freqDomainFeats : dict
                   VLF_Power, LF_Power, HF_Power, LF/HF Ratio

    """
    # Resample @ 4 Hz
    fsResamp = 4
    NNs = np.divide(RRints, 1000)
    tmStamps = np.cumsum(NNs)  # in seconds
    timestamp_list = tmStamps - tmStamps[0]

    f = interpolate.interp1d(timestamp_list, RRints, 'linear')
    tmInterp = np.arange(0, timestamp_list[-1], 1 / fsResamp)

    RRinterp = f(tmInterp)

    # Remove DC component
    RRseries = RRinterp - np.mean(RRinterp)

    # Pwelch w/ zero pad
    freq, psd = signal.welch(RRseries, fsResamp, nfft=4096, window='hann')

    # bandwidth
    vlf_band = (0.003, 0.04)
    lf_band = (0.04, 0.15)
    hf_band = (0.15, 0.4)

    vlf_indexes = np.logical_and(freq >= vlf_band[0], freq < vlf_band[1])
    lf_indexes = np.logical_and(freq >= lf_band[0], freq < lf_band[1])
    hf_indexes = np.logical_and(freq >= hf_band[0], freq < hf_band[1])

    # Integrate using the composite trapezoidal rule
    lf = np.trapz(y=psd[lf_indexes], x=freq[lf_indexes])
    hf = np.trapz(y=psd[hf_indexes], x=freq[hf_indexes])

    # total power & vlf : Feature often used for  "long term recordings" analysis
    vlf = np.trapz(y=psd[vlf_indexes], x=freq[vlf_indexes])
    total_power = vlf + lf + hf

    lf_hf_ratio = lf / hf
    lfnu = (lf / (lf + hf)) * 100
    hfnu = (hf / (lf + hf)) * 100

    freqency_domain_features = {
        'lf': lf,
        'hf': hf,
        'lf_hf_ratio': lf_hf_ratio,
        'total_power': total_power,
        'vlf': vlf
    }

    return freqency_domain_features