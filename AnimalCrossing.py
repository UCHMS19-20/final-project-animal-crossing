import pygame 
import sys
from pygame.locals import *

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
PLAYER_SPEED = 100

# # play background music
# pygame.mixer.init()
# pygame.mixer.music.load("src/3pm.mp3")
# pygame.mixer.music.play(-1,0.0)

# display screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# # center screen
# os.environ['SDL_VIDEO_CENTERED'] = '1'

def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.SysFont(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
 
    return newText
 

font = "comicsansms"

clock = pygame.time.Clock()
FPS=30

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
 
    def smooth_movement(self):
        """allows player to move smoothly"""
        # initial velocity
        self.vx, self.vy = 0, 0

        key = pygame.key.get_pressed()

        # diagonal movement
        if key[pygame.K_LEFT] and key[pygame.K_UP]:
            self.vy = -PLAYER_SPEED
            self.vx = -PLAYER_SPEED
        elif key[pygame.K_LEFT] and key[pygame.K_DOWN]:
            self.vy = PLAYER_SPEED
            self.vx = -PLAYER_SPEED
        elif key[pygame.K_RIGHT] and key[pygame.K_UP]:
            self.vy = -PLAYER_SPEED
            self.vx = PLAYER_SPEED
        elif key[pygame.K_RIGHT] and key[pygame.K_DOWN]:
            self.vy = PLAYER_SPEED
            self.vx = PLAYER_SPEED

        # straight line movement
        elif key[pygame.K_LEFT]:
            self.vx = -PLAYER_SPEED
        elif key[pygame.K_RIGHT]:
            self.vx = PLAYER_SPEED
        elif key[pygame.K_UP]:
            self.vy = -PLAYER_SPEED
        elif key[pygame.K_DOWN]:
            self.vy = PLAYER_SPEED
        
        
    def move(self, dx=0, dy=0):
        """ moves the player"""
        if not self.house_collide(dx,dy) and not self.screen_bounds(dx,dy):
            self.x += dx
            self.y += dy

    # def screen_bounds(self, dx = 0, dy = 0):
    #     """makes it so the player cannot move past the width and height constraints of the screen"""
    #     screen_there_x = False
    #     screen_there_y = False
    #     for wall in self.game.walls:
    #         if GRIDWIDTH + 1 == self.x + dx:
    #              screen_there_x = True
    #         if GRIDHEIGHT + 1 == self.y + dy:
    #              screen_there_y = True
    #         while screen_there_x and screen_there_y == True:
    #             return True
    #     return False

    def house_collide(self, dx = 0, dy = 0):
        """makes the wall solid and doesnt let player pass through"""
        wall_there_x = False
        wall_there_y = False
        for wall in self.game.walls:
            for n in (0, 2, 1): 
                if wall.x + n == self.x + dx:
                    wall_there_x = True
            for m in (0, 3, 1):
                if wall.y + m  == self.y + dy:
                    wall_there_y = True
            while wall_there_x and wall_there_y == True:
                return True
        return False


    def update(self, x = 0, y = 0):
        """updates the player's position"""
        self.smooth_movement()
        if not self.house_collide(x,y):
            self.x += self.vx * self.game.dt
            self.y += self.vy * self.game.dt
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


class Game:
    """Game class"""
    def __init__(self):
        """creates screen"""
        pygame.init()
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

    def run(self):
        """game loop"""
        self.playing = True
        key = pygame.key.get_pressed()

        # mainmenu = pygame.image.load("src/img/mainmenu.png") 
        # screen.blit(mainmenu,(0,0))
        # pygame.display.flip()
        # pygame.display.update()
        # clock.tick(FPS)
    
        if key[pygame.K_LEFT]:
            self.playing == True
            self.screenimage = pygame.image.load("src/img/grass2.png")
            self.rect = self.screenimage.get_rect()
            screen.blit(self.screenimage, self.rect)

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

# def main_menu():
     
#     menu=True
#     selected="start"
 
#     while menu:
#         for event in pygame.event.get():
#             if event.type==pygame.QUIT:
#                 pygame.quit()
#                 quit()
#             if event.type==pygame.KEYDOWN:
#                 if event.key==pygame.K_UP:
#                     selected="start"
#                 elif event.key==pygame.K_DOWN:
#                     selected="quit"
#                 if event.key==pygame.K_RETURN:
#                     if selected=="start":
#                         print("Start")
#                     if selected=="quit":
#                         pygame.quit()
#                         quit()
 
        
#         # main menu background image
#         mainmenu = pygame.image.load("src/img/mainmenu.png") 
#         screen.blit(mainmenu,(0,0))
#         pygame.display.flip()

#         title=text_format("Animal Crossing", font, 90, BLACK)
#         if selected=="start":
#             text_start=text_format("start!", font, 75, WHITE)
#         else:
#             text_start = text_format("start!", font, 75, WHITE)
#         if selected=="quit":
#             text_quit=text_format("quit...", font, 75, RED)
#         else:
#             text_quit = text_format("quit...", font, 75, RED)
 
#         title_rect=title.get_rect()
#         start_rect=text_start.get_rect()
#         quit_rect=text_quit.get_rect()
 
#         # Main Menu Text
#         screen.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
#         screen.blit(text_start, (WIDTH/2 - (start_rect[2]/2), 300))
#         screen.blit(text_quit, (WIDTH/2 - (quit_rect[2]/2), 360))
#         pygame.display.update()
#         clock.tick(FPS)
#         pygame.display.set_caption("main menu")

#         key = pygame.key.get_pressed()


#         if key[pygame.K_LEFT]:
#             break

        


# create the game object
g = Game() # abbreviation for game class

g.show_start_screen()


while True: 
    g.new()
    g.run()
    g.show_go_screen()