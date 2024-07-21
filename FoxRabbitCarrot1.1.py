import string
from random import *
import numpy as np
from math import sqrt
from timeit import default_timer as timer

from settings import *
from GUI import *


class VegPatch:

    def __init__(self, ecosystem, centre_x, centre_y, area):

        self.ecosystem = ecosystem
        self.dictionary = self.ecosystem.veg_patches

        self.x = centre_x
        self.y = centre_y
        self.pos = np.array([self.x, self.y])  # position vector
        self.area = area
        self.cal_per_sqr = 100  # calories per unit area
        self.growth_rate = 1  # increase total area per turn
        self.grid_ref = "A1"  # default grid ref
        self.dictionary[self.grid_ref].append(self)

    def assign_grid(self):

        col_num = self.pos[0] // GRID_SIZE
        row_num = self.pos[1] // GRID_SIZE
        new_grid_ref = a_az[col_num] + str(row_num)
        if new_grid_ref != self.grid_ref:
            self.dictionary[self.grid_ref].remove(self)
            self.dictionary[new_grid_ref].append(self)
            self.grid_ref = new_grid_ref

    def grow(self):
        "Patch areas grow at logistic rate"

        r = 0.05  # growth rate per capita
        max_area = 9000  # max area patch can grow as t approaches infinity
        da_dt = r*((max_area-self.area)/max_area)*self.area
        self.area += da_dt


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
        self.reprod_rate = 100  # n - 1 offspring created every n turns
        self.burn_rate = 100  # calories burned every turn

        # variable attr
        self.pos = np.array([x, y])  # position vector
        self.vel = np.array([0, 0])  # velocity vector
        self.grid_ref = "A1"  # default grid ref
        self.total_energy = 10000  # starting energy (declines every turn)

        self.age = 1  # Incremented by 1 for each turn

    def assign_grid(self):

        col_num = self.pos[0] // GRID_SIZE
        row_num = self.pos[1] // GRID_SIZE
        new_grid_ref = a_az[col_num] + str(row_num)
        if new_grid_ref != self.grid_ref:
            self.dictionary[self.grid_ref].remove(self)
            self.dictionary[new_grid_ref].append(self)
            self.grid_ref = new_grid_ref

    def move(self):

        self.vel[0] = choice((-1, 1)) * self.speed
        self.vel[1] = choice((-1, 1)) * self.speed

        # reset if off the grid
        if not 0 < self.pos[0] + self.vel[0] < GRID[0]:
            self.vel[0] = 0
        if not 0 < self.pos[1] + self.vel[1] < GRID[1]:
            self.vel[1] = 0

        self.pos += self.vel
        self.assign_grid()

    def reproduce(self):

        bell = self.age % self.reprod_rate
        if bell == 0:
            offspring = type(self)(self.ecosystem, self.pos[0], self.pos[1])
            offspring.assign_grid()

    def migrate(self):
        pass

    def expire(self):

        dead = False
        self.age += 1
        self.total_energy -= self.burn_rate

        if self.age > self.lifespan:
            dead = True
        elif self.total_energy < 0:
            dead = True

        if dead:
            self, self.dictionary[self.grid_ref].pop()


class Rabbit(Animal):

    def __init__(self, ecosystem, x, y):
        Animal.__init__(self, ecosystem, x, y)
        # fixed attr
        # self.dictionary = self.ecosystem.rbbts  # dictionary in which rabbit instances are stored
        self.dictionary[self.grid_ref].append(self)
        self.territory_rad = 20  # distance in which animal consumes prey
        self.speed = 5
        self.lifespan = 150  # turns animal exists unless starved or eaten
        self.calories = 500  # energy transferred to preditor
        self.A_consm = 10  # area of veg patch comsumed per turn
        self.burn_rate = 100  # calories burned every turn
        self.reprod_rate = 30  # n - 1 offspring created every n turns

        # variable attr
        self.total_energy = 5000  # starting energy (declines every turn)

    def graze(self, veg_patch):

        target_vec = veg_patch.pos - self.pos
        veg_radius = int(sqrt(veg_patch.area / 3.142))
        if np.linalg.norm(target_vec) - veg_radius <= self.territory_rad:  # target vector magnitude within territorial radius
            in_range = True
        else:
            in_range = False

        if in_range:
            self.total_energy += veg_patch.cal_per_sqr
            veg_patch.area -= self.A_consm
            if veg_patch.area < 1:  # limit such that patch area never completely destroyed
                veg_patch.area = 1


class Fox(Animal):

    def __init__(self, ecosystem, x, y):

        Animal.__init__(self, ecosystem, x, y)
        # fixed attr
        self.dictionary = self.ecosystem.foxes  # dictionary in which fox instances are stored
        self.dictionary[self.grid_ref].append(self)
        self.territory_rad = 60  # distance in which animal consumes prey
        self.speed = 20
        self.lifespan = 500  # turns animal exists unless starved or eaten
        self.prey_consm = 5  # rbbts consumed per turn
        self.burn_rate = 100  # calories burned every turn
        self.reprod_rate = 100  # 1/n - 1 offspring created every n turns

        # variable attr
        self.total_energy = 10000  # starting energy (declines every turn)

    def hunt(self, prey):

        target_vec = prey.pos - self.pos
        if np.linalg.norm(target_vec) <= self.territory_rad:  # target vector magnitude within territorial radius
            in_range = True
        else:
            in_range = False

        if in_range:
            self.total_energy += prey.calories
            prey, ecosystem.rbbts[prey.grid_ref].pop()


class Ecosystem:

    def __init__(self, veg_count, rabbit_count, fox_count):

        "create veg_patch inst- assign to grids overlapping patch area,  create rbbt, fox inst at random points- assign to relevant grid"
        self.running = True
        # Initialise dictionary for each species where instances are assigned to grid reference key, depending on x, y locations
        self.veg_patches = {sector: [] for sector in grid_sectors}
        self.rbbts = {sector: [] for sector in grid_sectors}
        self.foxes = {sector: [] for sector in grid_sectors}

        for i in range(0, veg_count):
            veg_patch = VegPatch(self, randrange(0, GRID[0]), randrange(0, GRID[1]), randrange(100, 2000))
            veg_patch.assign_grid()
        for i in range(0, rabbit_count):
            rabbit = Rabbit(self, randrange(0, GRID[0]), randrange(0, GRID[1]))
            rabbit.assign_grid()
        for i in range(0, fox_count):
            fox = Fox(self, randrange(0, GRID[0]), randrange(0, GRID[1]))
            fox.assign_grid()

    def lifecycle(self):
        "Veg patch growth. Move animals, hunt, reproduce"
        start1 = timer()
        for veg_patches in self.veg_patches.values():
            for patch in veg_patches:
                patch.grow()

        for grid_ref, rabbits in self.rbbts.items():
            for rabbit in rabbits:
                rabbit.move()
                rabbit.migrate()
                [rabbit.graze(veg_patch) for veg_patch in self.veg_patches[grid_ref]]
                rabbit.reproduce()
                rabbit.expire()
                # print(grid_ref, '->', animals)

        for grid_ref, foxes in self.foxes.items():
            for fox in foxes:
                fox.move()
                fox.migrate()
                [fox.hunt(rabbit) for rabbit in self.rbbts[grid_ref]]
                fox.reproduce()
                fox.expire()
                # print(grid_ref, '->', animals)

        end1 = timer()
        # print(end1 - start1)


def grid_setup():

    a_z = list(string.ascii_uppercase)  # list of strings A-Z
    a_az = a_z + (list((a_z[0]) + letter for letter in a_z))  # A-AZ  (52 possible columns)

    # list of grid refs: A1, A2, A3 etc
    grid_sectors = [(a_az[i] + str(j))
        for i in range(int(GRID[0]/GRID_SIZE))
        for j in range(int(GRID[1]/GRID_SIZE))]

    return a_az, grid_sectors


a_az, grid_sectors = grid_setup()
ecosystem = Ecosystem(100, 20, 5)
ecosim = Ecosim()  # pygame animation

while ecosystem.running:
    ecosystem.lifecycle()
    ecosim.run(ecosystem)
