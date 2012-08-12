from collections import namedtuple as ntuple
import pygame
import math

PixelSize = ntuple('PixelSize', 'w h')

class Bullets(pygame.sprite.Group):
    def __init__(self,sprite=()):
        pygame.sprite.Group.__init__(self,sprite)
    def update(self,milliseconds):
        self.CheckSpriteCollisions()
        pygame.sprite.Group.update(self,milliseconds)
    def CheckSpriteCollisions(self):
        for sprite1 in self.sprites():
            for sprite2 in self.sprites():
                if sprite1!=sprite2:
                    if pygame.sprite.collide_circle(sprite1, sprite2):
                        sprite1.Collision(sprite2)
                    else: continue
                else: continue

class Bullet(pygame.sprite.Sprite):
    screen_size = PixelSize(640,480)
    speed = 0.5
    size = PixelSize(10,10)
    def __init__(self, surface, origin_pos ,mouse_pos ):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.center = origin_pos
        self.pos = [float(origin_pos[0]), float(origin_pos[1])]
        self.radius = Bullet.size.w/2
        scale = 1/math.sqrt( math.pow(mouse_pos.x,2) + math.pow(mouse_pos.y,2) )
        vx = scale * mouse_pos.x * Bullet.speed
        vy = -scale * mouse_pos.y * Bullet.speed
        self.velocity = [vx, vy]

    def update(self, milliseconds):
        if self.rect.left < 0: 
            self.pos[0] = Bullet.size.w/2 
            self.velocity[0] = -self.velocity[0]
        elif self.rect.right > Bullet.screen_size.w:
            self.pos[0] = Bullet.screen_size.w - Bullet.size.w/2
            self.velocity[0] = -self.velocity[0]
        if self.rect.top < 0:
            self.pos[1] = Bullet.size.h/2
            self.velocity[1] = -self.velocity[1]
        elif self.rect.bottom > Bullet.screen_size.h:
            self.pos[1] = Bullet.screen_size.h - Bullet.size.h/2
            self.velocity[1] = -self.velocity[1]
        dx = self.velocity[0]*milliseconds
        dy = self.velocity[1]*milliseconds
        self.pos[0] = self.pos[0]+dx
        self.pos[1] = self.pos[1]+dy
        self.rect.center = tuple(self.pos)

    def Collision(self,other):
        speed = math.sqrt(math.pow(self.velocity[0],2)+math.pow(self.velocity[1],2))
        dx = other.pos[0]-self.pos[0]
        dy = other.pos[1]-self.pos[1]
        if dx > 0:
            if dy > 0:
                angle = math.degrees(math.atan(dy/dx))
                vx = -speed*math.cos(math.radians(angle))
                vy = -speed*math.sin(math.radians(angle))
            elif dy < 0:
                angle = math.degrees(math.atan(dy/dx))
                vx = -speed*math.cos(math.radians(angle))
                vy = -speed*math.sin(math.radians(angle))
        elif dx < 0:
            if dy > 0:
                angle = 180 + math.degrees(math.atan(dy/dx))
                vx = -speed*math.cos(math.radians(angle))
                vy = -speed*math.sin(math.radians(angle))
            elif dy < 0:
                angle = -180 + math.degrees(math.atan(dy/dx))
                vx = -speed*math.cos(math.radians(angle))
                vy = -speed*math.sin(math.radians(angle))
        elif dx == 0:
            if dy > 0:
                angle = -90
            else:
                angle = 90
            vx = speed*math.cos(math.radians(angle))
            vy = speed*math.sin(math.radians(angle))
        elif dy == 0:
            if dx < 0:
                angle = 0
            else:
                angle = 180
            vx = speed*math.cos(math.radians(angle))
            vy = speed*math.sin(math.radians(angle))
        self.velocity[0] = vx
        self.velocity[1] = vy

