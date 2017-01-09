import pygame, sys, random, time
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()
def displayText(fontSize, text, sec=0):
    basicFont = pygame.font.SysFont(None, fontSize)
    text = basicFont.render(text, True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = windowSurface.get_rect().centery
    
    windowSurface.fill(BLACK)
    windowSurface.blit(BGStretchedImage, BG)
    windowSurface.blit(text, textRect)
    pygame.display.update()
    if sec != 0:
        time.sleep(sec)
def playAgain():
    while True:
        displayText(48, 'Play Again? Y/N')
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == ord('y'):
                    return True
                elif event.key == ord('n'):
                    return False
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
def titleScreen():
    music.play(-1,0.0)
    tempmusic=True
    while True:
        basicFont = pygame.font.SysFont(None, 48)
        secondaryFont = pygame.font.SysFont(None, 40)
        text = basicFont.render("WELCOME!", True, (255, 0, 0))
        text2 = basicFont.render("Choose difficulty:", True, (255, 0, 0))
        text3 = secondaryFont.render("Press 1 for EASY", True, (255, 255, 255))
        text4 = secondaryFont.render("Press 2 for MEDIUM", True, (255, 255, 255))
        text5 = secondaryFont.render("Press 3 for HARD", True, (255, 255, 255))
        windowSurface.fill(BLACK)
        windowSurface.blit(BGStretchedImage, BG)
        textRect = text.get_rect()
        textRect.centerx = windowSurface.get_rect().centerx
        textRect.top = windowSurface.get_rect().top
        windowSurface.blit(text, textRect)
        texts=[text2,text3,text4,text5]
        height=-20
        for text in texts:
            text2Rect = text.get_rect()
            text2Rect.centerx = windowSurface.get_rect().centerx
            text2Rect.centery = windowSurface.get_rect().centery+height
            height+=40
            windowSurface.blit(text, text2Rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == ord('1'):
                    return 1
                elif event.key == ord('2'):
                    return 2
                elif event.key == ord('3'):
                    return 3
                elif event.key == ord('m'):
                    if tempmusic:
                        music.stop()
                    else:
                        music.play(-1, 0.0)
                    tempmusic = not tempmusic
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
resources='./resources/'
WINDOWWIDTH = 700
WINDOWHEIGHT = 500
'''instead of the 0 you can put pygame.FULLSCREEN'''
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption("InputGameTest")
pygame.mouse.set_visible(False)
BG = pygame.Rect(0,0,WINDOWWIDTH, WINDOWHEIGHT)
BGImage = pygame.image.load(resources+'BG.jpg')
BGStretchedImage = pygame.transform.scale(BGImage, (BG.width, BG.height))

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

music=pygame.mixer.music
pickUpSound = pygame.mixer.Sound(resources + 'pickup.wav')
missCherieSound = pygame.mixer.Sound(resources+'lose1.wav')
gameOverSound = pygame.mixer.Sound(resources+'gameover.wav')
winSound = pygame.mixer.Sound(resources+'win.wav')
enemyHit = pygame.mixer.Sound(resources+'enemyHit.wav')
musicPlaying = True
defaultPlayer = pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT-100, 20, 20)
cheats=False
while True:
    music.load(resources+'The_Misty_Mountains_Cold_The_Hobbit.wav')
    music.load(resources+'welcome.wav')
    moveLeft = moveRight = moveUp = moveDown = False
    difficulty = titleScreen()
    if difficulty == 1:
        foodSpeed=2
        enemySpeed=3
        targetScore=random.randint(40,40)
        MOVESPEED = 6
        NEWFOOD = 35
        NEWENEMY = 5 * NEWFOOD
        #gametime=60
    if difficulty == 2:
        foodSpeed=4
        enemySpeed=5
        targetScore=random.randint(40,60)
        MOVESPEED = 8
        NEWFOOD = 30
        NEWENEMY = 3 * NEWFOOD
        #gametime=80
    if difficulty == 3:
        foodSpeed=6
        enemySpeed=7
        targetScore=random.randint(60,80)
        MOVESPEED = 10
        NEWFOOD = 25
        NEWENEMY = 2 * NEWFOOD
        #gametime=100
    nlifes=3
    lifesize=25
    lifes=[]
    lifeImage = pygame.image.load(resources+'head.png')
    lifeX=(WINDOWWIDTH/4)+7
    for life in range(nlifes):
        lifes.append(pygame.Rect(lifeX, 0, lifesize, lifesize+3))
        lifeX+=lifesize
    defaultEnemySpeed = enemySpeed
    player = defaultPlayer
    playerImage = pygame.image.load(resources+'player.png')
    playerStretchedImage = pygame.transform.scale(playerImage, (player.width, player.height))
    foodCounter = 0
    FOODSIZE = 20
    foods=[]
    foodImage = pygame.image.load(resources+'cherry.png')
    foodStreched = pygame.transform.scale(foodImage, (20, 20))
    enemyCounter = 0
    ENEMYSIZE = 20
    enemies=[]
    enemyImage = pygame.image.load(resources+'enemy.png')
    enemyStreched = pygame.transform.scale(enemyImage, (20, 20))
    gameScore=0
    music.stop()
    music.load(resources+'Video_Game_Themes_-_Super_Mario_All_Stars.mid')
    if musicPlaying:
        music.play(-1, 0.0)
    displayText(48, "Collect "+str(targetScore)+" cherries!",2)
    displayText(48, "START!",2)
    pygame.mouse.set_pos(player.centerx, player.centery)
    tick=0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True
                if event.key == ord('c'):
                    cheats = True
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
                if event.key == ord('c'):
                    cheats = False
                if event.key == ord('x'):
                    player.top = random.randint(0, WINDOWHEIGHT - player.height)
                    player.left = random.randint(0, WINDOWWIDTH - player.width)
                if event.key == ord('m'):
                    if musicPlaying:
                        music.stop()
                    else:
                        music.play(-1, 0.0)
                    musicPlaying = not musicPlaying
            if event.type == MOUSEBUTTONUP:
                foods.append(pygame.Rect(event.pos[0], event.pos[1], FOODSIZE, FOODSIZE))
            if event.type == MOUSEMOTION:
                if event.pos[0]>=(WINDOWWIDTH/4)+7 and event.pos[0]<=WINDOWWIDTH-(WINDOWWIDTH/4+10):
                    player.move_ip(event.pos[0] - player.centerx, event.pos[1] - player.centery)
        '''if the line below this is enabled, the pointer is always at the
        center of the player and you can't get it out of the window'''
        #pygame.mouse.set_pos(player.centerx, player.centery)
        foodCounter += 1
        if foodCounter >= NEWFOOD:
            '''add new food'''
            foodCounter = 0
            foods.append(pygame.Rect(random.randint((WINDOWWIDTH/4)+7, WINDOWWIDTH-(WINDOWWIDTH/4+10) - FOODSIZE), 0, FOODSIZE, FOODSIZE))
        enemyCounter += 1
        if enemyCounter >= NEWENEMY:
            enemyCounter = 0
            enemies.append(pygame.Rect(random.randint((WINDOWWIDTH/4)+7, WINDOWWIDTH-(WINDOWWIDTH/4+10) - ENEMYSIZE), 0, ENEMYSIZE, ENEMYSIZE))
        ''' draw the black background onto the surface'''
        windowSurface.fill(BLACK)
        windowSurface.blit(BGStretchedImage, BG)
        if moveLeft and player.left > (WINDOWWIDTH/4)+7:
            player.move_ip(-1 * MOVESPEED, 0)
        if moveRight and player.right < WINDOWWIDTH-(WINDOWWIDTH/4+10):
            player.move_ip(MOVESPEED, 0)
        if moveUp and player.top > 0:
            player.move_ip(0, -1 * MOVESPEED)
        if moveDown and player.bottom < WINDOWHEIGHT:
            player.move_ip(0, MOVESPEED)
        ''' move the player, alternate method'''
#        if moveDown and player.bottom < WINDOWHEIGHT:
#            player.top += MOVESPEED
#        if moveUp and player.top > 0:
#            player.top -= MOVESPEED
#        if moveLeft and player.left > 0:
#            player.left -= MOVESPEED
#        if moveRight and player.right < WINDOWWIDTH:
#            player.right += MOVESPEED
        if cheats:
            enemySpeed=2
        else:
            enemySpeed=defaultEnemySpeed
        ''' draw the player onto the surface'''
        windowSurface.blit(playerStretchedImage, player)
        ''' check if the player has intersected with any food squares.
         foods[:] creates a copy of the whole list foods'''
        for food in foods[:]:
            if player.colliderect(food):
                gameScore+=1
                foods.remove(food)
                if player.width <= 100:
                    player = pygame.Rect(player.left, player.top, player.width + 2, player.height + 2)
                    playerStretchedImage = pygame.transform.scale(playerImage, (player.width, player.height))
                if musicPlaying:
                    pickUpSound.play()
            if food.top > WINDOWHEIGHT:
                if musicPlaying:
                    missCherieSound.play()
                if player.width > defaultPlayer.width:
                    player = pygame.Rect(player.left, player.top, player.width - 2, player.height - 2)
                    playerStretchedImage = pygame.transform.scale(playerImage, (player.width, player.height))
                gameScore-=1
                foods.remove(food)
        for enemy in enemies[:]:
            if player.colliderect(enemy):
                nlifes-=1
                lifes.pop()
                gameScore-=5
                enemies.remove(enemy)
                player = pygame.Rect(player.left, player.top, defaultPlayer.width, defaultPlayer.height)
                playerStretchedImage = pygame.transform.scale(playerImage, (player.width, player.height))
                if musicPlaying:
                    enemyHit.play()
            if enemy.top > WINDOWHEIGHT:
                enemies.remove(enemy)
        for enemy in enemies:
            enemy.top+=enemySpeed
            windowSurface.blit(enemyStreched, enemy)
        ''' draw the food'''
        for food in foods:
            food.top+=foodSpeed
            windowSurface.blit(foodStreched, food)
        for life in lifes:
            windowSurface.blit(lifeImage, life)
        scoreFont = pygame.font.SysFont(None, 28)
        score = scoreFont.render('Score: '+str(gameScore)+"/"+str(targetScore), True, (255, 255, 255))
        scoreRect = score.get_rect()
        scoreRect.left = 0
        scoreRect.top = 0
        windowSurface.blit(score, scoreRect)
        #minutes=gametime//60
        #seconds=gametime%60
        #gameT = scoreFont.render('Time left: {0:02}:{1:02}'.format(minutes,seconds), True, (255, 255, 255))
        #gameTRect = gameT.get_rect()
        #gameTRect.left = 0
        #gameTRect.top = 28
        #windowSurface.blit(gameT, gameTRect)
        #if tick == 45:
            #tick=0
            #gametime-=1
        tick+=1
        if not nlifes:
            result=0
            break
        if gameScore >= targetScore:
            result=1
            break
        if gameScore < 0:
            result=0
            break
        #if not gametime:
            #result=0
            #break
        ''' draw the window onto the screen'''
        pygame.display.update()
        mainClock.tick(45)
    if not result:
        pygame.mixer.music.stop()
        gameOverSound.play()
        displayText(48, 'You Lose!',3)
        displayText(48, "Game Over!",3)
        gameOverSound.stop()
    else:
        pygame.mixer.music.stop()
        winSound.play()
        displayText(48, 'WINNER!',5)
        displayText(48, "Game Over!",3)
        winSound.stop()
    again=playAgain()
    if not again:
        pygame.quit()
        sys.exit()
