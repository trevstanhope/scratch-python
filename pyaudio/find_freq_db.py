import pyaudio
import numpy as np

FORMAT=8
CHANNELS=1
INPUT=True
RATE=44100
CHUNK=1024
REFERENCE=32767
mic = pyaudio.PyAudio()
microphone = mic.open(
    format=FORMAT,
    channels=CHANNELS,
    input=INPUT,
    rate=RATE,
    frames_per_buffer=CHUNK
)
microphone.start_stream()
data = microphone.read(CHUNK)
wave_array = np.fromstring(data, dtype='int16')
wave_fft = np.fft.fft(wave_array)
wave_freqs = np.fft.fftfreq(len(wave_fft))
hz = RATE*abs(wave_freqs[np.argmax(np.abs(wave_fft)**2)])
amp = np.sqrt(np.mean(np.abs(wave_fft)**2))
db =  20*np.log10(amp/REFERENCE)
print hz
print amp, db
