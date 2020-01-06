import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

# Decomposes audio stream into frequencies using fast fourier transform
def fft_decomp(stream):
    data = struct.unpack(str(2 * CHUNK) + 'B', stream.read(CHUNK))
    data = np.array(data, dtype='b')[::2] + 128
    x_fft = np.linspace(0,RATE,CHUNK)
    y_fft = fft(data)
    y_fft = 8* np.abs(y_fft[0:CHUNK])*2/(256*CHUNK)
    return x_fft, y_fft, data  # for plotting

plt.style.use('dark_background')

global CHUNK, FORMAT, CHANNELS, RATE
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, output = True, frames_per_buffer = CHUNK)

fig, (ax, ax2) = plt.subplots(2, figsize=(15, 7))
x = np.arange(0, 2 * CHUNK, 2)
x_fft = np.linspace(0, RATE, CHUNK)

line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)
line_fft, = ax2.semilogx(x_fft, np.random.rand(CHUNK),'-',lw=2)

ax.set_title('Audio Waveform')
ax.set_ylim(0, 255)
ax.set_xlim(0, 2 * CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])
plt.show(block=False)

while True:
    x_fft, y_fft,data = fft_decomp(stream)
    line_fft.set_ydata(y_fft)
    line.set_ydata(data)
    fig.canvas.draw()
    fig.canvas.flush_events()
