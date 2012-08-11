import os, sys, pygame
import time
import math
from collections import namedtuple as ntuple
from Bullets import Bullet

#pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()

# Set up some useful named tuples to hold data
PixelPos = ntuple('PixelPos', 'x y')
PixelSize = ntuple('PixelSize', 'w h')
RGB = ntuple('RGB', 'r g b')

# initialize some global varables with magic numbers
SCREENSIZE = PixelSize(640, 480)
HEROSIZE = PixelSize(50,50)
BULLETSIZE = PixelSize(10,10)
CURSORRADIUS = BULLETSIZE.h/2
HEROORIGIN = PixelPos(SCREENSIZE.w/2,SCREENSIZE.h)
BULLETORIGIN = PixelPos(HEROORIGIN.x,HEROORIGIN.y-BULLETSIZE.h)
BKGCOLOUR = RGB(0, 0, 0)
LINECOLOUR = RGB(20, 200, 20)
CURSORCOLOUR = RGB(255, 0, 0)
MAXFPS = 100
FONTSIZE = 16
BULLETSPEED = 250.
STATS = False

ball_angle_prev = 0.
ball_angle = 0.
mouse_pos = PixelPos(0,0)
bullets = pygame.sprite.Group()
Bullet.screen_size = SCREENSIZE
Bullet.speed = BULLETSPEED
Bullet.size = BULLETSIZE

# Load our sprite skins and get surfaces (+rects if possible)
ball = pygame.image.load(os.path.join("data","ball.gif"))

ballHero_scaled = pygame.transform.scale( ball, HEROSIZE )
ballHero = pygame.transform.rotate( ballHero_scaled, ball_angle )

ballBullet_scaled = pygame.transform.scale( ball, BULLETSIZE )

# Make the screen do a bit of screen behaviour set up.
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption("BallShooter!")
pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
RUNNING = True
# game loop

class HeroPos(object):
    def __init__(self,origin):
        self.origin = origin
    def CorrectedPos(self,pos):
        self.pos = pos
        relx = self.pos.x - self.origin.x
        rely = self.origin.y - self.pos.y
        self.relpos = PixelPos(relx,rely)
        return self.relpos

while RUNNING:
    # limit the frame rate and calculate the real one
    milliseconds = clock.tick(MAXFPS)
    seconds = milliseconds / 1000.0 # seconds passed since last frame
    fps = clock.get_fps()
    # clear the screen
    screen.fill(BKGCOLOUR)
    # check for user inputs
    for event in pygame.event.get():
        evtType = event.type
        if evtType == pygame.QUIT: RUNNING = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: RUNNING = False
            elif event.key == pygame.K_TAB: STATS = True
            else: continue
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_TAB: STATS = False
            else: continue
        elif evtType == pygame.MOUSEMOTION:
            mouse_pos = PixelPos(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
            hp = HeroPos(HEROORIGIN)
            corr_pos = hp.CorrectedPos(mouse_pos)
            ball_angle_rad = math.atan2(float(corr_pos.y),float(corr_pos.x))
            ball_angle = math.degrees(ball_angle_rad)
        elif evtType == pygame.MOUSEBUTTONDOWN:
            mouse_pos = PixelPos(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
            hp = HeroPos(HEROORIGIN)
            corr_pos = hp.CorrectedPos(mouse_pos)
            b = Bullet(ballBullet_scaled,corr_pos)
            b.rect.center = BULLETORIGIN
            bullets.add(b)

    ballHero = pygame.transform.rotate( ballHero_scaled, ball_angle )
    ballHero_rect = ballHero.get_rect()
    ballHero_rect.center = HEROORIGIN
    pygame.draw.circle(screen, CURSORCOLOUR, mouse_pos, CURSORRADIUS, 2) # red circle
    screen.blit(ballHero, ballHero_rect)
    bullets.update(seconds)
    for b in bullets.sprites(): screen.blit(b.image,b.rect)
    if STATS:
        myFont = pygame.font.SysFont("None", FONTSIZE)
        screen.blit(myFont.render("FPS: %.2f" %fps, 0, LINECOLOUR), (10,10))
    pygame.display.flip()

sys.exit()
