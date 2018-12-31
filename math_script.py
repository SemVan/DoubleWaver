from matplotlib import pyplot as plt



def plot_signals(ch1, ch2):
    plt.plot(range(len(ch1)), ch1, color='red')
    plt.plot(range(len(ch2)), ch2, color='red')
    plt.show()
    return


def get_phase_shift(sig1, sig2):
    return 0
