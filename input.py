import sys
import pygame
from pygame.locals import *

class Input(object):
    current = None
    def __init__(self):
        Input.current = self
        self.mouse_pos = 0,0
        self.mouse_delta = 0,
        self.mouse_moved = False
        
        self._keys_begin = []
        self._keys_last = []
        self._keys = []
        self._keys_end = []

        self._mouse_keys_begin = []
        self._mouse_keys_last = []
        self._mouse_keys = []
        self._mouse_keys_end = []
    
    # @property
    # def mouse_pos(self):
    #     return self._mouse_pos
    # @property
    # def mouse_delta(self):
    #     return self._mouse_delta
    
    def update(self):
        pygame.event.pump()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        # Update Mouse
        self.mouse_delta = pygame.mouse.get_rel()
        self.mouse_pos = pygame.mouse.get_pos()

        self._keys = pygame.key.get_pressed()
        self._mouse_keys = pygame.mouse.get_pressed()
        # # Update the keys
        # del self._keys_begin[:]
        # del self._keys_end[:]
        # self._keys = pygame.key.get_pressed()
        # for key in self._keys:
        #     if key not in self._keys_last:
        #         self._keys_begin.append(key)
        # for key in self._keys_last:
        #     if key not in self._keys:
        #         self._keys_end.append(key)
        # del self._keys_last[:]
        # self._keys_last.extend(self._keys)
        # 
        # # Update the mouse keys
        # del self._mouse_keys_begin[:]
        # del self._mouse_keys_end[:]
        # self._mouse_keys = pygame.mouse.get_pressed()
        # for key in self._mouse_keys:
        #     if key not in self._mouse_keys_last:
        #         self._mouse_keys_begin.append(key)
        # for key in self._mouse_keys_last:
        #     if key not in self._mouse_keys:
        #         self._mouse_keys_end.append(key)
        # del self._mouse_keys_last[:]
        # self._mouse_keys_last.extend(self._mouse_keys)
        
    # def key_began(self, key):
    #     return key in self._keys_begin
    def key_pressed(self, key):
        return self._keys[key]
    # def key_ended(self, key):
    #     return key in self._keys_end
    # def mouse_began(self, key):
    #     return key in self._mouse_keys_begin
    def mouse_pressed(self, key):
        return key in self._mouse_keys
    # def mouse_ended(self, key):
    #     return key in self._mouse_keys_end
        