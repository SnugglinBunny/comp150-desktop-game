import pygame


class Player:

    def __init__(self, x, y, width, height, image_path, image_path_up, image_path_electric, image_path_electric_up):
        self.x = x
        self.y = y
        self.width = width/4
        self.height = height/4
        self.velocity = 0

        self.images = pygame.image.load(image_path)
        self.images = pygame.transform.scale(self.images, (self.width*8, self.height))
        self.imageRight = pygame.image.load(image_path)
        self.imageRight = pygame.transform.scale(self.images, (self.width * 8, self.height))
        self.imageUp = pygame.image.load(image_path_up)
        self.imageUp = pygame.transform.scale(self.imageUp, (40 * 8, self.height))
        self.imagesElectric = pygame.image.load(image_path_electric)
        self.imagesElectric = pygame.transform.scale(self.imagesElectric, (self.width * 8, self.height))
        self.imagesElectricRight = pygame.image.load(image_path_electric)
        self.imagesElectricRight = pygame.transform.scale(self.imagesElectric, (self.width * 8, self.height))
        self.imagesElectricUp = pygame.image.load(image_path_electric_up)
        self.imagesElectricUp = pygame.transform.scale(self.imagesElectricUp, (40 * 8, self.height))
        self.numImages = 7
        self.currentImage = 0
        self.counter = 0
        self.inkCounter = 0
        self.punchCounter = 0
        self.health = 100

    def check_health(self):
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
