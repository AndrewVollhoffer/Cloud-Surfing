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

running = True

CANVAS = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cloud Surfing")


class Collectables(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/raindrop.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(10, 690), 710)
    def update(self):
        if self.rect.top > -10:
            self.rect.y -= 20
        if self.rect.top < -10:
            self.rect.center = (random.randint(10, 690), 710)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/cloudpng.png"), (150, 100))
        pygame.Surface.convert_alpha(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (180, 320)

    def update(self):
        if self.rect.left > 0 & self.rect.left < SCREEN_WIDTH:
            if key_pressed[K_LEFT] or key_pressed[K_a]:
                self.rect.move_ip(-5, 0)
        if self.rect.right > 0 & self.rect.left < SCREEN_WIDTH:
            if key_pressed[K_RIGHT] or key_pressed[K_d]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

P1 = Player()   

while running:

    CANVAS.fill((255,255,255))
    P1.draw(CANVAS)

    key_pressed = pygame.key.get_pressed()

    for event in pygame.event.get():
        if key_pressed[K_ESCAPE] or event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()
    
    P1.update()

    pygame.display.update()
    GameFrames.tick(FPS)