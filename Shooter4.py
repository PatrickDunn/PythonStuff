import pygame
from pygame import *
import random
import math

black = ( 0, 0, 0)
white = ( 255, 255, 255)
red = ( 255, 0, 0)
blue = ( 0, 0, 255)

class Block(pygame.sprite.Sprite):
    """ This class  moves enemys . """
 
    def __init__(self, color, width, height):
        """ Constructor that create's the enemy image. """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
 
        # The "center" the sprite will orbit
        self.center_x = 0
        self.center_y = 0
 
        # Current angle in radians
        self.angle = 0
 
        # How far away from the center to orbit, in pixels
        self.radius = 0
 
        # How fast to orbit, in radians per frame
        self.speed = 0.05

    def update(self):
        """ Update the enemy position. """
        # Calculate a new x, y
        self.rect.x = self.radius * math.sin(self.angle) + self.center_x
        self.rect.y = self.radius * math.cos(self.angle) + self.center_y
 
        # Increase the angle in prep for the next round.
        self.angle += self.speed

class Player(pygame.sprite.Sprite):
    """ This class is the player-controlled sprite. """

    # -- Methods
    def __init__(self, x, y):
        """Constructor function"""
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(red)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # -- Attributes
        # Set speed vector
        self.change_x = 0
        self.change_y = 0

    def changespeed(self, x, y):
        """ Change the speed of the player"""
        self.change_x += x
        self.change_y += y

    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        
class Bullet(pygame.sprite.Sprite):

    def __init__(self, mouse, player):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([4, 10])
        self.image.fill(white)

        self.mouse_x, self.mouse_y = mouse[0], mouse[1]
        self.player = player

        self.rect = self.image.get_rect()
    def update(self):
        """ set user position and speed """
        speed = 4.
        range = 200
        distance = [self.mouse_x - self.player[0], self.mouse_y - self.player[1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1] / norm]
        bullet_vector = [direction[0] * speed, direction[1] * speed]
        self.rect.x += bullet_vector[0]
        self.rect.y += bullet_vector[1]
# Initialise game
pygame.init()

screen_width = 700
screen_height = 400
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode([screen_width,screen_height])
# list of all sprites
all_sprites_list = pygame.sprite.Group()

block_list = pygame.sprite.Group()

bullet_list = pygame.sprite.Group()

# Create Player
player = Player(350,200)
all_sprites_list.add(player)

# loop untill user clicks close button
done = False

clock = pygame.time.Clock()

score = 0
level = 1
levelcount = 20
player.rect.x = 350
player.rect.y = 200

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:

            bullet = Bullet(pygame.mouse.get_pos(), [player.rect.x, player.rect.y])

            bullet.rect.x = player.rect.x
            bullet.rect.y = player.rect.y

            all_sprites_list.add(bullet)
            bullet_list.add(bullet)

     # Set the speed based on the key pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, -3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, 3)

        # Reset speed when key goes up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, 3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -3)

    # --- Game logic

    if player.rect.x < -10:
        player.rect.x = 690
    if player.rect.x > 710:
        player.rect.x = 0
    if player.rect.y < -10:
        player.rect.y = 390
    if player.rect.y > 410:
        player.rect.y = 0 

    for bullet in bullet_list:

        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)

        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1

        if bullet.rect.x > 710:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

        if bullet.rect.x < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

            
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

        if bullet.rect.y > 410:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)


        # if less than ten enemys on screen create a new one
        if len(block_list) < 10:
             
            for i in range(1):

                block = Block(blue, 20, 15)

                # Set a random center location for the block to orbit
                block.center_x = random.randrange(screen_width)
                block.center_y = random.randrange(screen_height)
                # Random radius from 10 to 200
                block.radius = random.randrange(10, 200)
                # Random start angle from 0 to 2pi
                block.angle = random.random() * 2 * math.pi
                # radians per frame
                block.speed = 0.012

                block_list.add(block)

                all_sprites_list.add(block)

        if score == levelcount:
            # update level
            level  +=1          
            levelcount  +=20

    all_sprites_list.update()        

    # clear screen 
    screen.fill(black)

   

    text = font.render("Score: "+str(score), True, white)
    screen.blit(text, [10, 10])

    text = font.render("Level: "+str(level), True, white)
    screen.blit(text, [10, 40])

    text = font.render("LevelCount: "+str(levelcount), True, white)
    screen.blit(text, [10, 60])
    # Draw all sprites
    all_sprites_list.draw(screen)
    # Update Screen
    pygame.display.flip()
    # FPS
    clock.tick(60)

pygame.quit()
