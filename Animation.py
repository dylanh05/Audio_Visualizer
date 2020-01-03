# TODO: Mood classifier to change colors

import pyaudio
import pygame
import struct
import numpy as np
from scipy.fftpack import fft

# For audio processing
global CHUNK,FORMAT,CHANNELS,RATE

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
orange = (255, 171, 0)
yellow = (255, 255, 0)
lime = (94, 255, 0)
teal = (0, 255, 255)
blueish = (0, 80, 255)
blue = (0, 0, 255)
violet = (77, 0, 255)
pink = (255, 0, 255)
colors = [red, orange, yellow, lime, green, teal, blueish, blue, violet, pink]


# Decomposes audio stream into frequencies using fast fourier transform
def fft_decomp(stream):
    data = struct.unpack(str(2 * CHUNK) + 'B', stream.read(CHUNK))
    data_np = np.array(data, dtype='b')[::2] + 128
    y_fft = fft(data_np)[::32]
    y_fft = 8* np.abs(y_fft[0:CHUNK])*2/(256*CHUNK)
    y_fft[0] = y_fft[1]
    return y_fft


# Transforms fft values into coordinates for rectangle drawing
def transform_fft(y_fft):
    mins = min(y_fft)
    maxs = max(y_fft)
    heights = []
    for height in y_fft:
        normalized = round((height-mins)/(maxs-mins),2) * 100
        heights.append(int(normalized))
    return heights


# Draws column of rectangles
def draw_rects(x,height,col):
    for i in range(0,height):
        pygame.draw.rect(screen,col,[x,500-(4*i),7,3])


# Rectangle x values
x = []
for i in range(128):
    x.append(88+(8*i))

# Audio stream
p = pyaudio.PyAudio()
stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, output = True, frames_per_buffer = CHUNK)

pygame.init()
 
# Set the width and height of the screen
size = (1200, 600)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

start = 0

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(black)

    # Audio processing
    heights = transform_fft(fft_decomp(stream))

    # Drawing code
    count = 0
    for i in range(128):
        if count >= len(colors):
            count = 0
        draw_rects(x[i],heights[i],colors[count])
        count+=1

    # Update screen
    pygame.display.flip()
 
    # 60 FPS
    clock.tick(60)

pygame.quit()
