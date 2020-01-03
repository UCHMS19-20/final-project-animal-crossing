#import sys and pygame
import sys
import pygame
#initialize pygame
pygame.init()

#import pygame font
pygame.font.init()


# setting the WIDTH & HEIGHT of the screen and the movement speed
WIDTH = 1024   
HEIGHT = 768  
FPS = 60

#title of the game
TITLE = "Animal_Crossing"

#colors of stuff
BACKGROUND = (0, 0, 0)
GREY = (40, 40, 40)

#size of each tile
TILESIZE = 32
#how many squares are on the screen
GWIDTH = WIDTH / TILESIZE
GHEIGHT = HEIGHT / TILESIZE

#create player class
class Player(pygame.sprite.Sprite):
    """player Class"""
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface()
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
    # size of player based on tilesize 
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

#main loop and functions for the game
class game():
    """game class"""
    #display screen and title
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

    def load_data(self):
        pass

    # initialize all variables and do setup for a new game
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.player = Player(self, 10, 10)
        for x in range(10, 20):
            Wall(self, x, 5)

    #where the game loops; if self.playing == false, then the game ends
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.speed = FPS
            self.events()
            self.update()
            self.draw()

    # ends the game
    def quit(self):
        pygame.quit()
        sys.exit()

    #update sprites during the game
    def update(self):
        self.all_sprites.update()

    # draw the grids on the screen
    def draw_grid(self):
        for x in range (0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, GREY, (x, 0), (x, HEIGHT))
        for y in range (0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, GREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BACKGROUND)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    # allows the player to quit and move
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.quit:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pygame.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pygame.K_UP:
                    self.player.move(dy=-1)
                if event.key == pygame.K_DOWN:
                    self.player.move(dy=1)

    # shows start screen
    def show_start_screen(self):
        pass

    #shows go screen
    def show_go_screen(self):
        pass