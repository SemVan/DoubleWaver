from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import correlate
from scipy.signal import butter, lfilter, lfilter_zi, welch

DESCRETISATION_PERIOD = 0.001

def plot_signals(ch1, ch2):
    plt.plot(range(len(ch1)), ch1, color='red')
    plt.plot(range(len(ch2)), ch2, color='green')
    plt.show()
    return


def get_phase_shift(sig1, sig2):
    cross_corr = correlate(sig1, sig2, 'full', 'same')
    # plt.plot(range(len(cross_corr)), cross_corr)
    # plt.show()
    shift = np.argmax(cross_corr) - len(sig1)
    return shift*DESCRETISATION_PERIOD


def butter_bandpass(lowcut, highcut, fs, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    zi = lfilter_zi(b, a)
    y, z = lfilter(b, a, data, zi=zi*data[0])
    return y


def norm_signal(sp):
    max = np.max(sp)
    norm = []
    for i in range(len(sp)):
        norm.append(sp[i] / max)
    return norm


def get_spectra(signal):
    period = 1/1000
    complex_four = np.fft.fft(signal)
    spectra = np.absolute(complex_four)
    freqs = []
    for i in range(len(signal)):
        freqs.append(1/(period*len(signal))*i)

    plt.plot(freqs, spectra)
    plt.ylim([0, 20])
    plt.show()
    return spectra, freqs
