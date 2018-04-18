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

def randx(x):
    random.seed(x)
    return random.random()

class Plot(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.width = width
        self.height = height
        self.size = (width, height)
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        self.PILimage = Image.new('RGB', self.size)

    def set(self, x, y, value):
        if x < 0: x=0
        if x > self.width-1: x=self.width-1
        if y < 0: y=0
        if y > self.height-1: y=self.height-1
        x = int(round(x))
        y = int(round(y))
        pos = (y*self.width)+x
        self.data[pos]=value

    def get(self, x, y):
        return self.data[y][x]
        
    def update(self):
        self.image = pygame.image.frombuffer(self.PILimage.tostring(), self.size, 'RGB') # frombuffer returnerar en surface
        # self.PILimage.putdata(self.data, 1, 0)
        # self.PILimage = self.PILimage.convert('RGB')
        # imgstr=self.PILimage.tostring()
        # self.image=pygame.image.frombuffer(imgstr, self.size, 'RGB')

class Lengths():
    def __init__(self, meanlength):
        self.data = dict()
        self.shift = 1 - 1.0/meanlength

    def get(self, pos):
        pos = int(pos)
        if pos in self.data: return self.data[pos]
        else:
            origin=pos
            while randx(pos-1) < self.shift:
                pos -= 1
            first = pos
            pos = origin
            while randx(pos) < self.shift:
                pos += 1
            last = pos
            setval = randx(pos+1)
            for a in range(first, last+1):
                self.data[a]=setval
            return setval

def main():

    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)
    # screen.fill ((100, 100, 100))
    pic1 = load_image('test.jpg')
    screen = pygame.display.set_mode(pic1.get_size(), 0, 32)

    #background = pygame.Surface(screensize)
    #background = background.convert()
    #background=load_image('2x2.png')
    #screen.blit(background, (0, 0))
    pygame.display.flip()
    
    plot = Plot(pic1.get_width(), pic1.get_height())
    plot.image = pic1
    allsprites = pygame.sprite.Group(plot)

    # def triwave(x):
    #     return max(1-abs(x*2%2-1), 0)
    # def sqrwave(x):
    #     return int(x%1+0.5)
    # def sinwave(x):
    #     return sin(x*pi*2)*0.5+0.5
    # def sawwave(x):
    #     return (x % 1)
    # def bllwave(x):
    #     return sin(acos(x*2%2-1))
    # def topwave(x):
    #     return 1-sin(acos((x*2+1)%2-1))
    # def logset(x, base, firstrange):
    #     return int(log((x*((base-1.0)/firstrange)+1), base))

    
    # for y in range(400):
    #     plot.set(25,y,200)
    #     plot.set(25*4,y,200)
    #     plot.set(25*13,y,200)
        
    # for x in range(400):
    #     x=float(x)
    #     p=50.0
    #     plot.set(x, 15 - sawwave(x/p)*10, 0)
    #     plot.set(x, 30 - sinwave(x/p)*10, 0)
    #     plot.set(x, 50 - sqrwave(x/p)*10,0)
    #     plot.set(x, 70 - triwave(x/p)*10, 0)
    #     plot.set(x, 100 - bllwave(x/p)*25, 0)
    #     plot.set(x, 125 - topwave(x/p)*25, 0)
    #     plot.set(x, 400 - logset(x, 3, 25)*10, 0)
    #     plot.set(x, 225 - lengths.get(x)*90, 0)

    
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