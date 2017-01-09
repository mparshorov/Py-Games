import pygame
# Define some colors
resources='./resources/'
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
purple = (255,0,255)
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x,y,width,height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
class Player(pygame.sprite.Sprite):
    # -- Attributes
    # Set speed vector
    change_x=0
    change_y=0
    # This is a frame counter used to determing which image to draw
    frame = 0
    # Constructor.
    def __init__(self,x,y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # List that the cat images will be saved in.
        self.images=[]
        # Load all the cat images, from cat1.png to cat8.png.
        for i in range(1,5):
            img = pygame.image.load(resources+"mario"+str(i)+".png").convert()
            img.set_colorkey(black)
            self.images.append(img)
            # By default, use image 0
        for image in self.images[:]:
            img = pygame.transform.flip(image, True, False)
            img.set_colorkey(black)
            self.images.append(img)
        self.image = self.images[0]
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    # Change the speed of the player
    def changespeed_x(self,x):
        self.change_x=x
    def changespeed_y(self,y):
        self.change_y=y
    def jump(self):
        self.change_y-=8
    def calc_gravity(self):
        if self.change_y!=0:
            self.change_y+=.35
#        if self.change_y >= 0:
#            self.change_y = 0
        # Find a new position for the player
    def update(self,walls):
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
            if self.rect.y > screen_height-(self.rect.height*3):
                self.change_y=0
        # If we are moving right to left
        if self.change_y:
            img = pygame.image.load(resources+"mario5.png").convert()
            img.set_colorkey(black)
            self.image = img
        elif self.change_x < 0:
            # Update our frame counter
            self.frame += 1
            # We go from 0...3. If we are above image 3, reset to 0
            # Multiply by 4 because we flip the image every 4 frames
            if self.frame > 3*4:
                self.frame = 0
                # Grab the image, do floor division by 4 because we flip
                # every 4 frames.
                # Frames 0...3 -> image[0]
                # Frames 4...7 -> image[1]
                # etc.
            self.image = self.images[self.frame//4+4]
            # Move left to right. About the same as before, but use
            # images 4...7 instead of 0...3. Note that we add 4 in the last
            # line to do this.
        elif self.change_x > 0:
            self.frame += 1
            if self.frame > 3*4:
                self.frame = 0
            self.image = self.images[self.frame//4]
def setupRoomOne():
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list=pygame.sprite.Group()
    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [ [0,0,20,250,white],
             [0,350,20,250,white],
            [780,0,20,250,white],
            [780,350,20,250,white],
            [20,0,760,20,white],
            [20,580,760,20,white],
            [390,50,20,500,blue]
            ]
    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        wall=Wall(item[0],item[1],item[2],item[3],item[4])
        wall_list.add(wall)
        # return our new list
    return wall_list
def setupRoomTwo():
    wall_list=pygame.sprite.Group()
    walls = [ [0,0,20,250,white],
             [0,350,20,250,white],
            [780,0,20,250,white],
            [780,350,20,250,white],
            [20,0,760,20,white],
            [20,580,760,20,white],
            [86,83,20,screen_height-103,red],
            [176,25,20,screen_height-125,red],
            [318,107,20,screen_height-127,red],
            [437,22,20,screen_height-125,red],
            [586,168,20,screen_height-188,red]
    ]
    for item in walls:
        wall=Wall(item[0],item[1],item[2],item[3],item[4])
        wall_list.add(wall)
        # return our new list
    return wall_list
# Initialize Pygame
pygame.init()
# Set the height and width of the screen
screen_width=800
screen_height=600
screen=pygame.display.set_mode([screen_width,screen_height],pygame.DOUBLEBUF)
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()
# Create a red player block
player = Player(50,150)
all_sprites_list.add(player)
wall_list = setupRoomOne()
#Loop until the user clicks the close button.
done=False
# Used to manage how fast the screen updates
clock=pygame.time.Clock()
score = 0
# -------- Main Program Loop -----------
room=1
playerSPEED=5
while done==False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
            # Set the speed based on the key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed_x(-playerSPEED)
            if event.key == pygame.K_RIGHT:
                player.changespeed_x(playerSPEED)
            if event.key == pygame.K_UP:
                player.jump()
            if event.key == pygame.K_DOWN:
                player.changespeed_y(playerSPEED)
                # Reset speed when key goes up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed_x(0)
            if event.key == pygame.K_RIGHT:
                player.changespeed_x(0)
            #if event.key == pygame.K_UP:
                #player.changespeed_y(playerSPEED)
            if event.key == pygame.K_DOWN:
                player.changespeed_y(-0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            print '('+str(event.pos[0])+','+str(event.pos[1])+')'
                # Clear the screen
    if player.rect.x > 805 :
        if room==1:
            room=2
            wall_list = setupRoomTwo()
            player.rect.x = 10
        else:
            room=1
            wall_list = setupRoomOne()
            player.rect.x = 10
    if player.rect.x < -20:
        if room==1:
            room=2
            wall_list = setupRoomTwo()
            player.rect.x = 780
        else:
            room=1
            wall_list = setupRoomOne()
            player.rect.x = 780
    screen.fill(black)
    player.calc_gravity()
    player.update(wall_list)
    # Draw all the spites
    wall_list.draw(screen)
    all_sprites_list.draw(screen)
    # Limit to 20 frames per second
    clock.tick(30)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
pygame.quit()