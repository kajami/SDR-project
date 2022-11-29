#1.9.3
import scipy.io.wavfile as wavfile
from scipy.signal import firwin
#1.23.4
import numpy as np
#3.6.2
from matplotlib import pyplot as plt
import matplotlib
import datetime





# read in wav format IQ data
rate, data = wavfile.read('AM_Sig_IQ_48khz.wav')

def formatSpectogram():
    cmap = plt.get_cmap('viridis')
    vmin = -40
    cmap.set_under(color='k', alpha=None)

    fig, ax = plt.subplots()
    pxx, freq, t, cax = ax.specgram(data[:, 0], # first channel
                                    Fs=rate,      # to get frequency axis in Hz
                                    cmap=cmap, vmin=vmin)
    cbar = fig.colorbar(cax)
    cbar.set_label('Intensity dB')
    ax.axis("tight")

    ax.set_xlabel('time h:mm:ss')
    ax.set_ylabel('frequency kHz')

    scale = 1e3                     # KHz
    ticks = matplotlib.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale))
    ax.yaxis.set_major_formatter(ticks)

    formatter = matplotlib.ticker.FuncFormatter(timeTicks)
    ax.xaxis.set_major_formatter(formatter)

def timeTicks(x, pos):
    d = datetime.timedelta(seconds=x)
    return str(d)


def demodulate(freq_shift=0, show_spectogram=False, decimate=1, db=12, name='audio_shifted.wav'):
    # split data into I and Q
    I, Q = data.T

    # create audio from I and Q usin 1j imaginary number
    audio = I + 1j*Q

    # use mathplot specgram function to create automatically a spectogram
    if show_spectogram:
        formatSpectogram()
        plt.specgram(audio, Fs=rate)
        plt.show()


    shift_amount = freq_shift

    # shift the center frequency by 10kHz and -7kHz
    audio_shift = audio * np.exp(1j*2*np.pi*shift_amount/rate*np.arange(len(audio)))

    # plot spectrogram
    if(show_spectogram):
        formatSpectogram()
        plt.specgram(audio_shift, Fs=rate)
        plt.show()



    # Decimate
    x = audio_shift[::decimate]
    sample_rate = rate / decimate

    # Low-Pass Filter
    taps = firwin(numtaps=101, cutoff=5e3, fs=sample_rate)
    x = np.convolve(x, taps, 'valid')

    # normalize volume
    x /= x.std()

    # lower the db
    x = x / db

    wavfile.write(name, int(sample_rate), (x.imag[:,np.newaxis]))


demodulate(10000,decimate=2, name="audio1.wav")
demodulate(-7000,decimate=2, name="audio2.wav")




