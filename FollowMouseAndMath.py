import pygame, sys, time, math
from pygame.locals import *
def getAngle(x1, y1, x2, y2):
    rise = y1 - y2
    run = x1 - x2
    angle = math.atan2(run, rise) # get the angle in radians
    angle = angle * (180 / math.pi) # convert to degrees
    angle = (angle + 90) % 360 # adjust for a right-facing sprite
    return angle
pygame.init()
windowW=800
windowH=600
screen = pygame.display.set_mode((windowW,windowH),0,32)
pygame.display.set_caption('TIMETEST')
clock=pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
timetick=0
tick=1
times = 20
step=0
xPos=0
car=pygame.image.load('./resources/car.png').convert()
strech=pygame.transform.scale(car,(30,60))
rotate=pygame.transform.rotate(strech,-90)
carrec=rotate.get_rect()
carrec.center = (100,100)
alpha=255
alphatick=alpha/times
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
    screen.fill((0,0,0))
    minutes = times/60
    seconds = times % 60
    output = 'Time left: {0:02}:{1:02}'.format(minutes,seconds)
    text = font.render(output,True,(255,255,255))
    textrec = text.get_rect()
    sur = pygame.Surface(textrec.size)
    surrec = sur.get_rect()
    surrec.center = screen.get_rect().center
    textrec.center = sur.get_rect().center  
    sur.set_alpha(alpha)
    sur.blit(text,textrec)
    screen.blit(sur,surrec)
    timetick+=1
    if timetick==30:
        step += 0.3
        step %= 2 * math.pi
        timetick=0
        times-=tick
        alpha-=alphatick
    if not times:
        screen.fill((0,0,0))
        texts = font.render('TIME IS OUT',True,(255,255,255))
        textsrec = texts.get_rect()
        textsrec.center = screen.get_rect().center
        screen.blit(texts,textsrec)
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        sys.exit(0)
    mousex, mousey = pygame.mouse.get_pos()
    degrees = getAngle(carrec.center[0], carrec.center[1], mousex, mousey)
    rotatedSurf = pygame.transform.rotate(rotate,degrees)
    screen.blit(rotatedSurf,carrec)
    xPos = -1*math.cos(step) * 180
    yPos = -1*math.sin(step) * 180 
    pygame.draw.line(screen, (255,0,0),(400,300),(int(xPos)+400, int(yPos)+300))
    pygame.draw.circle(screen, (255,0,255), (int(xPos)+400, int(yPos)+300), 30)    
    pygame.display.flip()
    clock.tick(30)