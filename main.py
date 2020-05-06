#!/usr/bin/env python

import pygame
import pymunk.pygame_util
import sys
import time
import pymunk

import settings as st

from objects import *
from common import *
from input import Input
from scene import Scene

pygame.init()

fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((st.SCREEN_WIDTH, st.SCREEN_HEIGHT), 0, 32)

surface = pygame.Surface(screen.get_size())
surface.fill((0, 0, 0))
surface = surface.convert()
clock = pygame.time.Clock()

pygame.key.set_repeat(1, 1)

space = pymunk.Space()
space.gravity = 0, 0  # Create a Space to contain the simulation
space.iterations = 20
print("Space iterations " + str(space.iterations))

def make_walls():
    walls = []

    half_ws = Wall.side_size / 2
    rect = pygame.Rect(0,0,10,10)
    rect.width = st.ARENA_WIDTH + Wall.side_size
    rect.height = st.ARENA_HEIGHT + Wall.side_size
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
    space.add(ship.body, ship.shapes)
    
    sprites = [ship]
    
    walls = make_walls()
    for wall in walls:
        space.add(wall.body, wall.shapes)
    sprites.extend(walls)
    
    return ship, sprites

def start():
    return time.time()
def end(var):
    return (time.time() - var) * 1000

if __name__ == '__main__':
    
    # Create scene and input
    scene = Scene()
    st.CURRENT_SCENE = scene
    ii = Input()
    st.CURRENT_INPUT = ii

    # Create crosshair
    crosshair = Sprite()
    crosshair.set_image(load_image("crosshair.png"))

    text_sprite = Sprite()
    text_sprite.ui = True
    text1_sprite = Sprite()
    text1_sprite.ui = True
    # Initialize everything and add to scene
    ship, allobjects = initialize()
    scene.objects.add(allobjects)
    scene.ui_objects.add([crosshair, text_sprite, text1_sprite])
    
    screen.blit(surface, (0, 0))

    camera = scene.camera_current

    font = pygame.font.Font(None, 14)
    
    u_time, r_time = 0.,0.
    while True:
        
        # Update physics
        space.step(st.STEP_TIME)
        
        # Update scene
        ii.update()
        t = start()
        scene.update()
        u_time = end(t)
        
        # Set crosshair and camera position
        crosshair.rect.center = ii.mouse_pos
        camera.position = ship.position

        # Set the debug texts
        text_sprite.set_image(font.render("DeltaTime: {}, Drawing: {} ".format(int(st.DELTA_TIME * 1000), len(
            scene._objects_in_screen)) + ship.stats(), 1, (255, 255, 255)))
        text_sprite.rect.centerx = st.SCREEN_WIDTH / 2

        text1_sprite.set_image(
            font.render("UpdateTime: {}, RenderTime: {}".format(int(u_time), int(r_time)), 1, (255, 255, 255)))
        text1_sprite.rect.centerx = st.SCREEN_WIDTH / 2
        text1_sprite.rect.top = text_sprite.rect.height

        # Draw to the screen
        t = start()
        scene.render(surface=screen, background=surface)
        r_time = end(t)
        
        # Draw physics debug
        if st.DEBUG:
            draw_options = pymunk.pygame_util.DrawOptions(screen)
            space.debug_draw(draw_options)
        
        pygame.display.flip()
        pygame.display.update()

        st.DELTA_TIME = float(fpsClock.tick(st.FPS))/1000  # and tick the clock.
        
