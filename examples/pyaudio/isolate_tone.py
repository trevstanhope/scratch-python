# Import Modules
import pyaudio
import numpy as np
from ctypes import *
from datetime import datetime
from matplotlib import pyplot

# Set Constants
MICROPHONE_INDEX = 0
MICROPHONE_CHANNELS = 1
MICROPHONE_INPUT = True
MICROPHONE_FORMAT = 8
MICROPHONE_RATE = 44100
MICROPHONE_CHUNK = 2**12

# Error Handler
print('Creating Error Handler...')
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  pass
C_ERROR_HANDLER = ERROR_HANDLER_FUNC(py_error_handler)

# Initialize Microphone
mic = pyaudio.PyAudio()
microphone = mic.open(
    format=MICROPHONE_FORMAT,
    channels=MICROPHONE_CHANNELS,
    input=MICROPHONE_INPUT,
    rate=MICROPHONE_RATE,
    frames_per_buffer=MICROPHONE_CHUNK
)

# Capture Stream
microphone.start_stream()
data = microphone.read(MICROPHONE_CHUNK)
microphone.stop_stream()

# Fourier Fast Transform
wave_array = np.fromstring(data, dtype='int16')
wave_fft = np.fft.fft(wave_array)
wave_freqs = np.fft.fftfreq(len(wave_fft))

# Calculate
all_decibels = 10 * np.log10(np.abs(wave_fft))
all_hertz = MICROPHONE_RATE * abs(wave_freqs)
dominant_peak = np.argmax(np.abs(wave_fft))
dominant_hertz = MICROPHONE_RATE * abs(wave_freqs[dominant_peak])
dominant_amplitude = np.sqrt(np.abs(wave_fft[dominant_peak])**2)
dominant_decibels = 10 * np.log10(dominant_amplitude)
rms_amplitudes = np.sqrt(np.mean(np.abs(wave_fft)**2))
rms_decibels =  10 * np.log10(rms_amplitudes)
sorted_peaks = np.argsort(np.abs(wave_fft))
sorted_hertz = MICROPHONE_RATE * abs(wave_freqs[sorted_peaks])

# Display Data
print('dB_RMS: %f' % rms_decibels)
print('dB_MAX: %f' % rms_decibels)
print('hz_MAX: %f' % dominant_hertz)

# Save Data
freqs = sorted(zip(all_decibels, all_hertz), reverse=True)
file_name = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M.csv')
with open(file_name, 'w') as freq_file:
    freq_file.write('Hz,dB\n')
    for (db, hz) in freqs:
        freq_file.write(','.join([str(hz),str(db),'\n']))
