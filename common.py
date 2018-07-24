import pygame
import os
import math

from pygame.locals import RLEACCEL

def load_image(name, colorkey = None):
    fullname = os.path.join('img', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit(message)

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class V(object):
    """
    A simple class to keep track of vectors, including initializing
    from Cartesian and polar forms.
    """
    def __init__(self, x=0, y=0, angle=None, magnitude=None):
        self.x = x
        self.y = y

        if (angle is not None and magnitude is not None):
            self.x = magnitude * math.sin(math.radians(angle))
            self.y = magnitude * math.cos(math.radians(angle))

    @property
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    @property
    def angle(self):
        if self.y == 0:
            if self.x > 0:
                return 90.0
            else:
                return 270.0
        if math.floor(self.x) == 0:
            if self.y < 0:
                return 180.0
        return math.degrees(math.atan(self.x / float(self.y)))

    def __add__(self, other):
        return V(x=(self.x + other.x), y=(self.y + other.y))

    def rotate(self, angle):
        c = math.cos(math.radians(angle))
        s = math.sin(math.radians(angle))
        self.x = self.x * c - self.y * s
        self.y = self.x * s + self.y * c

    def __str__(self):
        return "X: %.3d Y: %.3d Angle: %.3d degrees Magnitude: %.3d" % (self.x, self.y, self.angle, self.magnitude)

