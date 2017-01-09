import pygame, math, sys, time
from pygame.locals import *
pygame.init()
black=(0,0,0)
screen = pygame.display.set_mode((800, 600),0,32)
clock = pygame.time.Clock()
resources='./resources/'
def displayFadingText(fontSize, text,windowSurface,clock,sec):
    """ 
    Displays a given text.
    
    fontSize -- the text size\n   
    text -- the text to be displayed\n
    windowSurface -- the surface on which the text is drawn\n
    clock -- the game clock\n
    sec -- the number of seconds the text should be displayed
    """
    alpha=255
    alphatick=(255/30)
    alphatick=alphatick/(sec-0.5)
    basicFont = pygame.font.SysFont(None, fontSize)
    text = basicFont.render(text, True, (255, 0, 0))
    textRect = text.get_rect()
    sur = pygame.Surface(textRect.size)
    surrec = sur.get_rect()
    surrec.center = windowSurface.get_rect().center
    textRect.center = sur.get_rect().center  
    while alpha>0:       
        sur.set_alpha(alpha)
        sur.blit(text,textRect)
        windowSurface.fill(black)
        windowSurface.blit(sur,surrec)
        pygame.display.update()
        alpha-=alphatick
        clock.tick(30)
        #time.sleep(.01)
class CarSprite(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    MAX_REVERSE_SPEED = 10
    ACCELERATION = 2
    TURN_SPEED = 5
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        tmpimg = pygame.image.load(image)
        streched = pygame.transform.scale(tmpimg, (30, 60))
        self.src_image = streched
        self.position = position
        self.speed = 0
        self.direction = -90
        self.k_left = self.k_right = self.k_down = self.k_up = 0
        self.rect = self.src_image.get_rect()
        self.rect.center = self.position
    def update(self, deltat):
        # SIMULATION
        self.speed += (self.k_up + self.k_down)
        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        if self.speed < -self.MAX_REVERSE_SPEED:
            self.speed = -self.MAX_REVERSE_SPEED
        self.direction += (self.k_right + self.k_left)
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += -self.speed*math.sin(rad)
        y += -self.speed*math.cos(rad)
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
class PadSprite(pygame.sprite.Sprite):
    tmp = pygame.image.load(resources+'cone.png')
    strech = pygame.transform.scale(tmp,(20,20))
    normal = strech
    hit = pygame.transform.rotate(normal,90)
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(self.normal.get_rect())
        self.rect.center = position
        self.hitlist=[]
        self.image = self.normal
        self.state = 0
    def update(self, hit_list):
        if self in hit_list: 
            self.image = self.hit
            self.state = 1
        #else: self.image = self.normal
pads = [
    PadSprite((100, 150)),
    PadSprite((600, 150)),
    PadSprite((100, 500)),
    PadSprite((600, 500)),
]
pad_group = pygame.sprite.RenderPlain(*pads)

rect = screen.get_rect()
car = CarSprite(resources+'car.png', (309,497))
car_group = pygame.sprite.RenderPlain(car)
score=0
padsss = pad_group.sprites()
background = pygame.image.load(resources+'track.png')
while 1:
    deltat = clock.tick(30)
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
            print event.pos[0], event.pos[1]
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        if event.key == K_RIGHT: car.k_right = down * -5
        elif event.key == K_LEFT: car.k_left = down * 5
        elif event.key == K_UP: car.k_up = down * 2
        elif event.key == K_DOWN: car.k_down = down * -2
        elif event.key == K_ESCAPE: sys.exit(0)
    for pad in padsss:
        if pad.state:
            score+=1
            padsss.remove(pad)
    screen.fill(black)
    screen.blit(background, (0,0))
    collisions = pygame.sprite.spritecollide(car, pad_group,False)
    pad_group.clear(screen, background)
    car_group.clear(screen, background)
    pad_group.update(collisions)
    pad_group.draw(screen)
    car_group.update(deltat)
    car_group.draw(screen)
    if not padsss:
        displayFadingText(48, 'WINNER!',screen,clock,5)
        displayFadingText(48, "Game Over!",screen,clock,3)
        pygame.quit()
        sys.exit(0)
    pygame.display.update()