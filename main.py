#!/usr/bin/env python

import pygame
import pymunk.pygame_util
import sys
import time
import pymunk
import os
import random
import math

from objects import *
from common import *
from pygame.locals import *
#from pygame.locals import *

FPS = 60

pygame.init()

fpsClock = pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
ARENA_WIDTH, ARENA_HEIGHT = 10 * SCREEN_WIDTH, 10 * SCREEN_HEIGHT 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((0, 0, 255))
clock = pygame.time.Clock()

pygame.key.set_repeat(1, 1)

space = pymunk.Space()
space.gravity = 0, 0  # Create a Space which contain the simulation

def initialize(space):
    ship = Ship()
    ship.setImage("ship.png")
    space.add(ship.body, ship.shape)
    sprites = [ship]

    # sprites.extend(boulders)
    # sprites.append(moon)
    return ship, pygame.sprite.RenderPlain(sprites)

# def add_ball(space):
#     mass = 1
#     radius = 14
#     moment = pymunk.moment_for_circle(mass, 0, radius) # 1
#     body = pymunk.Body(mass, moment) # 2
#     x = random.randint(120, 380)
#     body.position = x, 550 # 3
#     shape = pymunk.Circle(body, radius) # 4
#     space.add(body, shape)  # 5
#     return shape, body

if __name__ == '__main__':

    ship, allsprites = initialize(space)



    while True:
        
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        if keys[K_r]:
            ship, allsprites = initialize(space)
        if keys[K_LEFT]:
            ship.body.velocity -= (5, 0)
        elif keys[K_RIGHT]:
            ship.body.velocity += (5, 0)
        if keys[K_UP]:
            ship.body.velocity += (0, 5)
        elif keys[K_DOWN]:
            ship.body.velocity -= (0, 5)

        # surface.fill((255, 255, 255))

        font = pygame.font.Font(None, 14)

        text = font.render(ship.stats(), 1, (255, 255, 255))
        textpos = text.get_rect()
        textpos.centerx = SCREEN_WIDTH / 2

        ship.update_image()

        # Draw surface
        screen.blit(surface, (0, 0))
        # Draw sprites
        allsprites.update()
        allsprites.draw(screen)
        # Draw text
        screen.blit(text, textpos)

        draw_options = pymunk.pygame_util.DrawOptions(screen)
        space.debug_draw(draw_options)

        # def render_center_text(surface, screen, txt, color):
        #     font2 = pygame.font.Font(None, 36)
        #     text = font2.render(txt, 1, color)
        #     textpos = text.get_rect()
        #     textpos.centerx = SCREEN_WIDTH / 2
        #     textpos.centery = SCREEN_HEIGHT / 2
        #     surface.blit(text, textpos)
        #     screen.blit(surface, (0,0))

        # if lander.landed:
        #     if not lander.intact:
        #         lander.explode(screen)
        #         #render_center_text(surface, screen, "Kaboom! Your craft is destroyed.", (255,0,0))
        #     else:
        #         render_center_text(surface, screen, "You landed successfully!", (0, 255, 0))
        #
        #     pygame.display.flip()
        #     pygame.display.update()
        #     time.sleep(1)
        #     ship, allsprites = initialize()
        # else:

        pygame.display.flip()
        pygame.display.update()

        # Update physics
        space.step(0.015)
        fpsClock.tick(FPS)  # and tick the clock.
