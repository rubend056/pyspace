import pygame

from common_classes1 import Camera
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Scene(object):
    current = None
    def __init__(self):
        Scene.current = self
        camera = Camera((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.camera_current = camera
        self.cameras = [camera]
        self.objects = pygame.sprite.Group()
        self._objects_in_screen = pygame.sprite.RenderClear()
        self.ui_objects = pygame.sprite.RenderClear()
    
    def update(self):
        for object in self.objects:
            object.update() # Updates the rigidbody and specifics of each object
        for object in self.ui_objects:
            object.update()
        
        self._objects_in_screen.empty()
        for object in self.objects:
            if self.camera_current.rect.colliderect(object.rect_world):
                object.update_screen(self.camera_current)
                self._objects_in_screen.add(object)
            elif object._image_trans_dirty:
                object.update_screen(self.camera_current)
    
    def render(self, surface, background):
        self._objects_in_screen.clear(surface, background)
        self.ui_objects.clear(surface, background)
        self._objects_in_screen.draw(surface)
        self.ui_objects.draw(surface)
