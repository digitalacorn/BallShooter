from collections import namedtuple as ntuple
import pygame
import math

PixelSize = ntuple('PixelSize', 'w h')

class Bullet(pygame.sprite.Sprite):
    screen_size = PixelSize(640,480)
    speed = 50.
    size = PixelSize(10,10)
    def __init__(self, surface, mouse_pos ):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect()
        scale = 1/math.sqrt( math.pow(mouse_pos.x,2) + math.pow(mouse_pos.y,2) )
        dx = scale * mouse_pos.x * Bullet.speed
        dy = -scale * mouse_pos.y * Bullet.speed
        self.velocity = [dx, dy]

    def update(self, seconds):
        if self.rect.left < 0: 
            self.rect.left = 0
            self.velocity[0] = -self.velocity[0]
        elif self.rect.right > Bullet.screen_size.w:
            self.rect.right = Bullet.screen_size.w
            self.velocity[0] = -self.velocity[0]
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity[1] = -self.velocity[1]
        elif self.rect.bottom > Bullet.screen_size.h:
            self.rect.bottom = Bullet.screen_size.h
            self.velocity[1] = -self.velocity[1]
        self.rect = self.rect.move(self.velocity[0]*seconds, self.velocity[1]*seconds)
