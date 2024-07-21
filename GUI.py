import pygame
import sys

from settings import *
from math import sqrt

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = (100, 100, 100)

FPS = 20


class Ecosim:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Eco Sim")
        self.screen = pygame.display.set_mode((GRID[0], GRID[1]))

        self.clock = pygame.time.Clock()

    def draw_grid(self):

        for x in range(0, GRID[0], GRID_SIZE):
            pygame.draw.line(self.screen, GREY, (x, 0), (x, GRID[1]))
        for y in range(0, GRID[1], GRID_SIZE):
            pygame.draw.line(self.screen, GREY, (0, y), (GRID[0], y))

    def draw_vegpatch(self, dictionary, colour):

        for grid in dictionary.values():
            for veg_patch in grid:
                radius = int(sqrt(veg_patch.area / 3.142))
                if radius < 1:
                    radius = 1
                pygame.draw.circle(self.screen, colour, [veg_patch.pos[0], veg_patch.pos[1]], radius, 1)

    def draw_animals(self, dictionary, colour, radius):

        for grid in dictionary.values():
            for animal in grid:

                pygame.draw.circle(self.screen, colour, [int(animal.pos[0]), int(animal.pos[1])], radius, 1)

    def draw(self, ecosystem):

        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_vegpatch(ecosystem.veg_patches, GREEN)
        self.draw_animals(ecosystem.rbbts, BLUE, 2)
        self.draw_animals(ecosystem.foxes, RED, 2)

        pygame.display.flip()


    def run(self, ecosystem):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.draw(ecosystem)
        self.clock.tick(FPS)



