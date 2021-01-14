import pygame, sys, random
from pygame.locals import *

class Game:
    pygame.init()
    pygame.display.set_caption("Flappy Bird")

    def __init__(self):
        self.WIDTH = 288
        self.HEIGHT = 512
        self.framerate = 60
        self.bird = Bird(self)
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.pipes = [Pipe(self,self.WIDTH*1.25),Pipe(self,self.WIDTH*1.25+160)]
        self.load_images()

    def mainLoop(self):
        while True:
            self.update()
            self.draw()
            pygame.display.update()

            self.inputManage()

            self.clock.tick(self.framerate)
    
    def update(self):
        #animate bacground
        if self.background_rect.right > 0:
            self.background_rect.left -= 1
        else:
            self.background_rect.left = 0
        #animate ground
        if self.ground_rect.right > 0:
            self.ground_rect.left -= 1
        else:
            self.ground_rect.left = 0
        #update game objects
        self.bird.update()
        for pipe in self.pipes:
            pipe.update()

    def inputManage(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.bird.isJumping == True:
                        self.bird.j_speed = 18
                    else:
                        self.bird.isJumping = True
                    #every jump reset gravity power and angle
                    self.bird.angle = 15
                    self.bird.gravity = 5
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.bird.isJumping == True:
                        self.bird.j_speed = 18
                    else:
                        self.bird.isJumping = True
                    #every jump reset gravity power and angle
                    self.bird.angle = 15
                    self.bird.gravity = 5
                    
    def draw(self):
        #draw background and other one on right side so when original moves left we sill see background
        self.window.blit(self.background, self.background_rect.topleft)
        self.window.blit(self.background, self.background_rect.topright)
        #draw pipes
        for pipe in self.pipes:
            self.window.blit(pipe.upperPipe,pipe.upperPipe_rect.topleft)
            self.window.blit(pipe.bottomPipe,pipe.bottomPipe_rect.topleft)
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
        self.gravity = 5
        self.loadImages()
        self.tick = 0
        self.j_speed = 18
        self.angle = 15
        self.frames_for_image = self.game.framerate // len(self.images)
        self.isJumping = False
        
    def update(self):
        if self.isJumping:
            self.jump()
        else:
            self.useGravity()
        #animating bird
        self.animate()
        #make rotation
        self.rotate()
        
    def animate(self):
        #select image to draw based on framerate, we have 4 images to draw in 1 second
        if self.tick == self.game.framerate or self.angle < -80:
            self.tick = 0
        
        self.image = self.images[self.tick//self.frames_for_image]
        self.tick += 1
        
    def rotate(self):
        #rotate image
        rot_image = pygame.transform.rotate(self.image,self.angle)
        rot_image_rect = rot_image.get_rect()
        rot_image_rect.center = self.rect.center
        #save it
        self.image = rot_image
        self.rect = rot_image_rect
        #change angle
        if self.angle > -90:
            self.angle -= 1*(self.gravity-4)
   
    def useGravity(self):
        #using gravity on the bird
        self.rect.bottom += self.gravity
        #going faster in time
        self.gravity *= 1.04

    def jump(self):
        self.rect.y -= self.j_speed*0.3
        self.j_speed -= 1
        if self.j_speed == -19:
            self.isJumping = False
            self.j_speed = 18
        
    def loadImages(self):
        #4 frames to animate
        self.images = [pygame.image.load("sprites\\yellowbird-downflap.png"),
                       pygame.image.load("sprites\\yellowbird-midflap.png"),
                       pygame.image.load("sprites\\yellowbird-upflap.png"),
                       pygame.image.load("sprites\\yellowbird-midflap.png")]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (40,200)

class Pipe():
    
    def __init__(self,game,pipeleft):
        self.game = game
        self.load_images()
        self.generatePipes(pipeleft)
        self.speed = 1
    
    def update(self):
        if self.upperPipe_rect.right > 0:
            self.upperPipe_rect.left -= 1
            self.bottomPipe_rect.left -= 1
        else:
            self.generatePipes(288)
    
    def generatePipes(self, pipeleft):
        self.upperPipe_rect.bottom = random.randint(self.game.HEIGHT//5,(self.game.HEIGHT//5)*3)
        self.upperPipe_rect.left = pipeleft
        self.bottomPipe_rect.top = self.upperPipe_rect.bottom+100
        self.bottomPipe_rect.left = pipeleft
    
    def load_images(self):
        #load bottom pipe
        self.bottomPipe = pygame.image.load("sprites\pipe-green.png")
        self.bottomPipe_rect = self.bottomPipe.get_rect()
        
        #make flipped
        self.upperPipe = pygame.transform.flip(self.bottomPipe,False,True)
        self.upperPipe_rect = self.upperPipe.get_rect()
        
if __name__ == "__main__":
    game = Game()
    game.mainLoop()