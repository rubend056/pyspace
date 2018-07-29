import pygame
import pymunk
import math

from common_classes0 import *
from scene import Scene
from common import *

class Sprite(pygame.sprite.Sprite, Transform):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        Transform.__init__(self)
        self.images = []
        self.anim_frames = 0
        self._anim_frame = 0
        self._anim_count = 0
        self._image_scale = 1
        self._image_rotation = 0
        self._image_trans_dirty = True
        self.rect = pygame.Rect(0, 0, 10, 10)  # Used for rendering
    def _set_image_scale(self, scale):
        if self._image_scale != scale:
            self._image_trans_dirty = True
        self._image_scale = scale;
    def _set_image_rotation(self, rot):
        if self._image_rotation != rot:
            self._image_trans_dirty = True
        self._image_rotation = rot;
    def update(self):
        camera = Scene.current.camera_current
        # Set scale and rotation
        self._set_image_scale (self.scale / camera.scale)
        self._set_image_rotation (self.angle - camera.angle)

        # Iterate over the animation
        if self.anim_frames > 0 and len(self.images) > 0:
            if self._anim_count >= self.anim_frames:
                if self._anim_frame < len(self.images) - 1:
                    self._anim_frame += 1
                else:
                    self._anim_frame = 0
                self._image = self.set_image(self.images[self._anim_frame])
                self._image_trans_dirty = True
                self._anim_count = 1
            else:
                self._anim_count += 1

        # Apply scale and rotation to image
        if self._image_trans_dirty and '_image' in dir(self):
            self.image = pygame.transform.rotozoom(self._image, self._image_rotation, self._image_scale)
            self._image_trans_dirty = False
            self.rect.size = self.image.get_rect().size

        # Apply position in screen based on camera
        self.rect.center = camera.world_to_screen_point(self.position)

    def set_image(self, image):
        self._image = image;
        self.rect = image.get_rect()
        self.image = self._image.copy()
        self._image_width, self._image_height = self.rect.width, self.rect.height

class GameObject(Sprite, Rigidbody):
    def __init__(self):
        Sprite.__init__(self)
        Rigidbody.__init__(self)
        self.synced = False
        
    def update(self):
        Sprite.update(self)
        Rigidbody.update(self)
        
