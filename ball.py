import sys, pygame
pygame.init()

size = width, height = 320, 240
speed = [1, 1]
bkg = 30, 200, 30

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.bmp")
ball = pygame.transform.scale( ball, (50,50) )
#    ball = pygame.transform.rotate( ball, -1 )
ballrect = ball.get_rect()

freq = 30
clock = 0
pygame.mouse.set_visible(False)
while 1:
    for event in pygame.event.get():
        evtType = event.type
        if evtType == pygame.QUIT: sys.exit()
        elif evtType == pygame.MOUSEMOTION:
            ballrect.center = pygame.mouse.get_pos()

#    if clock==0:
#        ballrect = ballrect.move(speed)
#        if ballrect.left < 0 or ballrect.right > width:
#            speed[0] = -speed[0]
#        if ballrect.top < 0 or ballrect.bottom > height:
#            speed[1] = -speed[1]

    screen.fill(bkg)
    screen.blit(ball, ballrect)
    pygame.display.flip()
#    clock+=1
#    clock = clock%freq
pygame.mouse.set_visible(True)
