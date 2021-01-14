import pygame, sys, random
from pygame.locals import *


class Game:
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Flappy Bird")

    def __init__(self):
        self.WIDTH = 288
        self.HEIGHT = 512
        self.gamestance = "MENU"
        self.framerate = 60
        self.tick = 0
        self.new_game()
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.load_images()
        self.load_sounds()

    def mainLoop(self):
        while True:

            if self.tick == self.framerate:
                self.tick = 0
            # if when we only see backgroudn and flappping bird
            if self.gamestance == "MENU":
                # self update
                self.update()
                self.bird.animate()
            # theres whe main game magic work
            if self.gamestance == "GAME":
                self.pipecollisionDetect()
                self.groundcollisionDetect()
                self.scoring()
                # update game objects
                self.update()
                self.bird.update()
                for pipe in self.pipes:
                    pipe.update()

            # when hit the pipe everything stops and bird fly down
            if self.gamestance == "PIPE_HIT":
                self.groundcollisionDetect()
                self.bird.update()

            self.inputManage()
            self.draw()
            self.tick += 1
            pygame.display.update()
            self.clock.tick(self.framerate)

    def new_game(self):
        self.score = 0
        self.bird = Bird(self)
        self.clock = pygame.time.Clock()
        self.pipes = [
            Pipe(self, self.WIDTH * 1.25),
            Pipe(self, self.WIDTH * 1.25 + 176),
        ]

    def scoring(self):
        for pipe in self.pipes:
            if self.bird.rect.left == pipe.bottomPipe_rect.centerx:
                self.score += 1
                self.point_sound.play()

    def update(self):
        # animate bacground
        if self.background_rect.right > 0:
            self.background_rect.left -= 1
        else:
            self.background_rect.left = 0
        # animate ground
        if self.ground_rect.right > 0:
            self.ground_rect.left -= 1
        else:
            self.ground_rect.left = 0

    def pipecollisionDetect(self):
        for pipe in self.pipes:
            if (
                self.bird.rect.colliderect(pipe.upperPipe_rect)
                or self.bird.rect.colliderect(pipe.bottomPipe_rect)
            ) and not self.gamestance == "PIPE_HIT":
                self.gamestance = "PIPE_HIT"
                self.hit_sound.play()

    def groundcollisionDetect(self):
        if (
            self.bird.rect.bottom > self.ground_rect.top
            and self.gamestance != "GAME_OVER"
        ):
            self.gamestance = "GAME_OVER"
            self.die_sound.play()

    def inputManage(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # key on keryboard clicked
            if event.type == KEYDOWN:
                # detect jumping, when pipe is hit game stops and we dont want to jump
                if (
                    event.key == K_SPACE
                    and self.gamestance == "MENU"
                    or self.gamestance == "GAME"
                ):
                    # if bird is already jumping we reset the height of jump
                    if self.bird.isJumping == True:
                        self.bird.j_speed = 18
                    else:
                        self.bird.isJumping = True
                    # play jump sound
                    self.wing_sound.play()
                    # every jump reset gravity power and angle
                    self.bird.angle = 15
                    self.bird.gravity = 5
                # if we in menu adc click something game starts
                if self.gamestance == "MENU":
                    self.gamestance = "GAME"
                # if we lost we can go back to menu
                if self.gamestance == "GAME_OVER":
                    self.gamestance = "MENU"
                    self.new_game()
            # mousebutton clicked
            if event.type == MOUSEBUTTONDOWN:
                # detect jumping, when pipe is hit game stops and we dont want to jump
                if (
                    event.button == 1
                    and self.gamestance == "MENU"
                    or self.gamestance == "GAME"
                ):
                    # if bird is already jumping we reset the height of jump
                    if self.bird.isJumping == True:
                        self.bird.j_speed = 18
                    else:
                        self.bird.isJumping = True
                    # play jump sound
                    self.wing_sound.play()
                    # every jump reset gravity power and angle
                    self.bird.angle = 15
                    self.bird.gravity = 5
                # if we in menu adc click something game starts
                if self.gamestance == "MENU":
                    self.gamestance = "GAME"
                # if we lost we can go back to menu
                elif self.gamestance == "GAME_OVER":
                    self.gamestance = "MENU"
                    self.new_game()

    def draw(self):
        # draw background and other one on right side so when original moves left we sill see background
        self.window.blit(self.background, self.background_rect.topleft)
        self.window.blit(self.background, self.background_rect.topright)
        # draw pipes
        for pipe in self.pipes:
            self.window.blit(pipe.upperPipe, pipe.upperPipe_rect.topleft)
            self.window.blit(pipe.bottomPipe, pipe.bottomPipe_rect.topleft)
        # the same with ground
        self.window.blit(self.ground, self.ground_rect.topleft)
        self.window.blit(self.ground, self.ground_rect.topright)
        # blit bird
        self.window.blit(self.bird.image, self.bird.rect.topleft)
        # blit score
        if self.gamestance != "MENU":
            self.drawScore()
        if self.gamestance == "MENU":
            self.window.blit(
                self.menu_graphics[self.tick // 30], self.menu_graphics_rect.topleft
            )
        if self.gamestance == "GAME_OVER":
            self.window.blit(self.gameover_graphic, self.gameover_graphic_rect.topleft)

    def drawScore(self):
        # change int score to str so we can eeasly pick number
        score = str(self.score)
        # length o surface wuth numbers, aour pngs have different width
        score_surface_len = 0
        # the we wil have x position of each number on surface
        score_posiotions = [0]
        for num in score:
            score_surface_len += self.numbers_images[int(num)].get_rect().width + 5
            score_posiotions.append(score_surface_len)
        # here we create surface to blit nuumbers
        scoreSurface = pygame.Surface((score_surface_len - 5, 36), pygame.SRCALPHA)
        for i in range(len(score)):
            scoreSurface.blit(
                self.numbers_images[int(score[i])], (score_posiotions[i], 0)
            )
        score_rect = scoreSurface.get_rect()
        score_rect.centerx = self.WIDTH // 2
        score_rect.y = 40
        # now we can blit score
        self.window.blit(scoreSurface, score_rect.topleft)

    def load_images(self):
        # load background
        self.background = pygame.image.load("sprites\\background-day.png")
        self.background_rect = self.background.get_rect()
        # load ground and place it on the bottom
        self.ground = pygame.image.load("sprites\\base.png")
        self.ground_rect = self.ground.get_rect()
        self.ground_rect.bottom = self.background_rect.bottom
        # load_numbers
        self.numbers_images = [
            pygame.image.load("sprites\\0.png"),
            pygame.image.load("sprites\\1.png"),
            pygame.image.load("sprites\\2.png"),
            pygame.image.load("sprites\\3.png"),
            pygame.image.load("sprites\\4.png"),
            pygame.image.load("sprites\\5.png"),
            pygame.image.load("sprites\\6.png"),
            pygame.image.load("sprites\\7.png"),
            pygame.image.load("sprites\\8.png"),
            pygame.image.load("sprites\\9.png"),
        ]
        # load_menu_graphics
        self.menu_graphics = [
            pygame.image.load("sprites\\message.png"),
            pygame.image.load("sprites\\message2.png"),
        ]
        self.menu_graphics_rect = self.menu_graphics[0].get_rect()
        self.menu_graphics_rect.center = (self.WIDTH // 2, 160)
        # load gamove grapighc
        self.gameover_graphic = pygame.image.load("sprites\\gameover.png")
        self.gameover_graphic_rect = self.gameover_graphic.get_rect()
        self.gameover_graphic_rect.centerx = self.WIDTH // 2
        self.gameover_graphic_rect.top = 100

    def load_sounds(self):
        self.hit_sound = pygame.mixer.Sound("audio\\hit.wav")
        self.die_sound = pygame.mixer.Sound("audio\\die.wav")
        self.point_sound = pygame.mixer.Sound("audio\\point.wav")
        self.wing_sound = pygame.mixer.Sound("audio\\wing.wav")


class Bird:
    def __init__(self, game):
        self.game = game
        self.gravity = 5
        self.loadImages()
        self.j_speed = 18
        self.angle = 15
        self.frames_for_image = self.game.framerate // len(self.images)
        self.isJumping = False

    def update(self):
        if self.isJumping and not self.game.gamestance == "PIPE_HIT":
            self.jump()
        else:
            self.useGravity()
        # animating bird
        self.animate()
        # make rotation
        self.rotate()

    def animate(self):
        # select image to draw based on framerate, we have 4 images to draw in 1 second
        if self.angle < -80:
            self.game.tick = 0

        self.image = self.images[self.game.tick // self.frames_for_image]

    def rotate(self):
        # rotate image
        rot_image = pygame.transform.rotate(self.image, self.angle)
        rot_image_rect = rot_image.get_rect()
        rot_image_rect.center = self.rect.center
        # save it
        self.image = rot_image
        self.rect = rot_image_rect
        # change angle
        if self.angle > -90:
            self.angle -= 1 * (self.gravity - 4)

    def useGravity(self):
        # using gravity on the bird
        self.rect.bottom += self.gravity
        # going faster in time
        self.gravity *= 1.04

    def jump(self):
        self.rect.y -= self.j_speed * 0.3
        self.j_speed -= 1
        if self.j_speed == -19:
            self.isJumping = False
            self.j_speed = 18

    def loadImages(self):
        # 4 frames to animate
        self.images = [
            pygame.image.load("sprites\\yellowbird-downflap.png"),
            pygame.image.load("sprites\\yellowbird-midflap.png"),
            pygame.image.load("sprites\\yellowbird-upflap.png"),
            pygame.image.load("sprites\\yellowbird-midflap.png"),
        ]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.game.WIDTH // 2, 205)


class Pipe:
    def __init__(self, game, pipeleft):
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
        self.upperPipe_rect.bottom = random.randint(40, 250)
        self.upperPipe_rect.left = pipeleft
        self.bottomPipe_rect.top = self.upperPipe_rect.bottom + 110
        self.bottomPipe_rect.left = pipeleft

    def load_images(self):
        # load bottom pipe
        self.bottomPipe = pygame.image.load("sprites\pipe-green.png")
        self.bottomPipe_rect = self.bottomPipe.get_rect()

        # make flipped
        self.upperPipe = pygame.transform.flip(self.bottomPipe, False, True)
        self.upperPipe_rect = self.upperPipe.get_rect()


if __name__ == "__main__":
    game = Game()
    game.mainLoop()
