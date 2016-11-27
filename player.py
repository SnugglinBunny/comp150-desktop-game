import pygame

class Player:

    def __init__(self, x, y, width, height, imagePath, imagePathUp):
        self.x = x
        self.y = y
        self.width = width/4
        self.height = height/4
        self.velocity = 0

        self.images = pygame.image.load(imagePath)
        self.images = pygame.transform.scale(self.images, (self.width*8, self.height))
        self.imageRight = pygame.image.load(imagePath)
        self.imageRight = pygame.transform.scale(self.images, (self.width * 8, self.height))
        self.imageUp = pygame.image.load(imagePathUp)
        self.imageUp = pygame.transform.scale(self.imageUp, (40 * 8, self.height))
        self.numImages = 7
        self.currentImage = 0
        self.counter = 0
        self.inkCounter = 0
        self.punchCounter = 0
        self.health = 100

    def checkHealth(self):
        if self.health == 0:
            print 'You are dead gg.'

    def update(self):
        self.y -= self.velocity
        if self.currentImage < self.numImages:
            self.currentImage += 1
        else:
            self.currentImage = 1


    def render(self, screen):
            screen.blit(self.images, (self.x, self.y), (self.currentImage * self.width, 0, self.width, self.height))
