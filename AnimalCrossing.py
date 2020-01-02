#import sys and pygame
import sys
import pygame
#import pygame font
pygame.font.init()
# initialize pygame
pygame.init()

# setting the width & height of the screen and the movement speed
width = 1024   
height = 768  
FPS = 60

#size of each tile
tile_size = 32
#dimensions of the grid according to the size of the tiles
gridwidth = width / tile_size
gridheight = height / tile_size

 # make screen 
# screen = pygame.display.set_mode( (900,900) )

# # make color for screen
# white = pygame.Color(0,0,0)

# # Create a font object
# font = pygame.font.SysFont("Arial", 50)
# # Create text using the font
# text = font.render("Hello", True, (200,0,255))

# # fill the screen with color
# screen.fill( white )
# # draw text to screen
# screen.blit(text, (20, 20) )
# # update the display
# pygame.display.flip()

