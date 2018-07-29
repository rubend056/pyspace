import pygame
import pymunk
import math

from input import Input
from pygame.locals import *
from common_classes1 import *

# Formated as only the right vertices, we will mirror them
def bisymetric(side_verts):
    right_verts = []
    left_verts = []
    for xpositive, y in side_verts:
        right_verts.append((xpositive, y))
    side_verts.reverse()
    for xpositive, y in side_verts:
        left_verts.append((-xpositive, y))
    return left_verts, right_verts

def addVerts(self, verts, middle, scale, separate=False):
    vertsm = []
    for vert in verts:
        vertsm.append(((vert[0] - middle) * scale, (vert[1] - middle) * scale))
    lverts, rverts = bisymetric(vertsm)
    if separate:
        self.shapes.append(pymunk.shapes.Poly(self.body, lverts))
        self.shapes.append(pymunk.shapes.Poly(self.body, rverts))
    else:
        self.shapes.append(pymunk.shapes.Poly(self.body, lverts + rverts))

class Wall(GameObject):
    side_size = 32
    def __init__(self, x = 0, y = 0):
        GameObject.__init__(self)
        self.position = x, y
        self.body.body_type = pymunk.Body.STATIC

        size = self.side_size / 2.0 * self.scale
        verts = (
            (-size, size),
            (-size, -size),
            (size, -size),
            (size, size)
        )
        self.body.moment = pymunk.moment_for_box(5, (self.side_size, self.side_size))
        self.shapes.append(pymunk.shapes.Poly(self.body, verts))
        
        
class Ship(GameObject):
    def __init__(self):
        GameObject.__init__(self)

        self.scale = 0.5
        self.linear_drag = 0.00
        self.angular_drag = 0.00

        middle = 128
        vertsb = (
            (137, 67),
            (155, 118),
            (162, 182),
            (129, 205)
        )
        vertsw = (
            (155, 118),
            (242, 65),
            (244, 99),
            (162, 182)
        )
        moment = pymunk.moment_for_poly(10, vertsb, (-middle, -middle))
        moment += pymunk.moment_for_poly(10, vertsw, (-middle, -middle)) * 2
        self.body.moment = moment * math.pow(self.scale, 2);
        addVerts(self, vertsb, middle, self.scale, False)
        addVerts(self, vertsw, middle, self.scale, True)

        self.engine_power = 2       # Engine Power
        self.fuel = 100             # Units of fuel
        self.boosting = 0           # Are we in "boost" mode? (show the flame graphic)
    
    def update(self):
        super(Ship, self).update()
        input = Input.current
        velocity = 300.;
        
        move = pymunk.Vec2d()
        if input.key_pressed(K_a):
            move += (-velocity, 0)
        elif input.key_pressed(K_d):
            move += (velocity, 0)
        if input.key_pressed(K_w):
            move += (0, velocity)
        elif input.key_pressed(K_s):
            move += (0, -velocity)

        move.rotate(-self.body.angle)
        self.body.apply_force_at_local_point(move, (0, 0))
        
    def stats(self):
        return "Position: [%.2d,%.2d] Velocity: %.2f m/s at %.3d degrees Orientation: %.3d degrees  Fuel: %d" % (self.position.x, self.position.y, self.body.velocity.length, self.body.velocity.angle_degrees, math.degrees(self.body.angle), self.fuel)