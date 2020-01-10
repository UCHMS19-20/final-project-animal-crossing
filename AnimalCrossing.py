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
FPS = 60
TITLE = "Animal Crossing"
TILESIZE = 48
# sizes of the grids
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

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
        self.x = x
        self.y = y
        
        
    def move(self, dx=0, dy=0):
        """ moves the player"""
        if not self.house_collide(dx,dy):
            self.x += dx
            self.y += dy

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

    def update(self):
        """updates the player's position"""
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class House(pygame.sprite.Sprite): 
    def __init__(self, game, x, y):
        """makes the wall that shows up on the screen"""
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load("src/img/townhall.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        pass

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.player = Player(self, 10, 10)
        for x in range(10, 20):
            House(self, 5, 3)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, GREEN, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, GREEN, (0, y), (WIDTH, y))

    def draw(self):
        # draw the grid
        self.draw_grid()
        # draw the background grass
        self.screenimage = pygame.image.load("src/img/grass.png")
        self.rect = self.screenimage.get_rect()
        screen.blit(self.screenimage, self.rect)
        # draw sprites
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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