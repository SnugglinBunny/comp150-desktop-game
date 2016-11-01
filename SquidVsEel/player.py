import pygame

class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 426
        self.height = 455
        self.velocity = 0
        self.falling = True
        self.onGround = False

        self.images = pygame.image.load("Images/SquidWalk.png")
        self.numImages = 7
        self.currentImage = 0


    def update(self):
        self.y -= self.velocity
        if self.currentImage < self.numImages:
            self.currentImage += 1
        else:
            self.currentImage = 1


    def render(self, screen):
            screen.blit(self.images, (self.x, self.y), (self.currentImage * self.width, 0, self.width, self.height))
