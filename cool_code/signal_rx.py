import SoapySDR
from SoapySDR import *
import numpy
import sounddevice as sd
import scipy as sp
#function def
def fm_demod(x, df=1.0, fc=0.0):
    ''' Perform FM demodulation of complex carrier.

    Args:
        x (array):  FM modulated complex carrier.
        df (float): Normalized frequency deviation [Hz/V].
        fc (float): Normalized carrier frequency.

    Returns:
        Array of real modulating signal.
    '''

    # Remove carrier.
    n = sp.arange(len(x))
    rx = x*sp.exp(-1j*2*sp.pi*fc*n)

    # Extract phase of carrier.
    phi = sp.arctan2(sp.imag(rx), sp.real(rx))

    # Calculate frequency from phase.
    y = sp.diff(sp.unwrap(phi)/(2*sp.pi*df))

    return y

#Check what compatible SoapySDR devices are connected

results = SoapySDR.Device.enumerate()
for result in results: print(result)

#Init HackRF

args = dict(driver="hackrf")
sdr = SoapySDR.Device(args)

##GQRX METRICS
#8192 FFT
#8000000 INPUT RATE
sdr.setSampleRate(SOAPY_SDR_RX,0,8000000)

#8.000 Msps SAMPLE RATE
#48 kHz AUDIO OUTPUT SAMPLE RATE


#Steps needed
#1. Tune SoapySDR to 101.103.000 (101.103 MHz)
sdr.setFrequency(SOAPY_SDR_RX,0,101103000)


#2 Setting up stream parameters (RX = Recieving antenna, recieve in CF32(Complex float 32 x2 == Complex64)
pasilaRX = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)


#create a re-usable buffer for rx samples (complex64 is 2 float 32's)
buff = numpy.array([0]*1024, numpy.complex64)

#activate the hackrf its antenna's
sdr.activateStream(pasilaRX)

#fill the array / complex64 with audiodata
for i in range(1000):
    sr = sdr.readStream(pasilaRX, [buff], len(buff))
    print(sr)

#dtype of np array
print(buff.dtype)
dmod_rx = fm_demod(buff)
#Sounddevice / SD can only play in the following formats:
#Can only play in float64, float32, int32, int16, int8 and uint8

#buff will be converted from complex64 to 2x float32 in the following lines

v = buff.view(numpy.float32)
w = numpy.array([numpy.real(buff), numpy.imag(buff)])
w = v.reshape(buff.shape + (2,))

#w is our reshaped array, we can confirm this by checking its dtype.

print(w.dtype)

print(w)

##TROUBLESHOOTING CODE; generate random array sample
data = numpy.random.uniform(-1, 1, 48000)
print("this is what the datavar looks like")
print(data)
#print(numpy.dtype(data))

sp.io.wavfile.write("karplus.wav", 48000, dmod_rx)
#Audioplayback, sample rate set to 48000. Blocking=True means that the code wont stop running until the audiofile is done / recieved.
#sd.play(dmod_rx, 48000, blocking=True)

#gracefully shutting down both the antenna and the hackrf datastream
sdr.deactivateStream(pasilaRX)
sdr.closeStream(pasilaRX)

#export code for Mikko, generates a numpy.save according to numpy.org docs
#https://numpy.org/doc/stable/reference/generated/numpy.save.html#numpy.save

numpy.save("float32reshape.npy", w, allow_pickle=True, fix_imports=True)
numpy.save("originalcomplex64.npy", buff, allow_pickle=True, fix_imports=True)
numpy.save("random.npy", data, allow_pickle=True, fix_imports=True)

#discover datafomat