import pygame
import pymunk
import os
import math

from common import *
from pygame.locals import RLEACCEL, QUIT, K_r, K_SPACE, K_UP, K_LEFT, K_RIGHT

class Rigidbody(object):
    def __init__(self):
        self.body = pymunk.Body(1, pymunk.moment_for_box(mass=1,size=2), pymunk.Body.STATIC)
        return super(object, self).__init__()

class Ship(pygame.sprite.DirtySprite):
    def __init__(self):
        self.engine_power = 2       # Engine Power
        self.fuel = 100             # Units of fuel
        self.boosting = 0           # Are we in "boost" mode? (show the flame graphic)
        return super(pygame.sprite.DirtySprite, self).__init__()

    def setImage(name):
        self.image, self.rect = load_image(name, -1)