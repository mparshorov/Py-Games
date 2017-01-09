# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys, random

BLACK    = (  0,   0,   0)
GREEN    = (  0, 255,   0)
WHITE    = (255, 255, 255)
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
RED      = (255,   0,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

WINDOWH=600
WINDOWW=400
pygame.init()
screen=pygame.display.set_mode((WINDOWW,WINDOWH),0,32)
pygame.display.set_caption('Plane Shooter!')
clock = pygame.time.Clock()
def displayFadingText(fontSize, text, windowSurface, clock, sec, FPS):
    alpha=255
    alphatick=(255/FPS)
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
        windowSurface.fill(BLACK)
        windowSurface.blit(sur,surrec)
        pygame.display.update()
        alpha-=alphatick
        clock.tick(FPS)
class Livebar(pygame.sprite.Sprite):
    def __init__(self, enemy):
        pygame.sprite.Sprite.__init__(self)
        self.enemy = enemy
        self.image = pygame.Surface([self.enemy.rect.width,7])
        self.image.set_colorkey((0,0,0))
        pygame.draw.rect(self.image, (0,255,0),
                         (0,0,
                          self.enemy.rect.width,7),1)
        self.rect = self.image.get_rect() 
        self.part=float(self.enemy.rect.width)/100
    def update(self):
        self.percent = (100 * float(self.enemy.health)) / float(self.enemy.fullhealth)
        pygame.draw.rect(self.image, (0,0,0), (1,1,self.enemy.rect.width-2,5))
        pygame.draw.rect(self.image, (0,255,0), (1,1,int(self.part*self.percent),5),0)
        self.rect.centerx = self.enemy.rect.centerx
        self.rect.centery = self.enemy.rect.centery - self.enemy.rect.height /2 - 10
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([4, 6])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.ellipse(self.image,YELLOW,[0, 0, 4, 6])
        pygame.draw.ellipse(self.image,RED,[1, 2, 2, 3])
        self.rect = self.image.get_rect()
class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('./resources/'+"rocket.png").convert()
        img.set_colorkey(WHITE)
        imgrect = img.get_rect()
        imgst = pygame.transform.scale(img,[imgrect.width/4,imgrect.height/4])
        self.image = imgst
        self.rect = self.image.get_rect()
class Enemy(pygame.sprite.Sprite):
    boss=False
    def __init__(self, image, health, speed, ratio):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('./resources/'+image).convert()
        img.set_colorkey(BLACK)
        imgrect = img.get_rect()
        imgst = pygame.transform.scale(img,[imgrect.width/ratio,imgrect.height/ratio])
        self.image = imgst
        self.rect = self.image.get_rect()
        self.fullhealth=health
        self.health=health
        self.life=Livebar(self)
        self.speed = speed
        self.ratio = ratio
    def update(self):
        self.life.update()
        if self.ratio > 10:
            self.rect.y += self.speed
        else:
            self.rect.x+= self.speed
            if self.rect.right>=WINDOWW or self.rect.left<=0:
                self.speed = -self.speed
class Player(pygame.sprite.Sprite):
    change_x=0
    change_y=0
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('./resources/'+"mig.png").convert()
        img.set_colorkey(WHITE)
        imgr=img.get_rect()
        imgst = pygame.transform.scale(img,[imgr.width/11,imgr.height/11])
        self.image = imgst
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fullhealth=200
        self.health=200
        self.life=Livebar(self)      
    def changespeed_x(self,x):
        self.change_x=x
    def changespeed_y(self,y):
        self.change_y=y
    def update(self):
        self.life.update()
        old_x=self.rect.x
        new_x=old_x+self.change_x
        self.rect.x = new_x
        if self.rect.left<0 or self.rect.right>WINDOWW:
             self.rect.x=old_x
        old_y=self.rect.y
        new_y=old_y+self.change_y
        self.rect.y = new_y
        if self.rect.top < 0 or self.rect.bottom > WINDOWH:
            self.rect.y=old_y
player = Player(WINDOWW/2,WINDOWH-100)
enemy_list = pygame.sprite.Group()
enemy_bullet = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
rocket_list = pygame.sprite.Group()
player_list = pygame.sprite.Group(player)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(player.life)
shoot=False
bg = pygame.image.load('./resources/'+"bgFULL.png")
bgrec = bg.get_rect()
FPS=45
# .05 - fastest   1 - slowest
fireRate=.05
bullettick=0
ebullettick=0
playerSPEED=5
enemytick=0
NEWENEMY=FPS*2
enemy = Enemy('alienEnemy.png',20, 2, 12)
enemy.rect.x = random.randint(0+enemy.rect.width,WINDOWW-enemy.rect.width)
enemy.rect.y = 0+enemy.rect.height
enemy_list.add(enemy)
all_sprites.add(enemy)
all_sprites.add(enemy.life)
score=0
y=bgrec.height-WINDOWH
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            if event.key == K_LEFT:
                player.changespeed_x(-playerSPEED)
            if event.key == K_RIGHT:
                player.changespeed_x(playerSPEED)
            if event.key == K_UP:
                player.changespeed_y(-playerSPEED)
            if event.key == K_DOWN:
                player.changespeed_y(playerSPEED)
            if event.key == K_SPACE:
                shoot=True
            if event.key == ord('r'):
                rocket = Rocket()
                rocket1 = Rocket()
                rocket.rect.centerx = player.rect.left
                rocket1.rect.centerx = player.rect.right
                rocket.rect.y = player.rect.centery
                rocket1.rect.y = player.rect.centery
                rocket_list.add(rocket1)
                all_sprites.add(rocket1)
                rocket_list.add(rocket)
                all_sprites.add(rocket)
        if event.type == KEYUP:
            if event.key == K_LEFT:
                player.changespeed_x(0)
            if event.key == K_RIGHT:
                player.changespeed_x(0)
            if event.key == K_UP:
                player.changespeed_y(0)
            if event.key == K_DOWN:
                player.changespeed_y(-0)
            if event.key == K_SPACE:
                shoot=False
    bullettick+=1
    enemytick+=1
    if shoot:
        if bullettick>=FPS*fireRate:
            bullet = Bullet()
            bullet.rect.x = player.rect.centerx
            bullet.rect.y = player.rect.top+2
            bullet_list.add(bullet)
            all_sprites.add(bullet)
            bullettick=0
    if score>=10:
        enemytick=0
        enemy = Enemy('alienEnemy.png',70, 1, 4)
        enemy.rect.x = WINDOWW/2
        enemy.rect.top = 0+enemy.rect.height
        enemy_list.add(enemy)
        Enemy.boss = True
        all_sprites.add(enemy)
        all_sprites.add(enemy.life)
        score=0
    if enemytick==NEWENEMY:
        if not Enemy.boss:
            score+=1
            enemytick=0
            enemy = Enemy('alienEnemy.png',20, 2, 12)
            enemy.rect.x = random.randint(0+enemy.rect.width,WINDOWW-enemy.rect.width)
            enemy.rect.y = 0+enemy.rect.height
            enemy_list.add(enemy)
            all_sprites.add(enemy)
            all_sprites.add(enemy.life)
    for bullet in bullet_list:
        bullet.rect.y -= 5
        enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, False)
        for enemy in enemy_hit_list:
            enemy.health-=1
            bullet_list.remove(bullet)
            all_sprites.remove(bullet)               
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites.remove(bullet)
    for rocket in rocket_list:
        rocket.rect.y -= 5
        enemy_hit_list = pygame.sprite.spritecollide(rocket, enemy_list, False)
        for enemy in enemy_hit_list:
            enemy.health-=10
            rocket_list.remove(rocket)
            all_sprites.remove(rocket)       
        if rocket.rect.y < -10:
            rocket_list.remove(rocket)
            all_sprites.remove(rocket)
    for enemy in enemy_list:
        enemy.update()
        if enemy.health>=20:
            ebullettick+=1
            if ebullettick>=FPS:
                bullet = Bullet()
                bullet.rect.x = enemy.rect.centerx
                bullet.rect.y = enemy.rect.bottom+4
                enemy_bullet.add(bullet)
                all_sprites.add(bullet)
                ebullettick=0
        if enemy.rect.top > WINDOWH:
            enemy_list.remove(enemy)
            all_sprites.remove(enemy)
            all_sprites.remove(enemy.life)
        if enemy.health<=0:
            enemy_list.remove(enemy)
            all_sprites.remove(enemy)
            all_sprites.remove(enemy.life)
    for bullet in enemy_bullet:
        bullet.rect.y += 3
        player_hit_list = pygame.sprite.spritecollide(bullet, player_list, False)
        for player in player_hit_list:
            player.health-=10
            enemy_bullet.remove(bullet)
            all_sprites.remove(bullet)
        if bullet.rect.y > WINDOWH:
            enemy_bullet.remove(bullet)
            all_sprites.remove(bullet)
    screen.fill(BLUE)
    y-=1
    if y<=0:
        screen.blit(bg,bgrec,area=(0,y+bgrec.height,WINDOWW,WINDOWH+10))
    screen.blit(bg,bgrec,area=(0,y,WINDOWW,WINDOWH+10))
    if y<-WINDOWH:
        y=bgrec.height-WINDOWH
    player_list.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)