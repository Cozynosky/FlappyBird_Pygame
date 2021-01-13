import pygame, sys
from pygame.locals import *

class Game:
    pygame.init()

    def __init__(self):
        self.WIDTH = 288
        self.HEIGHT = 512
        self.framerate = 60
        self.bird = Bird(self)
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.load_images()

    def mainLoop(self):
        while True:
            self.update()
            self.draw()
            pygame.display.update()

            self.inputManage()

            self.clock.tick(self.framerate)
    
    def update(self):
        if self.background_rect.right > 0:
            self.background_rect.left -= 2
        else:
            self.background_rect.left = 0
        if self.ground_rect.right > 0:
            self.ground_rect.left -= 1
        else:
            self.ground_rect.left = 0
        self.bird.update()

    def inputManage(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def draw(self):
        #draw background and other one on right side so when original moves left we sill see background
        self.window.blit(self.background, self.background_rect.topleft)
        self.window.blit(self.background, self.background_rect.topright)
        #the same with ground
        self.window.blit(self.ground,self.ground_rect.topleft)
        self.window.blit(self.ground,self.ground_rect.topright)
        #blit bird
        self.window.blit(self.bird.image,self.bird.rect.topleft)
    
    def load_images(self):
        #load background
        self.background = pygame.image.load("sprites\\background-day.png")
        self.background_rect = self.background.get_rect()
        #load ground and place it on the bottom
        self.ground = pygame.image.load("sprites\\base.png")
        self.ground_rect = self.ground.get_rect()
        self.ground_rect.bottom = self.background_rect.bottom
    
class Bird:
    def __init__(self,game):
        self.game = game
        self.loadImages()
        self.tick = 0
        self.frames_for_image = self.game.framerate // len(self.images)
        
    def update(self):
        #select image to draw based on framerate, we have 4 images to draw in 1 second
        if self.tick == self.game.framerate:
            self.tick = 0
        else:
            self.image = self.images[self.tick//self.frames_for_image]
            self.tick += 1

    def loadImages(self):
        #4 frames to animate
        self.images = [pygame.image.load("sprites\\yellowbird-downflap.png"),
                  pygame.image.load("sprites\\yellowbird-midflap.png"),
                  pygame.image.load("sprites\\yellowbird-upflap.png"),
                  pygame.image.load("sprites\\yellowbird-midflap.png")]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (10,200)

class Pipe:
    pass

if __name__ == "__main__":
    game = Game()
    game.mainLoop()