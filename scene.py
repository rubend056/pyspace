import pygame
import time

from common_classes1 import Camera
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Scene(object):
    current = None
    # delta_time = 0.
    def __init__(self):
        Scene.current = self
        camera = Camera((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.camera_current = camera
        self.cameras = [camera]
        self.objects = []
        self._objects_in_screen = pygame.sprite.RenderClear()
    
    def update(self):
        # self.delta_time = time.clock() - self.delta_time
        for object in self.objects:
            object.update() # Updates the rigidbody and specifics of each object
        
        # screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self._objects_in_screen.empty()
        for object in self.objects:
            if self.camera_current.rect.colliderect(object.rect_world):
                object.update_screen()
                self._objects_in_screen.add(object)
            elif object._image_trans_dirty:
                object.update_screen()
        
    
    def render(self, surface, background):
        self._objects_in_screen.clear(surface, background)
        self._objects_in_screen.draw(surface)
        
        
        