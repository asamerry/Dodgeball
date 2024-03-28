import pygame
from random import randint

class Fireball:
    def __init__(self):
        self.image = pygame.image.load("data/entities/fireball.png")
        self.image.set_colorkey((0, 0, 0))

        self.start = randint(0, 640)

        if self.start < 120:
            self.end = randint(320, 640)
        elif self.start >= 120 and self.start <= 520:
            self.end = randint(120, 520)
        elif self.start > 520:
            self.end = randint(0, 320)

        self.slope = (self.end - self.start) / 480
        self.position = [self.start, 0]