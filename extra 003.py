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
        self.upPILimage = Image.new('RGB', (self.PILimage.size[0]*2, self.PILimage.size[1]*2))
        self.data = self.PILimage.load() #skapar ett arrayliknande objekt för snabba pixelmodifikationer typ "pix[x, y] = value"
        self.updata = self.upPILimage.load()
        self.image = pygame.Surface(self.PILimage.size) #förbereder en pygame image surface för visning i fönster, den fylls med data i update
        self.rect = self.image.get_rect() #måste finnas en rect annars klagar pygame


    def update(self):
        return

    def setLow(self):
        self.image = pygame.image.frombuffer(self.PILimage.tostring(), self.PILimage.size, 'RGB') # frombuffer returnerar en surface
        self.rect = self.image.get_rect()

    def setHi(self):
        self.image = pygame.image.frombuffer(self.upPILimage.tostring(), self.upPILimage.size, 'RGB') # frombuffer returnerar en surface
        self.rect = self.image.get_rect() #måste finnas en rect annars klagar pygame

    def upsample(self):
        row = 0
        while row < self.upPILimage.size[1]: #en rad i taget
            col = 0
            while col < self.upPILimage.size[0]: #en kolumn i taget
                self.updata[col,row] = self.data[int(floor(col/2.0)),int(floor(row/2.0))]
                col += 1
            row += 1
        print "done"

def main():

    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)
    
    plot = Plot("data/test.jpg") #ladda en bild

    allsprites = pygame.sprite.Group(plot) #lägger till spriten 'plot' i gruppen allsprites

    plot.setLow()
    allsprites.draw(screen)
    pygame.display.flip()
    plot.upsample()
    plot.setHi()
    allsprites.draw(screen)
    pygame.display.flip()    

    

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