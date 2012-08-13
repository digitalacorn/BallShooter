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
        for sprite in self.sprites(): self.colliding = False
        for sprite1 in self.sprites():
            for sprite2 in self.sprites():
                if sprite1!=sprite2:
                    diff_vec = self.AddVector(sprite1.pos,self.MultiplyVector(sprite2.pos,-1.))
                    r = self.Magnitude(diff_vec)
#                    if pygame.sprite.collide_circle(sprite1, sprite2):
                    if r<(float(sprite1.radius)+float(sprite2.radius)):
                        sprite1.Collision(sprite2)
                    else: continue
                else: continue

    def Magnitude(self, vec):
        square_sum=0.
        root = 0
        for x in vec:
            square_sum+=math.pow(x,2)
            root+=1
        return math.pow(square_sum,1./root)

    def AddVector(self,vec1,vec2):
        add_vec = []
        for element in zip(vec1,vec2):
            add_vec.append(element[0]+element[1])
        return add_vec

    def MultiplyVector(self,vec,scale):
        new_vec = []
        for element in vec:
            new_vec.append(element*scale)
        return new_vec


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
        self.collision_velocity = self.velocity
        self.colliding = False

    def update(self, milliseconds):
        if self.colliding: self.velocity = self.collision_velocity
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

    def Magnitude(self, vec):
        square_sum=0.
        root = 0
        for x in vec:
            square_sum+=math.pow(x,2)
            root+=1
        return math.pow(square_sum,1./root)

    def DotProduct(self, vec1, vec2):
        dot_prod = 0.
        for element in zip(vec1,vec2):
            dot_prod += element[0]*element[1]
        return dot_prod

    def AddVector(self,vec1,vec2):
        add_vec = []
        for element in zip(vec1,vec2):
            add_vec.append(element[0]+element[1])
        return add_vec

    def MultiplyVector(self,vec,scale):
        new_vec = []
        for element in vec:
            new_vec.append(element*scale)
        return new_vec

    def Collision(self,other):
        self.colliding = True
        normal12 = self.AddVector(other.pos,self.MultiplyVector(self.pos,-1.))
        n_scale = 1./self.Magnitude(normal12)
        normal12 = self.MultiplyVector(normal12,n_scale)

        v_self_dot = self.DotProduct(self.velocity,normal12)
        v_other_dot = self.DotProduct(other.velocity,normal12)
        v_self12 = self.MultiplyVector(normal12,v_self_dot)
        v_other12 = self.MultiplyVector(normal12,v_other_dot)

        v_self_tangent = self.AddVector(self.velocity, self.MultiplyVector(v_self12,-1.))
        v_other_tangent = self.AddVector(other.velocity, self.MultiplyVector(v_other12,-1.))

        v_newself12 = v_other12
        self.collision_velocity = self.AddVector(v_newself12,v_self_tangent)

