# coding: utf-8
import os, pygame
import sys
import time
from pygame.locals import *
import random
from math import *
import colorsys
from PIL import Image
import numpy

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
        self.resLevels = int(log(min(self.PILimage.size[0], self.PILimage.size[1]), 3)) #ta reda på hur många gånger ett övre medelvärde skall sökas
        # print self.resLevels
        self.resolver = [[[[0.0,0.0,0.0] for y in range(self.PILimage.size[1])] for x in range(self.PILimage.size[0])] for level in range(self.resLevels)]
        # print len(self.resolver)
        # crop = self.PILimage.crop((0,0,2,2))
        
        # self.resolver[0][0].append((120,12,14))
        # print self.resolver[0][0]
        # a= [  [ [1,2,3] , [4,5,6] ] , [ [7,8,9] , [10,11,12] ]  ]
        # print a
        # print log(27,3)
        # a = numpy.mean(a, axis=0)
        # print a
        # print numpy.mean(crop, axis=1, keepdims=True), "1"
        # print numpy.mean(crop, axis=2), "2"
        # self.resolver[col,row,res] = self.data[int(floor(col/2.0)),int(floor(row/2.0))]

    def update(self):
        return

    def setLow(self):
        self.image = pygame.image.frombuffer(self.PILimage.tostring(), self.PILimage.size, 'RGB') # frombuffer returnerar en surface
        self.rect = self.image.get_rect()

    def setLevel(self, level):
        self.image = pygame.image.frombuffer(self.upPILimage.tostring(), self.upPILimage.size, 'RGB') # frombuffer returnerar en surface
        self.rect = self.image.get_rect() #måste finnas en rect annars klagar pygame

    def gatherData(self):
        print "gathering..."
        row = 0
        while row < self.PILimage.size[1]: #en rad i taget
            col = 0
            while col < self.PILimage.size[0]: # här sker varje pixel
                cropsize = 3
                level = 0
                while level < self.resLevels:
                    csize = (cropsize-1)/2
                    cropL = max(0, col-csize)
                    cropT = max(0, row-csize)
                    cropR = min(self.PILimage.size[0], col+csize)
                    cropB = min(self.PILimage.size[1], row+csize)
                    crop = self.PILimage.crop((cropL, cropT, cropR, cropB))
                    meanA = numpy.mean(crop, axis=0)
                    meanB = numpy.mean(meanA, axis=0)
                    meanList = list(meanB)
                    # self.resolver[col][row][level] = list(numpy.mean(numpy.mean(crop, axis=0), axis=0))
                    self.resolver[level][col][row] = meanList
                    cropsize *= 3
                    level += 1
                col += 1
            row += 1
        print self.resolver[0][0][0]
        # print min(self.PILimage.size[0], self.PILimage.size[1])
        # print log(3, 200)
        print "done"

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

    plot.gatherData()
    # allsprites.draw(screen)
    # pygame.display.flip()
    # plot.upsample()
    # plot.setHi()
    # allsprites.draw(screen)
    # pygame.display.flip()    

    

    #mainloop
    going=False
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