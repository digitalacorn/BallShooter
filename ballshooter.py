import os, sys, pygame
import time
import math
from collections import namedtuple as ntuple
from Bullets import Bullets,Bullet,Magnitude

#pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()

# Set up some useful named tuples to hold data
PixelPos = ntuple('PixelPos', 'x y')
PixelSize = ntuple('PixelSize', 'w h')
RGB = ntuple('RGB', 'r g b')

# initialize some global varables with magic numbers
SCREENSIZE = PixelSize(640, 480)
#SCREENSIZE = PixelSize(200, 150)
HEROSIZE = PixelSize(75,75)
BULLETSIZE = PixelSize(20,20)
CURSORRADIUS = BULLETSIZE.h/2
HEROORIGIN = PixelPos(SCREENSIZE.w/2,SCREENSIZE.h)
BULLETORIGIN = PixelPos(HEROORIGIN.x,HEROORIGIN.y-BULLETSIZE.h/2)
BKGCOLOUR = RGB(0, 0, 0)
LINECOLOUR = RGB(20, 200, 20)
CURSORCOLOUR = RGB(255, 0, 0)
MAXFPS = 100
FONTSIZE = 16
BULLETSPEED = 0.2
STATS = False
powerball = 2.5

score = 0
current_score = 0
score_time = 0
ball_angle_prev = 0.
ball_angle = 0.
mouse_pos = PixelPos(0,0)
bullets = Bullets()
Bullet.screen_size = SCREENSIZE
Bullet.speed = BULLETSPEED
Bullet.size = BULLETSIZE

# Load our sprite skins and get surfaces (+rects if possible)
ball = pygame.image.load(os.path.join("data","ball.gif"))

ballHero_scaled = pygame.transform.scale( ball, HEROSIZE )
ballHero = pygame.transform.rotate( ballHero_scaled, ball_angle )

ballBullet_scaled = pygame.transform.scale( ball, BULLETSIZE )
bullet_rect = ballBullet_scaled.get_rect()

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

aimbulletx = 0.
aimbullety = 0.
aimbullet_pos = PixelPos(0.,0.)

while RUNNING:
    # limit the frame rate and calculate the real one
    milliseconds = clock.tick(MAXFPS)
    seconds = milliseconds / 1000.0 # seconds passed since last frame
    score_time+=seconds
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
            aimbulletx = 0.5 * (HEROSIZE.w+BULLETSIZE.w) * math.cos(math.radians(ball_angle))
            aimbullety = 0.5 * (HEROSIZE.w+BULLETSIZE.w) * math.sin(math.radians(ball_angle))
            aimbullet_pos = PixelPos( (HEROORIGIN.x+aimbulletx), (HEROORIGIN.y-aimbullety) )
        elif evtType == pygame.MOUSEBUTTONDOWN:
            mouse_pos = PixelPos(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
            bulletmouse_pos = CorrectPos(mouse_pos,BULLETORIGIN)
            b = Bullet(ballBullet_scaled,aimbullet_pos,bulletmouse_pos)
            bullets.add(b)
            if len(bullets.sprites())>1:
                score+= score_time*math.pow(len(bullets.sprites()),powerball)
            score_time=0

    bullet_rect.center = ( aimbullet_pos )

    ballHero = pygame.transform.rotate( ballHero_scaled, ball_angle )
    ballHero_rect = ballHero.get_rect()
    ballHero_rect.center = HEROORIGIN
    bullets.update(milliseconds)

    for b in bullets.sprites():
        sprite_pos = PixelPos(*b.pos)
        corr_sprite_pos = CorrectPos(sprite_pos,HEROORIGIN)
        rad_dist = Magnitude(corr_sprite_pos)
        if rad_dist<=(HEROSIZE.w/2.):
            RUNNING=False
        else: continue

    pygame.draw.circle(screen, CURSORCOLOUR, mouse_pos, CURSORRADIUS, 2) # red circle
    screen.blit(ballHero, ballHero_rect)
    screen.blit(ballBullet_scaled, bullet_rect)
    for b in bullets.sprites(): screen.blit(b.image,b.rect)
    myFont = pygame.font.SysFont("None", FONTSIZE)
    current_score = score+(score_time*math.pow(len(bullets.sprites()),powerball))
    screen.blit(myFont.render("Score: %i" %current_score, 0, LINECOLOUR), (SCREENSIZE.w-200,10))
    if STATS:
        screen.blit(myFont.render("FPS: %.2f    Mouse Pos: (%i,%i)" %(fps, corr_pos.x, corr_pos.y), 0, LINECOLOUR), (10,10))
    pygame.display.flip()

ENDSCREEN = True
myFont = pygame.font.SysFont("None", FONTSIZE+30)
while ENDSCREEN:
    screen.fill(BKGCOLOUR)
    for event in pygame.event.get():
        evtType = event.type
        if evtType == pygame.QUIT: ENDSCREEN = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: ENDSCREEN = False
            else: continue
    score_surface = myFont.render("Final Score: %i" %current_score, 0, LINECOLOUR)
    score_rect = score_surface.get_rect()
    screen.blit(score_surface, ((SCREENSIZE.w/2)-(score_rect.width/2),(SCREENSIZE.h/2)-(score_rect.height/2)))
    pygame.display.flip()

pygame.quit()
#sys.exit()
