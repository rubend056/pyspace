import pygame
import pymunk
import os
import math

from common import *
from pygame.locals import RLEACCEL, QUIT, K_r, K_SPACE, K_UP, K_LEFT, K_RIGHT

class Rigidbody(object):
    def __init__(self):
        self.body = pymunk.Body(1, pymunk.moment_for_box(1,(2,2)))
        self.shape = pymunk.shapes.Poly(self.body, ((-1, 1), (1, 1), (-1, -1), (1, -1)))


class DSprite(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
    def setImage(self, name):
        self.image, self.rect = load_image(name)


# class GameObject():
#     def __init__(self):
#         self.rect = pygame.__rect_constructor(0, 0, 10, 10)

class Ship(DSprite, Rigidbody):
    def __init__(self):
        DSprite.__init__(self)
        Rigidbody.__init__(self)
        # GameObject.__init__(self)
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.engine_power = 2       # Engine Power
        self.fuel = 100             # Units of fuel
        self.boosting = 0           # Are we in "boost" mode? (show the flame graphic)
    def update_image(self):
        self.rect.top = -self.body.position.y
        self.rect.left = self.body.position.x

    def stats(self):
        return "Position: [%.2d,%.2d] Velocity: %.2f m/s at %.3d degrees Orientation: %.3d degrees  Fuel: %d" % (self.rect.left, self.rect.top, self.body.velocity.length, self.body.velocity.angle, self.body.angle, self.fuel)