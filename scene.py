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
        self.objects = []
        self._objects_in_screen = pygame.sprite.RenderClear()
    
    def update(self):
        for object in self.objects:
            object.update()
        
        
        # self._objects_in_screen.empty()
        # for sprite in self.objects:
        #     # if self.camera_current.rect.colliderect(sprite.rect):
        #     self._objects_in_screen.add(sprite)
        
    
    def render(self, surface, background):
        self._objects_in_screen.clear(surface, background)
        self._objects_in_screen.draw(surface)
        
        
        