import pygame
import os
import math


from pygame.locals import RLEACCEL

def clamp(val, min, max):
    if val < min:
        val = min
    elif val > max:
        val = max
    return val

# Exclusive wrap, max is not included in the allowed range
def wrap(val, min, max):
    range = max - min
    if val < min:
        val += range
    elif val > max:
        val -= range
    return val

def load_image(name, colorkey = None):
    fullname = os.path.join('img', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def euler_interpolate(a, b, inter):  # Returns what should be added to a based on inter
    diff = a - b  # We get a value pointing from b to a
    if diff > 180 or diff < -180:
        rdiff = 360 - diff  # Pointer from a to b on the right direction
        return rdiff * inter
    else:
        return -1 * diff * inter
def radians_interpolate(a, b, inter):
    return math.radians(euler_interpolate(math.degrees(a), math.degrees(b), inter))
