import numpy as np


def findRPeaks(ecgValues,appleWatchECGSampleRate):

    """
    function to detect R peaks in an ECG using a threshold optimized with considering a maximum heart rate

    @param ecgValues: numpy float array with measured ECG values, recommended to be filtered

    @return numpy int array containing the position of detected R peaks in the ecgValues array

    """


    r_peaks = ([])
    average= np.mean(ecgValues)
    s = np.std(ecgValues)
    factor = 1.5
    #use 0.3 for a maximum heart rate of 200 beats/min
    #assume that the heart rate is not greater than 200 in order to skip parts
    #after a peak was detected and to speed up the detection
    refractary = 0.3 * appleWatchECGSampleRate
    threshold = average+factor*s
    #only where ecg value is over the threshold can a peak be as it is a local max
    logicVector = ecgValues >= threshold
    logicVector = np.multiply(logicVector, 1)
    i=1
    row=0
    #helper array which will be filled with parts ecg in which a peak could
    #potentially be
    peakBlocks=np.zeros((ecgValues.size, ecgValues.size))
    while i < ecgValues.size:
        #if current value just exeeded threshold or is over it, add to helper array
        if (logicVector[i]==1 and logicVector[i-1]==0) or (logicVector[i]==1 and logicVector[i-1]==1) :
          peakBlocks[row,i]=ecgValues[i]
          i= int(i)+1
        #if current value is the first under the threshold after previous ones were
        #over threshold, then get max of all values over threshold to get potential peak
        #and add its position to peak array, then jump some datapoints from the
        #detected peak (in this time no peak is expected, because of maximum hr and
        #refrectary time, therefore they must not be looked at)
        elif logicVector[i]==0 and logicVector[i-1]==1:
          xPos = np.argmax(peakBlocks[row,:])
          if xPos != 0:
            r_peaks = np.append(r_peaks, xPos)
            row = row+1
            i= int(xPos+ refractary)
          else:
            i = int(i)+1
        #if current value is under threshold then proceed to next, no peak to be found
        #here
        elif logicVector[i]==0 and logicVector[i-1]==0:
          i=int(i)+1
    return r_peaks.astype('int')