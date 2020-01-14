import pygame 
import sys

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


pygame.mixer.init()
pygame.mixer.music.load("src/3pm.mp3")
pygame.mixer.music.play(-1,0.0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Player(pygame.sprite.Sprite): # player that can be moved by keys
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

        # straight line mov ement
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

    # def house_collide(self, dx = 0, dy = 0):
    #     """makes the wall solid and doesnt let player pass through"""
    #     wall_there_x = False
    #     wall_there_y = False
    #     for wall in self.game.walls:
    #         for n in (0, 2, 1): 
    #             if wall.x + n == self.x + dx:
    #                 wall_there_x = True
    #         for m in (0, 3, 1):
    #             if wall.y + m  == self.y + dy:
    #                 wall_there_y = True
    #         while wall_there_x and wall_there_y == True:
    #             return True
    #     return False


    def update(self):
        """updates the player's position"""
        self.smooth_movement()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y

# seperate classes for town hall and houses/trees bc town hall is 2x3 squares and trees/houses are 2x2 squares
class Hall(pygame.sprite.Sprite): 
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
        while self.playing:
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

        # #draw the grid
        # self.draw_grid()

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
                # if event.key == pygame.K_LEFT:
                #     self.player.move(dx=-1)
                # if event.key == pygame.K_RIGHT:
                #     self.player.move(dx=1)
                # if event.key == pygame.K_UP:
                #     self.player.move(dy=-1)
                # if event.key == pygame.K_DOWN:
                #     self.player.move(dy=1)

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()