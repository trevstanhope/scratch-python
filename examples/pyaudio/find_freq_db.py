import pyaudio
import numpy as np
from ctypes import *
from matplotlib import pyplot

print('Creating Error Handler...')
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  pass
C_ERROR_HANDLER = ERROR_HANDLER_FUNC(py_error_handler)

print('Setting Constants...')
BITS = 15
INDEX=0
FORMAT=8
CHANNELS=1
INPUT=True
RATE=44100
CHUNK=2**BITS

print('Loading ASound...')
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(C_ERROR_HANDLER) # Set error handler

print('Opening Microphone...')
mic = pyaudio.PyAudio()
microphone = mic.open(
    input_device_index=INDEX,
    format=FORMAT,
    channels=CHANNELS,
    input=INPUT,
    rate=RATE,
    frames_per_buffer=CHUNK
)

print('Capturing Microphone Stream...')
microphone.start_stream()
data = microphone.read(CHUNK)

print('Calculating Wave Array...')
wave_array = np.fromstring(data, dtype='int16')
print('\tArray Length: %s' % str(len(wave_array)))
with open('wave_array_' + str(BITS) + 'bit.csv', 'w') as array_file:
    for i in wave_array:
        array_file.write(str(i) + ',')
        
print('Calculating FFT...')
wave_fft = np.fft.fft(wave_array)
print('\tFFT Length: %s' % str(len(wave_fft)))
with open('wave_fft_' + str(BITS) + 'bit.csv', 'w') as fft_file:
    for i in wave_fft:
        fft_file.write(str(i) + ',')

print('Calculating Frequencies...')
wave_freqs = np.fft.fftfreq(len(wave_fft))
print('\tFrequencies Length: %s' % str(len(wave_freqs)))
with open('wave_freqs_' + str(BITS) + 'bit.csv', 'w') as freqs_file:
    for i in wave_freqs:
        freqs_file.write(str(i) + ',')

print('Plotting Frequency Domain...')
pyplot.scatter(RATE*abs(wave_freqs), abs(wave_fft), s=0.1)
pyplot.show()

print('Calculating Major and Minor Frequencies...')
major_freq = np.argmax(np.abs(wave_fft))
major_hz = RATE*abs(wave_freqs[major_freq])
print('\tMajor Hz: %s' % str(major_hz))
print('\tMajor Amp: %s' % str(major_freq))

print('Calculating Amplitude...')
amp = np.sqrt(np.mean(np.abs(wave_fft)**2))
print('\tAmps: %s' % str(amp))

print('Calculating Decibels...')
db =  20*np.log10(amp)
print('\tdB: %s' % str(db))
