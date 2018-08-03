import pygame
import pymunk
import math

import settings as st
from common_classes1 import *
from pygame.locals import *

# Formated as only the right vertices, we will mirror them
def bisymetric(side_verts):
    right_verts = []
    left_verts = []
    for xpositive, y in side_verts:
        right_verts.append((xpositive, y))
    side_verts.reverse()
    for xpositive, y in side_verts:
        left_verts.append((-xpositive, y))
    return left_verts, right_verts

def addVerts(self, mass, verts, middle, scale, separate):
    vertsm = []
    for vert in verts:
        vertsm.append(((vert[0] + middle[0]) * scale, (vert[1] + middle[1]) * scale))
    lverts, rverts = bisymetric(vertsm)
    if separate:
        a_shape = pymunk.shapes.Poly(self.body, lverts)
        b_shape = pymunk.shapes.Poly(self.body, rverts)
        a_shape.mass = mass
        b_shape.mass = mass
        self.shapes.append(a_shape)
        self.shapes.append(b_shape)
    else:
        shape = pymunk.shapes.Poly(self.body, lverts + rverts)
        shape.mass = mass
        self.shapes.append(shape)

class Wall(GameObject):
    side_size = 32
    def __init__(self, x = 0, y = 0):
        GameObject.__init__(self)
        self.position = x, y
        self.body.body_type = pymunk.Body.STATIC

        size = self.side_size / 2.0 * self.scale
        verts = (
            (-size, size),
            (-size, -size),
            (size, -size),
            (size, size)
        )
        self.body.moment = pymunk.moment_for_box(5, (self.side_size, self.side_size))
        self.shapes.append(pymunk.shapes.Poly(self.body, verts))

class Bullet(GameObject, Killable):
    radius = 15
    def __init__(self):
        GameObject.__init__(self)
        Killable.__init__(self)
        self.scale = 0.3
        self.mass = 0.1
        shape = pymunk.shapes.Circle(self.body, self.radius * self.scale)
        shape.mass = self.mass
        self.shapes.append(shape)
    def update(self):
        GameObject.update(self)
        if self.update_killable(st.DELTA_TIME):
            st.CURRENT_SCENE.objects.remove(self)
            self.body.space.remove(self.body, self.shapes)
        
    
class Particle(Sprite, Killable):
    def __init__(self):
        Sprite.__init__(self)
        Killable.__init__(self)
        self.linear_drag = 0.
        self.velocity = pymunk.Vec2d()
    def update(self):
        self.position += self.velocity * st.STEP_TIME
        self.velocity *= 1.0 - self.linear_drag * st.STEP_TIME
        if self.update_killable(st.DELTA_TIME):
            st.CURRENT_SCENE.objects.remove(self)
        

class Ship(GameObject):
    bullet_image = None
    smoke_image = None
    
    def __init__(self):
        GameObject.__init__(self)
        self.set_image(load_image("ship2.png"))
        if Ship.bullet_image == None:
            Ship.bullet_image = load_image("bullet.png")
        if Ship.smoke_image == None:
            Ship.smoke_image = load_image("smoke0.png")
        
        self.scale = 0.2
        self.mass = 10
        self.linear_drag = 0.00
        self.angular_drag = 0.00

        self.bullet_force = 2000.
        self.move_force = 1500.
        self.rot_force = 400.

        # middle = 128
        # vertsb = (
        #     (137, 67),
        #     (155, 118),
        #     (162, 182),
        #     (129, 205)
        # )
        # vertsw = (
        #     (155, 118),
        #     (242, 65),
        #     (244, 99),
        #     (162, 182)
        # )
        # moment = pymunk.moment_for_poly(20, vertsb, (-middle, -middle))
        # moment += pymunk.moment_for_poly(20, vertsw, (-middle, -middle)) * 2
        # self.body.moment = moment * math.pow(self.scale, 2);
        # addVerts(self, vertsb, (-middle, -middle), self.scale, False)
        # addVerts(self, vertsw, (-middle, -middle), self.scale, True)
        
        offset = (-74, -241)
        verts = (
            (94, 38),
            (141, 86),
            (141, 394),
            (106, 460),
            (93, 469)
        )
        
        addVerts(self, self.mass, verts, offset, self.scale, False)
        
    def update(self):
        super(Ship, self).update()
        
        input = st.CURRENT_INPUT
        
        if input.mouse_began(1) or input.key_began(K_SPACE):
            # Create bullet
            bullet = Bullet()
            bullet.kill_time = 10
            st.CURRENT_SCENE.objects.add(bullet)
            self.body.space.add(bullet.body, bullet.shapes)
            bullet.angle = self.angle
            force_pos = pymunk.Vec2d(0, 250) * self.scale
            bullet.body.velocity = self.body.velocity_at_local_point(force_pos)
            force_pos.rotate(self.body.angle)
            bullet.position = self.position + force_pos
            bullet.set_image(self.bullet_image)
            bullet.body.apply_force_at_local_point((0, self.bullet_force), (0,0))
            self.body.apply_force_at_local_point((0, -self.bullet_force), (0,0))
        
        force_list = []
        if input.key_pressed(K_w) or input.key_pressed(K_UP):
            if not input.key_pressed(K_q):
                force_vector = pymunk.Vec2d(0, self.move_force)
            else:
                force_vector = pymunk.Vec2d(0, self.move_force * 2)
            force_pos = pymunk.Vec2d(0, -210)
            force_list.append((force_pos, force_vector))
        if input.key_pressed(K_a) or input.key_pressed(K_LEFT):
            force_vector = pymunk.Vec2d(-self.rot_force, 0)
            force_pos = pymunk.Vec2d(67, 134)
            force_list.append((force_pos, force_vector))
            force_pos = pymunk.Vec2d(-67, -140)
            force_vector = force_vector * -1
            force_list.append((force_pos, force_vector))
        elif input.key_pressed(K_d) or input.key_pressed(K_RIGHT):
            force_vector = pymunk.Vec2d(self.rot_force, 0)
            force_pos = pymunk.Vec2d(-67, 134)
            force_list.append((force_pos, force_vector))
            force_pos = pymunk.Vec2d(67, -140)
            force_vector = force_vector * -1
            force_list.append((force_pos, force_vector))
        
        for force_pos, force_vector in force_list:
            force_pos *= self.scale
            self.body.apply_force_at_local_point(force_vector, force_pos)
            force_pos.rotate_degrees(self.angle)
            force_vector.rotate_degrees(self.angle)
            
            smoke = Particle()
            smoke.kill_time = 2
            smoke.scale = force_vector.length / 2000. * 0.5
            smoke.set_image(self.smoke_image)
            st.CURRENT_SCENE.objects.add(smoke)
            smoke.position = self.position + force_pos
            smoke.velocity = self.body.velocity + force_vector.normalized() * -500
            
        
    def stats(self):
        return "Position: [%.2d,%.2d] Velocity: %.2f m/s at %.3d degrees Orientation: %.3d degrees" % (self.position.x, self.position.y, self.body.velocity.length, self.body.velocity.angle_degrees, self.angle)