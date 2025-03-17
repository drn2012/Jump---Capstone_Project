import pygame 
import sys
import threading

pygame.init()
pygame.mixer.init()

#Creates function to show text with a black background
def showmessage(text):
    screen.fill(BLACK)
    display = font.render(text,True,WHITE)
    screen.blit(display,(WIDTH//2-display.get_width()//2,HEIGHT//2-display.get_height()//2))
    pygame.display.update()
    pygame.time.wait(2000)
       

#Screen dimensions
WIDTH = 800
HEIGHT = 405

#Frames per second
FPS = 30

#Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#Clock
clock = pygame.time.Clock()

#Screen and its image and rect
screen =  pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Jump!")
background = pygame.image.load("background_jump_larger.png")
background_rect = background.get_rect()

#Sprites' images
spikeimage = pygame.image.load("spball-removebg-preview.png")
playerimg = pygame.image.load("ninja-removebg-preview.png")
goalimg = pygame.image.load("diamond-removebg-preview.png")

#Jumping sound
jumpnoise = pygame.mixer.Sound("cartoon-jump-6462.mp3")


#When a spike should be created
n = [45,80,120,165,225,255,300,348,371,417,444]


#Loop running
running = True

#Creates a score variable
score = 0


#Fonts
font = pygame.font.SysFont("Arial",40)
smallfont = pygame.font.SysFont("Courier",20)

#Defining player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self,width,height):
        #Initializing attributes
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(playerimg,(width,height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.bottom = HEIGHT

    def update(self):
        #Jump's speed
        jumpspeed = 10

        #Getting pressed key
        keydown = pygame.key.get_pressed()

        #Player's jump
        if keydown[pygame.K_SPACE] and self.rect.bottom == HEIGHT:
            jumpnoise.play()           
            for i in range(12):
                self.rect.y -= jumpspeed
                pygame.time.delay(30)

            for i in range(12):
               self.rect.y += jumpspeed
               pygame.time.delay(30)

#Defining spike sprite
class Thorn(pygame.sprite.Sprite):
    def __init__(self):
        #Initializing attributes
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(spikeimage,(50,38))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.left = WIDTH + 40
        self.rect.bottom = HEIGHT

    def update(self):
        #Makes score global
        global score

        #Moves the spike
        speed = 10
        self.rect.x -= speed

        #Kill if the spike is out of screen and increases score by 10
        if self.rect.right < 0:
            score += 10
            self.kill()

#Goal sprite class
class Goal(pygame.sprite.Sprite):
    def __init__(self):
        #Initializing attributes
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(goalimg,(105,76))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.left = WIDTH + 40
        self.rect.bottom = HEIGHT

    def update(self):
        #Moves the spike
        speed = 10
        self.rect.x -= speed
        
        #Kill if the spike is out of screen
        if self.rect.right < 0:
            self.kill()
            
#Creating the group for all sprites
all_sprites = pygame.sprite.Group()

#Creating the group for all sprites other than the player
excluding_player = pygame.sprite.Group()

#Creating the ninja
ninja = Player(50,38)
all_sprites.add(ninja)

#Creating the group for the goal
goalgroup = pygame.sprite.Group()

#Creating the group for spikes
spikes = pygame.sprite.Group()

#Variable to count the iterations of the loop
count = 0




while running:
    #Applies the background image
    screen.blit(background,background_rect)

    #Sets the FPS
    clock.tick(FPS)

    #Counts iterations
    count += 1

    #Enables quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #Creates spikes
    if count in n:
        spike = Thorn()
        all_sprites.add(spike)
        spikes.add(spike)
        excluding_player.add(spike)

    #Creates goal
    if count == 500:
        goal = Goal()
        all_sprites.add(goal)
        excluding_player.add(goal)
        goalgroup.add(goal)


    
 

    #Updating the sprites
    threading.Thread(target=ninja.update, daemon=True).start()
    excluding_player.update()
    
    #Shows the score on screen
    scoredisplay = smallfont.render(f"Your score : {score}",True,BLACK)
    screen.blit(scoredisplay,(20,20))

    #Draws the sprites
    all_sprites.draw(screen)

    
    #Ends the game if the player touches the spike
    if pygame.sprite.spritecollide(ninja,spikes,False):
        showmessage(f"You lose! Score : {score}")
        running = False

    #Checks for collision between player and the goal
    if pygame.sprite.spritecollide(ninja,goalgroup,False):
        showmessage("You Won!")
        running = False

    #Updates the screen
    pygame.display.update()
            


#Quits the program
pygame.quit()
sys.exit()

