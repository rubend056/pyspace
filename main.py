#!/usr/bin/env python

import pygame
import sys
import time
import pymunk
import os
import random
import math

from common import *
from pygame.locals import RLEACCEL, QUIT, K_r, K_SPACE, K_UP, K_LEFT, K_RIGHT
#from pygame.locals import *

FPS = 60

pygame.init()

fpsClock = pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
ARENA_WIDTH, ARENA_HEIGHT = 10 * SCREEN_WIDTH, 10 * SCREEN_HEIGHT 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((0,0,0))
clock = pygame.time.Clock()

pygame.key.set_repeat(1, 1)


def initialize():
    lander = Lander()
    moon = Moon()
    sprites = [lander]
    boulders = [Boulder() for i in range(random.randint(2,5))]
    sprites.extend(boulders)
    sprites.append(moon)
    return lander, moon, boulders, pygame.sprite.RenderPlain(sprites)

def add_ball(space):
    mass = 1
    radius = 14
    moment = pymunk.moment_for_circle(mass, 0, radius) # 1
    body = pymunk.Body(mass, moment) # 2
    x = random.randint(120, 380)
    body.position = x, 550 # 3
    shape = pymunk.Circle(body, radius) # 4
    space.add(body, shape) # 5
    return shape, body

if __name__ == '__main__':

    lander, moon, boulders, allsprites = initialize()

    space = pymunk.Space()
    space.gravity = 0, 0  # Create a Space which contain the simulation

    bshape, bbody = add_ball(space)


    while True:
        
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        if keys[K_r]:
            lander, moon, boulders, allsprites = initialize()
        elif keys[K_SPACE] or keys[K_UP]:
            lander.boost()
        elif keys[K_LEFT]:
            lander.rotate(-5)
        elif keys[K_RIGHT]:
            lander.rotate(5)

        lander.check_landed(moon)
        for boulder in boulders:
            lander.check_landed(boulder)

        surface.fill((255,255,255))

        font = pygame.font.Font(None, 14)

        text = font.render(lander.stats(), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = SCREEN_WIDTH / 2
        surface.blit(text, textpos)
        screen.blit(surface, (0,0))
        allsprites.update()
        allsprites.draw(screen)

        def render_center_text(surface, screen, txt, color):
            font2 = pygame.font.Font(None, 36)
            text = font2.render(txt, 1, color)
            textpos = text.get_rect()
            textpos.centerx = SCREEN_WIDTH / 2
            textpos.centery = SCREEN_HEIGHT / 2
            surface.blit(text, textpos)
            screen.blit(surface, (0,0))

        if lander.landed:
            if not lander.intact:
                lander.explode(screen)
                #render_center_text(surface, screen, "Kaboom! Your craft is destroyed.", (255,0,0))
            else:
                render_center_text(surface, screen, "You landed successfully!", (0,255,0))

            pygame.display.flip()
            pygame.display.update()
            time.sleep(1)
            lander, moon, boulders, allsprites = initialize()
        else:
            pygame.display.flip()
            pygame.display.update()

        #Update physics
        space.step(0.02)

        fpsClock.tick(FPS) # and tick the clock.
