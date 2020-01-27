# import pygame
import pygame 
import sys
# operating system: i just need this so i can center the screen
import os
# import stuff like event/key/display
from pygame.locals import *

# center screen 
os.environ['SDL_VIDEO_CENTERED'] = '1'

#initialize pygame
pygame.init()

# predefine some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 225, 0)

# setting the parameters for the screen
WIDTH = 1056                                                            
HEIGHT = 624

# measurement (in pixels) of individual tiles height/width
TILESIZE = 48
# sizes of the grids in tiles
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE


# caption
TITLE = "Animal Crossing"

#player speed settings
PLAYER_SPEED = {'x': 0, 'y': 0}

# default font (official animal crossing font)
font_name = 'src/humming_otf.otf'

# create an object to detect key presses
key = pygame.key.get_pressed()

# display screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# create an object to help track time
clock = pygame.time.Clock()
#framerate
FPS = 30

# list to store the fruit that you've collected
collected_fruit = []

class Player(pygame.sprite.Sprite): 
    """this is what the user is going to be moving around on the screen"""
    def __init__(self, game, x, y): 
        """creates the icon that the player can move around on the grid"""

        #this is part of the sprites group
        self.groups = game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)

        #part of the games group
        self.game = game

        #image of the Player
        self.image = pygame.image.load("src/img/villager.png")
        self.rect = self.image.get_rect()
        screen.blit(self.image, self.rect)

        # x position of the player in terms of the grid
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        # velocity of the player
        self.vx, self.vy = 0, 0


    def smooth_movement(self):
        """allows player to move smoothly"""

        # object for key presses
        key = pygame.key.get_pressed()



       # how much the velocity of the player changes while the key is pressed
        if key[pygame.K_LEFT]:
            self.vx -= 18
        elif key[pygame.K_RIGHT]:
            self.vx += 18
        if key[pygame.K_UP]:
            self.vy -= 18
        elif key[pygame.K_DOWN]:
            self.vy += 18


        # friction x direction
        if self.vx > 12:
            self.vx -= 12
        elif self.vx >= -12:
            self.vx = 0
        else:
            self.vx += 12
        # friction y direction
        if self.vy > 12:
            self.vy -= 12
        elif self.vy >= -12:
            self.vy = 0
        else:
            self.vy += 12



    def update(self, x = 0, y = 0):
        """updates the player's position"""
        # makes sure the player till moves smoothly
        self.smooth_movement()

        # new x and y positions
        new_x = self.x + self.vx * self.game.dt
        if 0 < new_x < 1008: # these are bounds of the screen
            self.x = new_x
        
        new_y = self.y + self.vy * self.game.dt
        if 0 < new_y < 576: # these are bounds of the screen
            self.y = new_y
        
        #check for collision
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

        
    def collide_with_walls(self, direction):
        if direction == 'x':
            #sprite collide function
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                # if Player hits wall, player cannot move.
                self.vx = 0
                self.rect.x = self.x
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                # if Player hits wall, player cannot move.
                self.vy = 0
                self.rect.y = self.y



class Apple(pygame.sprite.Sprite): 
    """just a lil fruity boi (apple)"""
    def __init__(self, game, x, y):
        """Just a fruit on the screen that the player can pick up"""
        # everything is the same as the Player class except it is also in the walls group
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load("src/img/apple.png")
        self.rect = self.image.get_rect()

        self.hit_rect = pygame.Rect(0, 0, 48, 48)
        self.hit_rect.center = self.rect.center

        self.x = x
        self.y = y

        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Orange(pygame.sprite.Sprite): 
    """just a lil fruity boi (orange)"""
    def __init__(self, game, x, y):
        """Just a fruit on the screen that the player can pick up"""
        # everything is the same as the Player class except it is also in the walls group
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load("src/img/orange.png")
        self.rect = self.image.get_rect()

        self.hit_rect = pygame.Rect(0, 0, 48, 48)
        self.hit_rect.center = self.rect.center

        self.x = x
        self.y = y

        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Peach(pygame.sprite.Sprite): 
    """just a lil fruity boi (peach)"""
    def __init__(self, game, x, y):
        """Just a fruit on the screen that the player can pick up"""
        # everything is the same as the Player class except it is also in the walls group
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load("src/img/peach.png")
        self.rect = self.image.get_rect()

        self.hit_rect = pygame.Rect(0, 0, 48, 48)
        self.hit_rect.center = self.rect.center

        self.x = x
        self.y = y

        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Pear(pygame.sprite.Sprite): 
    """just a lil fruity boi (pear)"""
    def __init__(self, game, x, y):
        """Just a fruit on the screen that the player can pick up"""
        # everything is the same as the Player class except it is also in the walls group
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load("src/img/pear.png")
        self.rect = self.image.get_rect()

        self.hit_rect = pygame.Rect(0, 0, 48, 48)
        self.hit_rect.center = self.rect.center

        self.x = x
        self.y = y

        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE



class Tree1(pygame.sprite.Sprite):
    """Just a tree"""
    def __init__(self, game, x, y):
        """The player cant do anything to this other than not go thru it"""
        # exact same stuff as all the fruit classes
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
    """NPC that the player can talk to"""
    def __init__(self, game, x, y):
        """makes Isabelle (Ms. Gerstein)"""
        # same stuff as fruit class
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pygame.image.load("src/img/isabelle.png")
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Game():
    """all the main functions for the actual game"""
    def __init__(self):
        """creates screen and window"""
        
        #screen and window creation
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        # clock object
        self.clock = pygame.time.Clock()
    

    def new(self):
        """stores groups and places all the sprites on the grid"""

        # where the groups are stored
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        
        # the numbers are the coordinates by tile, not pixel (so position divided by 48)
        # the coordinates go from the top left corner of the image

        #isabelle position
        Isabelle(self, 6, 5)

    
        #tree  positions
        Tree1(self, 2, 11)
        Tree1(self, 13, 8)
        Tree1(self, 20, 8)
        Tree1(self, 4, 9)
        Tree1(self, 15, 10)
        Tree1(self, 2, 3)
        Tree1(self, 3, 7)
        Tree1(self, 19, 1)
        Tree1(self, 6, 1)
        

        # fruit positions
        Apple(self, 6, 10 )
        Orange(self, 18, 4)
        Peach(self, 2, 2)
        Pear(self, 17, 10)

        # player position
        self.player = Player(self, 21, 6)

    def run(self):
        """game loop"""
        self.playing = True

        # introductory stuff not inside the main loop
        main_menu()
        name() 
        instructions()


        # main loop
        while self.playing == True:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            
        
    def quit(self):
        """quits the game"""
        pygame.quit()
        sys.exit()

    def update(self):
        """updates portion of the game loop"""
        # update all sprites
        self.all_sprites.update()
        
    def draw_grid(self):
        """draws the grid"""
        # i only used this for reference when i was choosing where to place the trees and stuff.
        # the whole grid is covered up by the background of the actual game.
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, GREEN, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, GREEN, (0, y), (WIDTH, y))

    def collect_fruit(self):
        """appends/deletes fruit from a list"""

        # what is supposed to cover the fruit once it has been collected
        #basically just a grass colored square
        patch = pygame.image.load("src/img/patch.png") 

        # can only hold one fruit at a time
        # makes sure the player actually went and got the fruit before giving it to the teacher
        if len(collected_fruit) < 1:
            if pygame.key.get_pressed()[pygame.K_a]: 
                screen.blit(patch, (288, 480))
                pygame.display.flip()
                collected_fruit.append("apple")
                print(collected_fruit)
            if pygame.key.get_pressed()[pygame.K_o]: 
                screen.blit(patch, (288, 480))
                pygame.display.flip()
                collected_fruit.append("orange")
                print(collected_fruit)
            if pygame.key.get_pressed()[pygame.K_p]: 
                screen.blit(patch, (288, 480))
                pygame.display.flip()
                collected_fruit.append("peach")
                print(collected_fruit)
            if pygame.key.get_pressed()[pygame.K_r]: 
                screen.blit(patch, (288, 480))
                pygame.display.flip()
                collected_fruit.append("pear")
                print(collected_fruit)

        # when they deliver the fruit, the fruit is deleted from the list 
        # clears space for the next fruit
        elif len(collected_fruit) == 1:
            if pygame.key.get_pressed()[pygame.K_1]:    
                collected_fruit.remove("apple")
                print(collected_fruit)
            if pygame.key.get_pressed()[pygame.K_2]: 
                collected_fruit.remove("orange")
                print(collected_fruit)
            if pygame.key.get_pressed()[pygame.K_3]: 
                collected_fruit.remove("peach")
                print(collected_fruit)
            if pygame.key.get_pressed()[pygame.K_4]: 
                collected_fruit.remove("pear")
                print(collected_fruit)

    def Isabelle_talk(self):
        """all the actual dialogue so far"""
        # the user inputted their name
        global name

        #initialize font
        font = pygame.font.Font(font_name, 15)

        # format for all the dialogues: 
            # check for key press
            # define all the variables first: images & text.
            # blit everything onto the screen
        
        if pygame.key.get_pressed()[pygame.K_t]: 
            box = pygame.image.load("src/img/smaller_box.png")
            block1 = font.render("Mrs. Gerstein", True, WHITE)
            block2 = font.render(f"Hello {name}! Welcome to Magnet!", True, WHITE)
            block3 = font.render("I'm Mrs. Gerstein. Perhaps we've met before?", True, WHITE)
            block4 = font.render("Anyway, what brings you here today?", True, WHITE)
            block5 = font.render("Next > Press Y", True, BLACK)
            
            screen.blit(box, (384, 0))
            screen.blit(block1, (425, 18))
            screen.blit(block2, (450, 50))
            screen.blit(block3, (450, 80))
            screen.blit(block4, (450, 110))
            screen.blit(block5, (500, 150))

        
        if pygame.key.get_pressed()[pygame.K_y]: 
            box = pygame.image.load("src/img/smaller_box.png")
            block1 = font.render("Mrs. Gerstein", True, WHITE)
            block2 = font.render("What? You want to know how to become", True, WHITE)
            block3 = font.render("valedictorian? Well, you need to be a well ", True, WHITE)
            block4 = font.render("rounded student... Why don't we start off by", True, WHITE)
            block5 = font.render("looking at your grades?", True, WHITE)
            block6 = font.render("Next > Press U", True, BLACK)

            screen.blit(box, (384, 0))
            screen.blit(block1, (425, 18))
            screen.blit(block2, (450, 50))
            screen.blit(block3, (450, 80))
            screen.blit(block4, (450, 110))
            screen.blit(block5, (450, 140))
            screen.blit(block6, (550, 160))

        if pygame.key.get_pressed()[pygame.K_u]: 
            card = pygame.image.load("src/img/report_card_original.png")
            block = font.render("Next > Press G", True, BLACK)
            
            screen.blit(card, (384, 0))
            screen.blit(block, (741, 460))

        if pygame.key.get_pressed()[pygame.K_g]: 
            box = pygame.image.load("src/img/smaller_box.png")
            block1 = font.render("Mrs. Gerstein", True, WHITE)
            block2 = font.render("Okay...so...", True, WHITE)
            block3 = font.render(f"*How did you even do that, {name}?...*", True, WHITE)
            block4 = font.render("Well, why don't you start off by asking", True, WHITE)
            block5 = font.render("your teachers how to raise your grade?", True, WHITE)
            block6 = font.render("Next > Press H", True, BLACK)

            screen.blit(box, (384, 0)) 
            screen.blit(block1, (425, 18))
            screen.blit(block2, (450, 50))
            screen.blit(block3, (450, 80))
            screen.blit(block4, (450, 110))
            screen.blit(block5, (450, 140))
            screen.blit(block6, (550, 160))
        
        if pygame.key.get_pressed()[pygame.K_h]: 
            card = pygame.image.load("src/img/report_card_arnold_rq.png")
            block = font.render("Next > Press J", True, BLACK)
            
            screen.blit(card, (384, 0))
            screen.blit(block, (741, 460))
        
        if pygame.key.get_pressed()[pygame.K_j]: 
            box = pygame.image.load("src/img/smaller_box.png")
            block1 = font.render("Mrs. Gerstein", True, WHITE)
            block2 = font.render("...Well, that's a first.", True, WHITE)
            block3 = font.render("Guess you gotta get Ms. Arnold an apple, then!", True, WHITE)
            block4 = font.render("I see one by the tree over there...", True, WHITE)
            block5 = font.render("Go run over and pick it up by pressing A!", True, WHITE)
            block6 = font.render("When you come back > Press V", True, BLACK)


            screen.blit(box, (384, 0)) 
            screen.blit(block1, (425, 18))
            screen.blit(block2, (450, 50))
            screen.blit(block3, (440, 80))
            screen.blit(block4, (450, 110))
            screen.blit(block5, (450, 140))
            screen.blit(block6, (530, 160))
        
        if pygame.key.get_pressed()[pygame.K_v]: 
            if "apple" in collected_fruit:
                box = pygame.image.load("src/img/smaller_box.png")
                block1 = font.render("Mrs. Gerstein", True, WHITE)
                block2 = font.render(f"Great job {name}!", True, WHITE)
                block3 = font.render("Why don't you give it to Ms. Arnold now?", True, WHITE)
                block4 = font.render("Press 1 to give it to her and then press B", True, WHITE)
                block5 = font.render("to check your grade...Hopefully it's improved...", True, WHITE)


                screen.blit(box, (384, 0)) 
                screen.blit(block1, (425, 18))
                screen.blit(block2, (450, 50))
                screen.blit(block3, (450, 80))
                screen.blit(block4, (450, 110))
                screen.blit(block5, (450, 140))

        if pygame.key.get_pressed()[pygame.K_b]: 
            if len(collected_fruit) == 0:
                card = pygame.image.load("src/img/report_card_arnold_a.png")
                block = font.render("Next > Press N", True, BLACK)
            
                screen.blit(card, (384, 0))
                screen.blit(block, (741, 460))
        
        if pygame.key.get_pressed()[pygame.K_n]: 
            box = pygame.image.load("src/img/smaller_box.png")
            block1 = font.render("Mrs. Gerstein", True, WHITE)
            block2 = font.render(f"Whoohoo {name}!", True, WHITE)
            block3 = font.render("You're one A closer to being valedictorian!", True, WHITE)
            block4 = font.render("Next, let's check on Mr. Sanservino.", True, WHITE)
            block5 = font.render("I wonder what type of fruit he'll want!", True, WHITE)


            screen.blit(box, (384, 0)) 
            screen.blit(block1, (425, 18))
            screen.blit(block2, (450, 50))
            screen.blit(block3, (450, 80))
            screen.blit(block4, (450, 110))
            screen.blit(block5, (450, 140))


    def draw(self):
        """draws everything onto the screen"""

        # draw the grid 
        self.draw_grid()

        # draw the background grass
        self.screenimage = pygame.image.load("src/img/grass2.png")
        self.rect = self.screenimage.get_rect()
        screen.blit(self.screenimage, self.rect)
    

        # draw sprites
        self.all_sprites.draw(self.screen)
        
        # dialogue
        self.Isabelle_talk()
        
        # fruit collection function
        self.collect_fruit()

        # flip everything once at the very end
        pygame.display.flip()
                    
 
    def events(self):
        """all events"""
        # i don't use this much, just to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

def main_menu():
    """starting screen of the game"""

    menu = True
    selected = "start"
 
    while menu: # while loop to display image until player exits
        #check for key presses
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
                        # confirm the players selection
                        print("Start")
                    if selected=="quit":
                        pygame.quit()
                        quit()
 
        
        # main menu background image
        mainmenu = pygame.image.load("src/img/titleimage.png") 
        screen.blit(mainmenu,(0,0))
        # window caption
        pygame.display.set_caption("main menu")
        pygame.display.flip()

        key = pygame.key.get_pressed()
        # if they press s, the game goes on
        if key[pygame.K_s]:
            break
        # if they press esc, the game quits
        elif key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()


def name():
    """where the player enters their name"""
    global name # for use in the dialogue function
    # empty string for storing letters
    name = "" 
    # initialize font
    font_name = 'src/humming_otf.otf'
    font = pygame.font.Font(font_name, 50)

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.unicode.isalpha(): #check if its in the alphabet
                    name += event.unicode # add to name string
                elif event.key == K_BACKSPACE: # backspace deletes the last letter
                    name = name[:-1]

            elif event.type == QUIT:
                return
        
        # background image
        mainmenu = pygame.image.load("src/img/nameentry.png") 
        screen.blit(mainmenu,(0,0))
        # rect for the text to go inside
        block = font.render(name, True, (254, 192, 30))
        rect = block.get_rect()
        rect.center = screen.get_rect().center # center the rect on the screen
        screen.blit(block, rect)
        
        pygame.display.flip()

        key = pygame.key.get_pressed()
        # if they press return, the game continues
        if key[pygame.K_RETURN]:
            break


def instructions():
    """introductory instructions for the player"""
    speak = True
    selected = "yes"
 
    # check for key press
    while speak:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="yes"
                if event.key==pygame.K_RETURN:
                    if selected=="yes":
                        print("Start")
                    
                    
        key = pygame.key.get_pressed()

        # dialogue box
        box = pygame.image.load("src/img/box.png") 
        screen.blit(box,(6,1))
        # window caption
        pygame.display.set_caption("instructions")
        
        # define font
        font = pygame.font.Font(font_name, 30)

        # all of the text for the instructions
        block = font.render("Instructions", True, WHITE)
        screen.blit(block, (120, 35))

        block = font.render("Move with ARROW KEYS", True, WHITE)
        screen.blit(block, (150,110))

        block = font.render("Your first task: Find and talk to Mrs. Gerstein!", True, WHITE)
        screen.blit(block, (150,155))

        block = font.render("Talk to her by holding T", True, WHITE)
        screen.blit(block, (150,200))

        block = font.render("Get rid of these instructions by", True, WHITE)
        screen.blit(block, (150,245))

        block = font.render("pressing BACKSPACE", True, WHITE)
        screen.blit(block, (150,290))

        pygame.display.flip()

        # if backspace is pressed, the game continues
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]: 
            break



# create the game object
g = Game() # abbreviation for game class

#main main loop: basically runs the whole game
while True: 
    g.new()
    g.run()
    
# good job you've reached the end! my butt hurts and my fingers ache from sitting and typing for so long. i hope you enjoyed reading all this code!
    