import pygame 
import sys
import random
import os
from pygame.locals import *

#center screen 
os.environ['SDL_VIDEO_CENTERED'] = '1'

#initialize pygame
pygame.init()

# predefining some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BGCOLOR = BLACK

# setting the parameters for the screen
WIDTH = 1056                                                            
HEIGHT = 624
FPS = 100
TITLE = "Animal Crossing"
TILESIZE = 48
# sizes of the grids
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#player settings
PLAYER_SPEED = {'x': 0, 'y': 0}

# # play background music
# pygame.mixer.init()
# pygame.mixer.music.load("src/3pm.mp3")
# pygame.mixer.music.play(-1,0.0)

# display screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))



clock = pygame.time.Clock()
FPS = 30

class Player(pygame.sprite.Sprite): # player that can be moved by keys
    """Player class"""
    def __init__(self, game, x, y): 
        """creates the icon that the player can move around on the grid"""
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pygame.image.load("src/img/villager.png")
        self.rect = self.image.get_rect()
        screen.blit(self.image, self.rect)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.vx, self.vy = 0, 0

        self.rect = pygame.Rect(48, 48, 48, 48)

    def smooth_movement(self):
        """allows player to move smoothly"""

        key = pygame.key.get_pressed()

       
        if key[pygame.K_LEFT]:
            self.vx -= 18
        elif key[pygame.K_RIGHT]:
            self.vx += 18
        if key[pygame.K_UP]:
            self.vy -= 18
        elif key[pygame.K_DOWN]:
            self.vy += 18

        # friction x
        if self.vx > 12:
            self.vx -= 12
        elif self.vx >= -12:
            self.vx = 0
        else:
            self.vx += 12
        # friction y
        if self.vy > 12:
            self.vy -= 12
        elif self.vy >= -12:
            self.vy = 0
        else:
            self.vy += 12

        
        

    def update(self, x = 0, y = 0):
        """updates the player's position"""
        self.smooth_movement()

        new_x = self.x + self.vx * self.game.dt
        if 0 < new_x < 1008:
            self.x = new_x
        
        new_y = self.y + self.vy * self.game.dt
        if 0 < new_y < 576:
            self.y = new_y
        
        self.rect.x = self.x
        self.rect.y = self.y

# seperate classes for town hall and houses/trees bc town hall is 2x3 squares and trees/houses are 2x2 squares
class Hall(pygame.sprite.Sprite): 
    """Hall class"""
    def __init__(self, game, x, y):
        """makes the town hall that shows up on the screen"""
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load("src/img/townhall.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Tree1(pygame.sprite.Sprite):
    """Tree class"""
    def __init__(self, game, x, y):
        """makes tree"""
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load("src/img/tree1.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Isabelle(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        """makes isabelle (NPC)"""
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load("src/img/tree1.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Game:
    """Game class"""
    def __init__(self):
        """creates screen"""
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        """loads data"""
        pass

    def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()


    def new(self):
        """initializes all variables and places all the sprites on the grid"""
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        #player position
        self.player = Player(self, 10, 10)

        #town hall position
        Hall(self, 5, 3)

        #tree 1 position
        Tree1(self, 8, 7)
        Tree1(self, 18, 5)
        Tree1(self, 1, 9)
        Tree1(self, 12, 5)
        Tree1(self, 20, 2)

        # Isabelle(self, 10, 10)

    def run(self):
        """game loop"""
        self.playing = True
        key = pygame.key.get_pressed()

        # self.intro()

        main_menu()

        name() 

        # dialogue()

        while self.playing == True:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
        
       

    def quit(self):
        """quit the game"""
        pygame.quit()
        sys.exit()

    def update(self):
        """update portion of the game loop"""
        self.all_sprites.update()

    def draw_grid(self):
        """draw the grid"""
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, GREEN, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, GREEN, (0, y), (WIDTH, y))

    def draw(self):
        """draw everything on the screen"""

        # draw the grid 
        self.draw_grid()

        # draw the background grass
        self.screenimage = pygame.image.load("src/img/grass2.png")
        self.rect = self.screenimage.get_rect()
        screen.blit(self.screenimage, self.rect)
    


        # draw sprites
        self.all_sprites.draw(self.screen)
        pygame.display.flip()


    def events(self):
        """catch all events here"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

    


    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

def main_menu():
     
    menu = True
    selected = "start"
 
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        print("Start")
                    if selected=="quit":
                        pygame.quit()
                        quit()
 
        
        # main menu background image
        mainmenu = pygame.image.load("src/img/titleimage.png") 
        screen.blit(mainmenu,(0,0))
        
        pygame.display.set_caption("main menu")
        pygame.display.flip()

        key = pygame.key.get_pressed()
        
        if key[pygame.K_s]:
            break
        elif key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()


def name():
    name = ""
    font_name = 'src/humming_otf.otf'
    font = pygame.font.Font(font_name, 50)

    while True:
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.unicode.isalpha():
                    name += evt.unicode
                elif evt.key == K_BACKSPACE:
                    name = name[:-1]

            elif evt.type == QUIT:
                return
        
        mainmenu = pygame.image.load("src/img/nameentry.png") 
        screen.blit(mainmenu,(0,0))

        block = font.render(name, True, (254, 192, 30))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)
        
        pygame.display.flip()

        key = pygame.key.get_pressed()

        if key[pygame.K_RETURN]:
            break


# def dialogue():
#         """uhh"""
#         key = pygame.key.get_pressed()

#         selected="start"

#         dialogue = True
#         # if key[pygame.K_SPACE]:
#         while dialogue:
            
#             if key[pygame.K_SPACE]: 
#                 image = pygame.image.load('src/img/grass.png') 
#                 screen.blit(image, (0, 0)) 
#                 pygame.display.set_caption("dialogue")  
#                 pygame.display.flip()
         




# create the game object
g = Game() # abbreviation for game class

g.show_start_screen()

while True: 
    g.new()
    g.run()
    g.intro()
    g.show_go_screen()