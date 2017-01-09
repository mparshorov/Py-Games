import pygame, random, sys
from pygame.locals import *
pygame.init()
windowW=800
windowH=600
black=(0,0,0)
blue=(0,0,255)
screen=pygame.display.set_mode((windowW,windowH),0,32)
pygame.display.set_caption('PygameFirst with Sprites')
pygame.mouse.set_visible(1)
class Block(pygame.sprite.Sprite):
    change_x=0
    change_y=0
    def __init__(self,image,size):
        pygame.sprite.Sprite.__init__(self)
        self.size=[size,size]
        self.img=pygame.image.load('./resources/'+image)
        self.image = pygame.transform.scale(self.img,self.size)
        self.rect = self.image.get_rect()
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y
    def reset_size(self, size):
        self.size=[size,size]
        self.image = pygame.transform.scale(self.img,self.size)
        self.rect.height = self.rect.width = self.image.get_rect().height
    def add_to_size(self,size):
        if self.size[0]<=100:
            self.size[0]+=size
            self.size[1]+=size
            self.image = pygame.transform.scale(self.img,self.size)
            self.rect.height = self.rect.width = self.image.get_rect().height
    def update(self, walls, speed=0):
        if speed:
            self.rect.top +=speed
        else:
            old_x=self.rect.x
            new_x=old_x+self.change_x
            self.rect.x = new_x
            # Did this update cause us to hit a wall?
            collide = pygame.sprite.spritecollide(self, walls, False)
            if collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.x=old_x
            old_y=self.rect.y
            new_y=old_y+self.change_y
            self.rect.y = new_y
            # Did this update cause us to hit a wall?
            collide = pygame.sprite.spritecollide(self, walls, False)
            if collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.y=old_y
class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        #self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([4, 10])
        self.image.fill(blue)
        self.rect = self.image.get_rect()
def add_cherry(block_list,all_sprites):
    block = Block('cherry.png',20)
    block.rect.center = (random.randint((windowW/4)+7, windowW-(windowW/4+10) - block.rect.height),0)
    block_list.add(block)
    all_sprites.add(block)
def add_enemy(enemy_list,all_sprites):
    block = Block('enemy.png',20)
    block.rect.center = (random.randint((windowW/4)+7, windowW-(windowW/4+10) - block.rect.height),0)
    enemy_list.add(block)
    all_sprites.add(block)
clock = pygame.time.Clock()
wall_list=pygame.sprite.Group()
wall=Wall((windowW/4)-5,0,0,windowH)
wall_list.add(wall)
wall=Wall((windowW/4),0,(windowW-(windowW/4))-(windowW/4),0)
wall_list.add(wall)
wall=Wall((windowW/4),windowH-5,(windowW-(windowW/4))-(windowW/4),0)
wall_list.add(wall)
wall=Wall((windowW-(windowW/4)),0,0,windowH)
wall_list.add(wall)
BG = pygame.Rect(0,0,windowW, windowH)
BGImage = pygame.image.load('./resources/BG.jpg')
BGStretchedImage = pygame.transform.scale(BGImage, (BG.width, BG.height))
playerSpeed=6
playerSize=40
SHOOT=False
while True:
    score=0
    NEWFOOD=5
    NEWENEMY=5*NEWFOOD
    foodSpeed=2
    enemySpeed=3
    foodCounter=enemyCounter=0
    bullet_list = pygame.sprite.Group()
    block_list = pygame.sprite.Group()
    enemy_list = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    player = Block('player.png',playerSize)
    player.rect.center = (screen.get_rect().center[0],
                          screen.get_rect().center[1]+200)
    all_sprites.add(player)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player.changespeed(-playerSpeed,0)
                if event.key == K_RIGHT:
                    player.changespeed(playerSpeed,0)
                if event.key == K_UP:
                    player.changespeed(0,-playerSpeed)
                if event.key == K_DOWN:
                    player.changespeed(0,playerSpeed)
                if event.key == K_SPACE:
                    SHOOT=True
                # Reset speed when key goes up
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == K_LEFT:
                    player.changespeed(playerSpeed,0)
                if event.key == K_RIGHT:
                    player.changespeed(-playerSpeed,0)
                if event.key == K_UP:
                    player.changespeed(0,playerSpeed)
                if event.key == K_DOWN:
                    player.changespeed(0,-playerSpeed)
                if event.key == K_SPACE:
                    SHOOT=False
            if event.type == MOUSEMOTION:
                if event.pos[0]>=(windowW/4)+7 and event.pos[0]<=windowW-(windowW/4+10):
                    player.rect.move_ip(event.pos[0] - player.rect.centerx, event.pos[1] - player.rect.centery)
            if event.type == MOUSEBUTTONDOWN:
                bullet = Bullet()
                bullet.rect.x = player.rect.x
                bullet.rect.y = player.rect.y
                bullet_list.add(bullet)
                all_sprites.add(bullet)
#            if event.type == MOUSEBUTTONUP:
#                print '(',event.pos[0],',',event.pos[1],')'
        if SHOOT:
            bullet = Bullet()
            bullet.rect.x = player.rect.centerx
            bullet.rect.y = player.rect.centery
            bullet_list.add(bullet)
            all_sprites.add(bullet)
        for bullet in bullet_list:
            bullet.rect.y -= 5
            # See if it hit a block
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)
            # For each block hit, remove the bollet and add to the score
            for enemy in enemy_hit_list:
                bullet_list.remove(bullet)
                all_sprites.remove(bullet)               
            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                all_sprites.remove(bullet)
        blocks_hit_list=pygame.sprite.spritecollide(player,block_list,True)
        for block in blocks_hit_list:
            score +=1
            player.add_to_size(5)
        enemy_hit_list=pygame.sprite.spritecollide(player,enemy_list,True)
        for enemy in enemy_hit_list:
            score -=10
            player.reset_size(playerSize)
        foodCounter+=1
        if foodCounter > NEWFOOD:
            foodCounter=0
            add_cherry(block_list,all_sprites)
        enemyCounter+=1
        if enemyCounter > NEWENEMY:
            enemyCounter=0
            add_enemy(enemy_list,all_sprites)
        #player.rect.center = pygame.mouse.get_pos()
        font = pygame.font.SysFont(None,28)
        text = font.render('Score: '+str(score),True,(255,255,255))
        textrec = text.get_rect()
        textrec.topleft = (0,0)
        screen.fill(black)
        screen.blit(BGStretchedImage, BG)
        screen.blit(text,textrec)
        block_list.update(wall_list, foodSpeed)
        enemy_list.update(wall_list, enemySpeed)
        player.update(wall_list)
        all_sprites.draw(screen)
        wall_list.draw(screen)
        pygame.display.flip()
        clock.tick(45)