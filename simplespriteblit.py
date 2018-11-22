# Simple sprite move 2



import pygame
import math
import random

# initiallise constants

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)


display_width = 800
display_height = 600


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):

        """ Set up the player """
        # call the parent class (Sprite) constructor

        super().__init__()

        self.image = pygame.Surface([20, 20])
        self.image.fill(red)
        self.image2 = pygame.Surface([20, 20])
        self.image2.fill(black)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # -- Atributes
        # Set speed vector

        self.change_x = 0
        self.change_y = 0
    def changespeed(self, x, y):

        self.change_x += x
        self.change_y += y

    def update(self):
        """ Find a new position for the player """

        self.rect.x += self.change_x
        self.rect.y += self.change_y

pygame.init()

screen = pygame.display.set_mode([display_width, display_height])

# this lists every sprite

all_sprites_list = pygame.sprite.Group()

#create a player

player = Player(40, 100)
all_sprites_list.add(player)
# play.rect = player.get_rect(self.image)
# loop untill done

done = False
# manage screen update speed
clock = pygame.time.Clock()
player.xspeed = 0
player.yspeed = 0

# Main loop untill quit

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # has a keey been pressed ?
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-8, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(8, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, -8)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, 8)
        elif event.type == pygame.KEYUP:
        # Reset speed if key released
            if event.key == pygame.K_LEFT:
                player.changespeed(8, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-8, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, 8)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -8)
    # --- Game Logic
    all_sprites_list.update()
    #fill black if needed
    all_sprites_list.draw(screen)
    screen.blit(player.image, (player.rect.x, player.rect.y))
    pygame.display.update()
    screen.blit(player.image2, (player.rect.x, player.rect.y))
    clock.tick(60)
pygame.quit()
