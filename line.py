import sys, pygame
pygame.init()

size = width, height = 600, 400
hero_pos = width/2,height

bkg_colour = 0, 0, 0
line_colour = 20, 200, 20

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Awesome Line Game!")
pygame.mouse.set_visible(False)

RUNNING = True

mousex, mousey = 0, 0
mouse_pos = 0,0

clock = pygame.time.Clock()

fontsize = 16

while RUNNING:
    clock.tick()
    fps = clock.get_fps()
    for event in pygame.event.get():
        evtType = event.type
        if evtType == pygame.QUIT: RUNNING = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: RUNNING = False
            else: continue
        elif evtType == pygame.MOUSEMOTION:
            mousex, mousey = pygame.mouse.get_pos()
            mouse_pos = mousex,mousey

    myFont = pygame.font.SysFont("None", fontsize)
    screen.fill(bkg_colour)
    # thickness 2
#    pygame.draw.line(screen, line_colour, hero_pos, mouse_pos, 2 )
    # blend = 1
    pygame.draw.aaline(screen, line_colour, hero_pos, mouse_pos, 1 )
    screen.blit(myFont.render("FPS: %.2f" %fps, 0, line_colour), (10,10))
    pygame.display.flip()

pygame.mouse.set_visible(True)
sys.exit()
