#TODO: turn bottom plot into a bar graph
#BPM Analysis and change color accordingly

import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

plt.style.use('dark_background')

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, output = True, frames_per_buffer = CHUNK)

fig, (ax, ax2) = plt.subplots(2, figsize=(15, 7))
x = np.arange(0, 2 * CHUNK, 2)
x_fft = np.linspace(0,RATE,CHUNK)

line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)
line_fft, = ax2.semilogx(x_fft,np.random.rand(CHUNK),'-',lw=2)

ax.set_title('Audio Waveform')
ax.set_ylim(0, 255)
ax.set_xlim(0, 2 * CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])
plt.show(block=False)
cols = ['r','FFA500','y','g','c','b','m','w']
i = 0

while True:
    data = struct.unpack(str(2 * CHUNK) + 'B', stream.read(CHUNK))
    data_np = np.array(data, dtype='b')[::2] + 128
    y_fft = fft(data_np)
    y_fft = 8* np.abs(y_fft[0:CHUNK])*2/(256*CHUNK)
    line_fft.set_ydata(y_fft)
    line.set_ydata(data_np)
    fig.canvas.draw()
    fig.canvas.flush_events()


