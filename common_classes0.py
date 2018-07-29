import pygame
import pymunk
import math

from common import *

class Transform(object):
    def __init__(self):
        self._position = pymunk.Vec2d(0, 0)  # The center of this object
        self._angle_degrees = 0.0  # In degrees
        self._scale = 1.0

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        self.set_position(value)

    @property
    def angle(self):
        return self._angle_degrees
    @angle.setter
    def angle(self, value):
        self.set_angle(value)

    @property
    def scale(self):
        return self._scale
    @scale.setter
    def scale(self, value):
        self.set_scale(value)

    def set_position(self, value):
        self._position = pymunk.Vec2d(value)
    def set_angle(self, value):
        self._angle_degrees = wrap(float(value), -180, 180)
    def set_scale(self, value):
        self._scale = clamp(float(value), 0.01, 100)

# class RectTransform(Transform):
#     def __init__(self):
#         Transform.__init__(self)
#         self.anchor = pymunk.Vec2d(0.5,0.5)
#     
#     @property
#     def anchored_pos(self):
#         return self.position
#     @property
#     def position(self):
#         return self.position


class Camera(Transform):
    def __init__(self, dimentions, position=(0, 0)):
        # Position is the camera's topleft corner
        super(Camera, self).__init__()
        self.rect = pygame.Rect(0, 0, dimentions[0], dimentions[1])
        self.position = position

    @property
    def dimensions(self):
        return self.rect.size

    @dimensions.setter
    def dimensions(self, value):
        self.rect.size = value


    def set_position(self, value):
        Transform.set_position(self, value)
        self.rect.center = value

    def world_to_screen_point(self, vect):
        out_vect = pymunk.Vec2d(vect)
        out_vect = out_vect - self.rect.bottomleft # Not topleft because then y would be negative
        out_vect[1] *= -1
        return out_vect

    def screen_to_world_point(self, vect):
        out_vect = pymunk.Vec2d(vect)
        out_vect[1] *= -1
        out_vect = out_vect + self.rect.bottomleft # Not topleft because then y would be negative
        return out_vect

    def world_to_screen_vector(self, vect):
        out_vect = vect / self.scale;
        out_vect.y *= -1
        return out_vect

    def screen_to_world_vector(self, vect):
        out_vect = vect * self.scale;
        out_vect.y *= -1
        return out_vect

class Rigidbody(Transform):
    def __init__(self):
        super(Rigidbody, self).__init__()
        self.body = pymunk.Body(1, pymunk.moment_for_box(1 ,(2, 2)))
        self.shapes = []
        self.linear_drag = 0.
        self.angular_drag = 0.

    def update(self):
        if self.body.body_type == pymunk.Body.DYNAMIC:
            self.body.velocity *= 1.0 - self.linear_drag
            self.body.angular_velocity *= 1.0 - self.angular_drag
            self.position = self.body.position
            self.angle = math.degrees(self.body.angle)

    # @position.setter
    # def position(self, value):
    #     # Transform.position(self, value)
    #     super(Rigidbody, self).position = value
    #     self.body.position = value
    # 
    # @angle.setter
    # def angle(self, value):
    #     super(Rigidbody, self).angle = value
    #     self.body.angle = math.radians(value)
    #     self.body.angle = wrap(self.body.angle, -math.pi, math.pi)

    def set_position(self, value):
        super(Rigidbody, self).set_position(value)
        self.body.position = value

    def set_angle(self, value):
        super(Rigidbody, self).set_angle(value)
        self.body.angle = math.radians(self.angle)