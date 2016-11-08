import pygame

class Player:

    def __init__(self, x, y, width, height, imagePath):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 0

        self.images = pygame.image.load(imagePath)
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
