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
        
        self._events = []
        
        
        
        # self._keys_begin = []
        # self._keys_last = []
        self._keys = []
        # self._keys_end = []
        # 
        # self._mouse_keys_begin = []
        # self._mouse_keys_last = []
        self._mouse_keys = []
        # self._mouse_keys_end = []
    
    # @property
    # def mouse_pos(self):
    #     return self._mouse_pos
    # @property
    # def mouse_delta(self):
    #     return self._mouse_delta
    
    def update(self):
        pygame.event.pump()
        
        self._events = pygame.event.get()
        for event in self._events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_delta = pygame.mouse.get_rel()
        self._keys = pygame.key.get_pressed()
        self._mouse_keys = pygame.mouse.get_pressed()
        
        if self.key_pressed(K_f):
            pygame.display.toggle_fullscreen()
        if self.key_pressed(K_ESCAPE):
            pygame.quit()
            sys.exit()
        
    def get_events(self, event_type):
        event_list = []
        for event in self._events:
            if event.type == event_type:
                event_list.append(event)
        return event_list
    def key_began(self, key):
        evl = self.get_events(KEYDOWN)
        for event in evl:
            if event.key == key:
                return True
        return False
    def key_pressed(self, key):
        return self._keys[key]
    # def key_ended(self, key):
    #     return key in self._keys_end
    def mouse_began(self, button):
        evl = self.get_events(MOUSEBUTTONDOWN)
        # print evl
        # if (evl > 0):
        #     return True
        for event in evl:
            if event.button == button:
                return True
        return False
    def mouse_pressed(self, key):
        return self._mouse_keys[key]
    # def mouse_ended(self, key):
    #     return key in self._mouse_keys_end
        