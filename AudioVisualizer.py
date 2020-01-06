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

blues = []
for i in range(0, 64):
    blues.append((0, 255-4*i, 255))
    blues.append((0, 255-4*i, 255))

greens = []
for i in range(0, 64):
    greens.append((255-4*i, 255, 0))
    greens.append((255-4*i, 255, 0))

reds = []
for i in range(0, 64):
    reds.append((255, 255-4*i, 0))
    reds.append((255, 255-4*i, 0))

whites = []
for i in range(0, 128):
    whites.append((255, 255, 255))

strobe = [reds, greens, blues]

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


# Changes color when buttons are pressed
def button_cols(x, y, w, h, color, old_color):
    new_col = old_color
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1:
            new_col = color
    return new_col


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
text1 = font.render("Audio Visualizer", True, teal)
font = pygame.font.SysFont('timesnewroman', 18)
text2 = font.render("Reset Audio Threshold", True, black)
font = pygame.font.SysFont('timesnewroman', 10)
text3 = font.render("-Dylan Herrera 1/2020", True, white)
font = pygame.font.Font('mvboli.ttf', 16)
text4 = font.render("Gradient", True, black)
text5 = font.render("Rainbow", True, black)
text6 = font.render("Blues", True, black)
text7 = font.render("Greens", True, black)
text8 = font.render("Reds", True, black)
text9 = font.render("White", True, black)
text10 = font.render("Strobe", True, black)

# For button
button = Button("buttonback.jpg", [840, 580])
audio = Audio("button.jpg",[880,597])

# Initial threshold for typical microphone levels
maxs = .1
mins = .001

color = gradients
strobe_count = 0

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
    screen.blit(text3, [1000, 630])

    # Audio processing
    y_fft = fft_decomp(stream)
    heights = transform_fft(y_fft, maxs, mins)

    # Buttons
    maxs, mins = button_click(860, 590, 235, 34, y_fft, maxs, mins)

    # Drawing code
    # Color buttons
    pygame.draw.rect(screen, white, [1120, 20, 70, 25])
    screen.blit(text4, [1123, 22])
    color = button_cols(1120, 20, 70, 25, gradients, color)
    pygame.draw.rect(screen, white, [1120, 55, 70, 25])
    screen.blit(text5, [1123, 57])
    color = button_cols(1120, 55, 70, 25, colors, color)
    pygame.draw.rect(screen, white, [1120, 90, 70, 25])
    screen.blit(text6, [1123, 92])
    color = button_cols(1120, 90, 70, 25, blues, color)
    pygame.draw.rect(screen, white, [1120, 125, 70, 25])
    screen.blit(text7, [1123, 127])
    color = button_cols(1120, 125, 70, 25, greens, color)
    pygame.draw.rect(screen, white, [1120, 160, 70, 25])
    screen.blit(text8, [1123, 162])
    color = button_cols(1120, 160, 70, 25, reds, color)
    pygame.draw.rect(screen, white, [1120, 195, 70, 25])
    screen.blit(text9, [1123, 197])
    color = button_cols(1120, 195, 70, 25, whites, color)
    pygame.draw.rect(screen, white, [1120, 230, 70, 25])
    screen.blit(text10, [1123, 232])
    color = button_cols(1120, 230, 70, 25, strobe, color)

    count = 0
    if color != strobe:
        for i in range(128):
            if count >= len(color):  # Gradients can be switched with any color array
                count = 0
            draw_rects(x[i], heights[i], color[count])
            count += 1
    else:
        for i in range(128):
            draw_rects(x[i], heights[i], strobe[round(strobe_count)][i])
        strobe_count += .2
        if strobe_count > 2:
            strobe_count = 0


    # Update screen
    pygame.display.flip()

    # 60 FPS
    clock.tick(60)

pygame.quit()
