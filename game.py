import pygame 
import sys
import random

from pygame.locals import *

pygame.init()

#FPS and screen settings
FPS = 60 
GameFrames = pygame.time.Clock()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400

CANVAS = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Cloud Surfing")
pygame.display.set_icon(pygame.image.load("assets/cloud.png"))

class Collectables(pygame.sprite.Sprite):

    raindrops = []

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/raindrop.png"), (40, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, 690), -10)
        self.mask = pygame.mask.from_surface(self.image)
        Collectables.raindrops.append(self)

    def update(self):
        if self.rect.top < 710:
            self.rect.y += 3
        if self.rect.top > 405:
            self.rect.center = (random.randint(0, 690), -10)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Player class
class Player(pygame.sprite.Sprite):
    # Initialize the player and assign the cloud png
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/cloud.png"), (150, 100))
        pygame.Surface.convert_alpha(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (350, 320)
        self.mask = pygame.mask.from_surface(self.image)

    # Move the player left or right
    def update(self):
        if self.rect.left > -100: #& self.rect.left < SCREEN_WIDTH - 100:
            if key_pressed[K_LEFT] or key_pressed[K_a]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < 800: # & self.rect.left < SCREEN_WIDTH:
            if key_pressed[K_RIGHT] or key_pressed[K_d]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Score class
class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.font = pygame.font.SysFont("comicsansms", 30)
        self.font.set_italic(True)
        self.color = "black"
        self.image = self.font.render("Score: " + str(self.value), True, self.color)
    
    def update(self):
        self.image = self.font.render("Score: " + str(self.value), True, self.color)

    def draw(self, surface):
        surface.blit(self.image, (10, 10))
        

# Initialize player, first raindrop, and score
P1 = Player()
RAINDROP = Collectables()
SCORE = Score()

# Create raindrop spawner event and timer
SPAWN_RAINDROP = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_RAINDROP, 5000, 0)

# Game over event and timer
# GAME_OVER = pygame.USEREVENT + 2
# pygame.time.set_timer(pygame.USEREVENT + 2, 10000, 1)

# Initialize music player and droplet sound
# Music
GAME_MUSIC = pygame.mixer.music.load("assets/floating-cat.ogg")
# Music from #Uppbeat (free for Creators!):
# https://uppbeat.io/t/michael-grubb/floating-cat
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# Sound
DROP_SOUND = pygame.mixer.Sound("assets/digital-drops.mp3")
DROP_SOUND.set_volume(0.25)

drop_counter  = 0
player_scale = 1.05

running = True


while running:

    # Draw the background, player, raindrops, and score
    CANVAS.fill("sky blue")
    P1.draw(CANVAS)
    [instance.draw(CANVAS) for instance in Collectables.raindrops]
    SCORE.draw(CANVAS)

    # Assign a key presses
    key_pressed = pygame.key.get_pressed()

    for event in pygame.event.get():
        # Check key presses
        if key_pressed[K_ESCAPE] or event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()

        #Check for raindrop spawn
        if event.type == SPAWN_RAINDROP:
            drop_counter += 1
            raindrop = Collectables()    
    
    # Check for player and raindrop collision
    for instance in Collectables.raindrops:
        if pygame.sprite.collide_mask(P1, instance):
            # Change size funtionality
            # P1.image = pygame.transform.smoothscale_by(P1.image, player_scale)
            # P1.mask = pygame.mask.from_surface(P1.image)
            # P1.rect.y = P1.rect.y / player_scale
            # Spawn raindrop and add score
            DROP_SOUND.play(0, 1000)
            instance.rect.center = (random.randint(0, 690), -10)
            SCORE.value += 1    

    # Update player/raindrop positions and score/game timer
    P1.update()
    [instance.update() for instance in Collectables.raindrops]
    SCORE.update()

    # Update and tick the display window 
    pygame.display.update()
    GameFrames.tick(FPS)