from scipy import signal


def filterEcg(ecgValueArray,appleWatchECGSampleRate):
    """
    function to filter the ecg data (high and lowpass to remove baseline drift and noise)

    @param ecgValueArray: numpy float array with measured ecg values over time

    @return numpy float array with low and highpass filtered input data
    """

    lowFilterValue = 30
    highFilterValue = 1.5
    #highpass
    bh, ah = signal.butter(4, 2*highFilterValue/appleWatchECGSampleRate, btype='highpass')
    highfilteredECGValues = signal.filtfilt(bh,ah, ecgValueArray)
    #lowpass
    bL,aL = signal.butter(4, 2*lowFilterValue/appleWatchECGSampleRate)
    low_highfilteredECGValues = signal.filtfilt(bL, aL, highfilteredECGValues)

    return low_highfilteredECGValues

