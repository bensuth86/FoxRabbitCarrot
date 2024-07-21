from settings import *
import string
from random import *
import numpy as np
from math import fabs, log


class VegPatch:

    def __init__(self, ecosystem, centre_x, centre_y, radius):

        self.ecosystem = ecosystem
        self.dictionary = self.ecosystem.veg_patches

        self.x = centre_x
        self.y = centre_y
        self.pos = np.array([self.x, self.y])  # position vector
        self.radius = radius
        self.cal_per_sqr = 100  # calories per unit area
        self.growth_rate = 1  # increase total area per turn
        self.grid_ref = "A1"  # default grid ref
        self.dictionary[self.grid_ref].append(self)
        # TO DO set growth rate to vary by inverse exponential (ln(radius)) depending on patch area

    def assign_grid(self):

        col_num = self.pos[0] // GRID_SIZE
        row_num = self.pos[1] // GRID_SIZE
        new_grid_ref = str(a_az[col_num]) + str(row_num)
        if new_grid_ref != self.grid_ref:
            self.dictionary[self.grid_ref].remove(self)
            self.dictionary[new_grid_ref].append(self)
            self.grid_ref = new_grid_ref


class Animal:

    """ Parent class for Fox, rabbit"""

    def __init__(self, ecosystem, x, y):

        # fixed attr
        self.ecosystem = ecosystem
        self.dictionary = self.ecosystem.rbbts  # default dictionary
        self.territory_rad = 1  # distance in which animal consumes prey
        self.speed = 1
        self.lifespan = 1  # turns animal exists unless starved or eaten
        self.calories = 100  # energy transferred to preditor
        self.consumption = 2
        self.reprod_rate = 1/5  # 1/n - 1 offspring created every n turns

        # variable attr
        self.pos = np.array([x, y])  # position vector
        self.vel = np.array([0, 0])  # velocity vector
        self.grid_ref = "A1"  # default grid ref
        self.total_energy = 10000  # starting energy (declines every turn)
        self.age = 0  # Incremented by 1 for each turn

    def assign_grid(self):

        col_num = self.pos[0] // GRID_SIZE
        row_num = self.pos[1] // GRID_SIZE
        new_grid_ref = str(a_az[col_num]) + str(row_num)
        if new_grid_ref != self.grid_ref:
            self.dictionary[self.grid_ref].remove(self)
            self.dictionary[new_grid_ref].append(self)
            self.grid_ref = new_grid_ref

    def move(self):

        self.vel[0] = self.speed * random.choice((-1, 1))
        self.vel[1] = self.speed * random.choice((-1, 1))

        # reset if off the grid
        if self.pos[0] > GRID[0]:
            self.vel[0] = -fabs(self.vel[0])  # vel.x defaults to negative
        elif self.pos[1] > GRID[1]:
            self.vel[1] = -fabs(self.vel[1])  # vel.y defaults to negative

        self.pos += self.vel

    def in_territory(self, prey):

        target_vec = prey.pos - self.pos
        if np.linalg.norm(target_vec) <= self.territory_rad:  # target vector magnitude within territorial radius
            return True
        else:
            return False

    def hunt(self, prey):

        if self.in_territory(prey) is True:
            self.total_energy += prey.calories
            # TO DO 'delete' prey instance

    def reproduce(self):

        pass

class Rabbit(Animal):

    def __init__(self, ecosystem, x, y):
        Animal.__init__(self, ecosystem, x, y)
        # fixed attr
        # self.dictionary = self.ecosystem.rbbts  # dictionary in which rabbit instances are stored
        self.dictionary[self.grid_ref].append(self)
        self.territory_rad = 20  # distance in which animal consumes prey
        self.speed = 5
        self.lifespan = 30  # turns animal exists unless starved or eaten
        self.calories = 500  # energy transferred to preditor
        self.A_consm = 1  # area of veg patch comsumed per turn
        self.reprod_rate = 1/3  # 1/n - 1 offspring created every n turns

        # variable attr
        self.total_energy = 5000  # starting energy (declines every turn)


class Fox(Animal):

    def __init__(self, ecosystem, x, y):

        Animal.__init__(self, ecosystem, x, y)
        # fixed attr
        self.dictionary = self.ecosystem.foxes  # dictionary in which fox instances are stored
        self.dictionary[self.grid_ref].append(self)
        self.territory_rad = 60  # distance in which animal consumes prey
        self.speed = 20
        self.lifespan = 90  # turns animal exists unless starved or eaten
        self.prey_consm = 5  # rbbts consumed per turn
        self.reprod_rate = 1 / 10  # 1/n - 1 offspring created every n turns

        # variable attr
        self.total_energy = 10000  # starting energy (declines every turn)


class Ecosystem:

    def __init__(self, veg_count, rabbit_count, fox_count):

        # create veg_patch inst- assign to grids overlapping patch area
        # create rbbt, fox inst at random points- assign to relevant grid
        self.veg_patches = {}
        self.rbbts = {}
        self.foxes = {}
        self.population_setup()

        for i in range(0, veg_count):
            veg_patch = VegPatch(self, randrange(0, GRID[0]), randrange(0, GRID[1]), randrange(5, 25))
            veg_patch.assign_grid()
        for i in range(0, rabbit_count):
            rabbit = Rabbit(self, randrange(0, GRID[0]), randrange(0, GRID[1]))
            rabbit.assign_grid()
        for i in range(0, fox_count):
            fox = Fox(self, randrange(0, GRID[0]), randrange(0, GRID[1]))
            fox.assign_grid()

    def population_setup(self):
        "Initialise dictionary for each species where instances are assigned to grid reference key depending on x, y locations"

        for sector in grid_sectors:
            self.veg_patches.update({sector: []})
            self.rbbts.update({sector: []})
            self.foxes.update({sector: []})

    def lifecycle(self):
        "Veg patch growth. Move animals, hunt, reproduce"


def grid_setup():

    a_z = list(string.ascii_uppercase)  # list of strings A-Z
    a_az = a_z + (list((a_z[0]) + letter for letter in a_z))  # A-AZ  (52 possible columns)
    grid_sectors = []  # list of grid refs: A1, A2, A3 etc

    for i in range(int(GRID[0]/GRID_SIZE)):
        col = a_az[i]
        for j in range(int(GRID[1]/GRID_SIZE)):
            row = str(j)
            grid_sectors.append(col+row)

    return a_az, grid_sectors


a_az, grid_sectors = grid_setup()
ecosystem = Ecosystem(100, 20, 5)
print()
