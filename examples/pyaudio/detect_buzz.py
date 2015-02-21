import pyaudio
import numpy as np
from ctypes import *
from matplotlib import pyplot
import time
from datetime import datetime

print('Creating Error Handler...')
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  pass
C_ERROR_HANDLER = ERROR_HANDLER_FUNC(py_error_handler)

print('Setting Constants...')
BITS = 12
INDEX=0
FORMAT=8
CHANNELS=1
INPUT=True
RATE=44100
CHUNK=2**BITS
DURATION = 60
START_TIME = time.time()
OUTPUT_FILE = 'major_freq.csv'

output_file = open(OUTPUT_FILE, 'w')
output_file.write('time,hz,db\n')

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

while time.time() < START_TIME + DURATION:
    print('Capturing Microphone Stream...')
    microphone.start_stream()
    data = microphone.read(CHUNK)
    microphone.stop_stream()

    print('Calculating Wave Array...')
    wave_array = np.fromstring(data, dtype='int16')
            
    print('Calculating FFT...')
    wave_fft = np.fft.fft(wave_array)
    
    print('Calculating Frequencies...')
    wave_freqs = np.fft.fftfreq(len(wave_fft))
    
    print('Calculating Major Frequency...')
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
    
    current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    output_file.write(','.join([current_time,str(major_hz),str(db),'\n']))
    time.sleep(1)
output_file.close()
