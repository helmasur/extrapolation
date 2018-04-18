import os, pygame
import sys
import time
from pygame.locals import *
import random
from math import *
import colorsys
from PIL import Image

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

def load_image(filename):
    fullpath = os.path.join(data_dir, filename)
    try:
        image = pygame.image.load(fullpath) #image.load returnerar en surface
    except pygame.error:
        print ('Cannot load image:', fullpath)
        raise SystemExit(str(geterror()))
    image = image.convert()
    return image

class Plot(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.PILimage = Image.open(filename)
        self.image = pygame.Surface(self.PILimage.size)
        self.rect = self.image.get_rect()

    def update(self):
        self.image = pygame.image.frombuffer(self.PILimage.tostring(), self.PILimage.size, 'RGB') # frombuffer returnerar en surface

def main():

    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)
    
    plot = Plot("data/test.jpg")

    allsprites = pygame.sprite.Group(plot)

    #mainloop
    going=True
    while going:

        #Handle Input Events
        for event in pygame.event.get():        
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
    
        allsprites.update()
        allsprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()