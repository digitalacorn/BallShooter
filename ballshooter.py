import os, sys, pygame
import time
import math
from collections import namedtuple as ntuple
from Bullets import Bullets,Bullet

#pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()

# Set up some useful named tuples to hold data
PixelPos = ntuple('PixelPos', 'x y')
PixelSize = ntuple('PixelSize', 'w h')
RGB = ntuple('RGB', 'r g b')

# initialize some global varables with magic numbers
SCREENSIZE = PixelSize(640, 480)
#SCREENSIZE = PixelSize(200, 150)
HEROSIZE = PixelSize(50,50)
BULLETSIZE = PixelSize(20,20)
CURSORRADIUS = BULLETSIZE.h/2
HEROORIGIN = PixelPos(SCREENSIZE.w/2,SCREENSIZE.h)
BULLETORIGIN = PixelPos(HEROORIGIN.x,HEROORIGIN.y-BULLETSIZE.h)
BKGCOLOUR = RGB(0, 0, 0)
LINECOLOUR = RGB(20, 200, 20)
CURSORCOLOUR = RGB(255, 0, 0)
MAXFPS = 100
FONTSIZE = 16
BULLETSPEED = 0.1
STATS = False

score = 0
score_time = 0
ball_angle_prev = 0.
ball_angle = 0.
mouse_pos = PixelPos(0,0)
#bullets = pygame.sprite.Group()
bullets = Bullets()
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

def CorrectPos(pos,origin):
        relx = pos.x - origin.x
        rely = origin.y - pos.y
        relpos = PixelPos(relx,rely)
        return relpos

corr_pos = CorrectPos(mouse_pos,HEROORIGIN)

while RUNNING:
    # limit the frame rate and calculate the real one
    milliseconds = clock.tick(MAXFPS)
    seconds = milliseconds / 1000.0 # seconds passed since last frame
    score_time+=seconds
    score+= score_time*math.pow(len(bullets.sprites()),2)
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
            corr_pos = CorrectPos(mouse_pos,HEROORIGIN)
            ball_angle_rad = math.atan2(float(corr_pos.y),float(corr_pos.x))
            ball_angle = math.degrees(ball_angle_rad)
        elif evtType == pygame.MOUSEBUTTONDOWN:
            mouse_pos = PixelPos(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
            bulletmouse_pos = CorrectPos(mouse_pos,BULLETORIGIN)
            b = Bullet(ballBullet_scaled,BULLETORIGIN,bulletmouse_pos)
            bullets.add(b)
            score_time=0

    ballHero = pygame.transform.rotate( ballHero_scaled, ball_angle )
    ballHero_rect = ballHero.get_rect()
    ballHero_rect.center = HEROORIGIN
    bullets.update(milliseconds)

    pygame.draw.circle(screen, CURSORCOLOUR, mouse_pos, CURSORRADIUS, 2) # red circle
    screen.blit(ballHero, ballHero_rect)
    for b in bullets.sprites(): screen.blit(b.image,b.rect)
    myFont = pygame.font.SysFont("None", FONTSIZE)
    screen.blit(myFont.render("Score: %i" %score, 0, LINECOLOUR), (SCREENSIZE.w-200,10))
    if STATS:
        screen.blit(myFont.render("FPS: %.2f    Mouse Pos: (%i,%i)" %(fps, corr_pos.x, corr_pos.y), 0, LINECOLOUR), (10,10))
    pygame.display.flip()

sys.exit()
