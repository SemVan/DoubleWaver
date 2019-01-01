from matplotlib import pyplot as plt
import numpy as np

DESCRETISATION_PERIOD = 0.001

def plot_signals(ch1, ch2):
    plt.plot(range(len(ch1)), ch1, color='red')
    plt.plot(range(len(ch2)), ch2, color='red')
    plt.show()
    return


def get_phase_shift(sig1, sig2):
    cross_corr = np.correlate(sig1, sig2, mode='full')
    shift = np.argmax(cross_corr)
    return shift*0.001
