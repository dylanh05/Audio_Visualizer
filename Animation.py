# TODO: Mood classifier to change colors

import pyaudio
import pygame
import struct
import numpy as np
from scipy.fftpack import fft

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Button(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Audio(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


# For audio processing
global CHUNK, FORMAT, CHANNELS, RATE

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Colors
# Rainbow
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

# Gradient color scheme
gradients = []
for i in range(0,31):
    gradients.append((0,8*i,255))
for i in range(0,31):
    gradients.append((0,255,255-8*i))
for i in range(0,31):
    gradients.append((8*i,255,0))
for i in range(0,31):
    gradients.append((255,255-8*i,0))
for i in range(0,4):
    gradients.append((255,0,0))

colors = [red, orange, yellow, lime, green, teal, blueish, blue, violet, pink]


# Decomposes audio stream into frequencies using fast fourier transform
def fft_decomp(stream):
    data = struct.unpack(str(2 * CHUNK) + 'B', stream.read(CHUNK))
    data_np = np.array(data, dtype='b')[::2] + 128
    y_fft = fft(data_np)[::32]
    y_fft = 8* np.abs(y_fft[0:CHUNK])*2/(256*CHUNK)
    y_fft[0] = y_fft[60]
    return y_fft


def audio_threshold(y_fft):
    return max(y_fft), min(y_fft)


# Resets audio threshold for ftt transform each time button is pressed
def button_click(x, y, w, h, y_fft, maxs, mins):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1:
            maxs, mins = audio_threshold(y_fft)
    return maxs, mins


# Transforms fft values into coordinates for rectangle drawing
def transform_fft(y_fft, maxs, mins):
    heights = []
    for height in y_fft:
        normalized = round((height-mins)/(maxs-mins),2) * 100
        heights.append(int(normalized))
    return heights


# Draws column of rectangles
def draw_rects(x,height,col):
    for i in range(0,height):
        pygame.draw.rect(screen,col,[x,550-(4*i),7,3])


# Rectangle x values
x = []
for i in range(128):
    x.append(88+(8*i))

# Audio stream
p = pyaudio.PyAudio()
stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, output = True, frames_per_buffer = CHUNK)

pygame.init()
 
# Set the width and height of the screen
size = (1200, 650)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Audio Visualizer")

done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# For background picture
BackGround = Background('background.jpg', [0,0])
# For text
font = pygame.font.Font('mvboli.ttf', 32)
text1 = font.render("Audio Visualizer",True,teal)
font = pygame.font.SysFont('timesnewroman',18)
text2 = font.render("Reset Audio Threshold", True, black)
# For button
button = Button("buttonback.jpg", [840, 580])
audio = Audio("button.jpg",[880,597])

# Initial threshold for typical microphone levels
maxs = .1
mins = .001

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(black)
    screen.blit(BackGround.image, BackGround.rect)
    screen.blit(button.image, button.rect)
    screen.blit(audio.image, audio.rect)
    screen.blit(text1, [500, 580])
    screen.blit(text2, [915, 594])

    # Audio processing
    y_fft = fft_decomp(stream)
    heights = transform_fft(y_fft, maxs, mins)

    # Buttons
    maxs, mins = button_click(860, 590, 235, 34, y_fft, maxs, mins)

    # Drawing code
    count = 0
    for i in range(128):
        if count >= len(gradients):  # Gradients can be switched with any color array
            count = 0
        draw_rects(x[i], heights[i], gradients[count])
        count += 1

    # Update screen
    pygame.display.flip()

    # 60 FPS
    clock.tick(60)

pygame.quit()
