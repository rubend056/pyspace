#!/usr/bin/env python

import pygame
import pymunk.pygame_util
import sys
import time
import pymunk
import os
import random
import math

from settings import *
from objects import *
from common import *
from input import Input
from scene import Scene
from pygame.locals import *

pygame.init()

fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

surface = pygame.Surface(screen.get_size())
surface.fill((0, 0, 0))
surface = surface.convert()
clock = pygame.time.Clock()

pygame.key.set_repeat(1, 1)

space = pymunk.Space()
space.gravity = 0, 0  # Create a Space to contain the simulation
space.iterations += 50
print("Space iterations " + str(space.iterations))

def make_walls():
    walls = []

    half_ws = Wall.side_size / 2
    rect = pygame.__rect_constructor(0,0,10,10)
    rect.width = ARENA_WIDTH + Wall.side_size
    rect.height = ARENA_HEIGHT + Wall.side_size
    rect.center = 0,0
    x = rect.left
    for y in range(rect.top, rect.bottom, Wall.side_size):
        walls.append(Wall(x,y))
    y = rect.bottom
    for x in range(rect.left, rect.right, Wall.side_size):
        walls.append(Wall(x, y))
    x = rect.right
    for y in range(rect.bottom, rect.top, -Wall.side_size):
        walls.append(Wall(x,y))
    y = rect.top
    for x in range(rect.right, rect.left, -Wall.side_size):
        walls.append(Wall(x,y))


    image0 = load_image("wall0.png").convert()
    image1 = load_image("wall1.png").convert()
    image2 = load_image("wall2.png").convert()
    image3 = load_image("wall3.png").convert()
    images = [image0, image1, image2, image3]
    for wall in walls:
        wall.set_image(image3)
        wall.images = images
        wall.anim_frames = 0

    return walls

def initialize():
    ship = Ship()
    ship.set_image(load_image("ship_gun0.png"))
    space.add(ship.body, ship.shapes)
    
    sprites = [ship]
    
    walls = make_walls()
    for wall in walls:
        space.add(wall.body, wall.shapes)
    sprites.extend(walls)
    
    return ship, pygame.sprite.RenderClear(sprites)

step_time = 1./FPS

t = 0.
def start():
    return time.clock()
def end(var):
    return (time.clock() - var) * 1000

if __name__ == '__main__':
    
    # Create scene and input
    scene = Scene()
    ii = Input()

    # Create crosshair
    crosshair = Sprite()
    crosshair.set_image(load_image("crosshair.png"))
    crosshair.scale = 2

    # Initialize everything and add to scene
    ship, allobjects = initialize()
    allobjects.add(crosshair)
    scene.objects.extend(allobjects)
    scene._objects_in_screen.add(scene.objects)
    
    screen.blit(surface, (0, 0))
    
    delta_time = step_time
    camera_v = 5.;

    camera = scene.camera_current
    
    
    while True:
        
        # Update physics
        space.step(step_time)

        t = start()
        ii.update()
        scene.update()
        t = end(t)
        mouse_pos = ii.mouse_pos

        if ii.key_pressed(K_f):
            pygame.display.toggle_fullscreen()
        if ii.key_pressed(K_ESCAPE):
            pygame.quit()
            sys.exit()
        
        
        font = pygame.font.Font(None, 14)

        text = font.render("DeltaTime: {}, Drawing: {}".format(delta_time, len(scene._objects_in_screen)) + ship.stats(), 1, (255, 255, 255))
        textpos = text.get_rect()
        textpos.centerx = SCREEN_WIDTH / 2
        

        

        # pygame.draw.line(screen, (0, 255, 255),
        #                  ship.rect.center, 
        #                  ship.rect.center + camera.world_to_screen_vector(ship.body.velocity) / 4, 
        #                  2)

        mouse_vec = camera.screen_to_world_point(mouse_pos) - ship.position
        mouse_vec = camera.world_to_screen_vector(mouse_vec)
        
        crosshair.position = camera.screen_to_world_point(mouse_pos)
        camera.position = ship.position

        ship.angle = -mouse_vec.angle_degrees - 90
        pygame.draw.line(screen, (0, 255, 0), ship.rect.center, ship.rect.center + mouse_vec.normalized() * 10, 2)
        
        # Do all time testing here
        # t = time.clock()
        
        start()
        # screen.blit(surface, (0, 0))
        # Do the drawing
        
        
        
        
        text1 = font.render("Time: {}".format(t), 1, (255, 255, 255))
        text1pos = text1.get_rect()
        text1pos.y = textpos.height
        text1pos.centerx = SCREEN_WIDTH / 2

        screen.blit(surface, textpos, textpos)
        screen.blit(surface, text1pos, text1pos)
        scene.render(screen, surface)
        
        if DEBUG:
            draw_options = pymunk.pygame_util.DrawOptions(screen)
            space.debug_draw(draw_options)
        
        screen.blit(text, textpos)
        screen.blit(text1, text1pos)
        
        
        
        pygame.display.flip()
        pygame.display.update()
        
        delta_time = float(fpsClock.tick(FPS)) / 1000.0  # and tick the clock.
        # delta_time = scene.delta_time
