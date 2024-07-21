import string
from random import *
import numpy as np
from math import *
from timeit import default_timer as timer
from matplot_live_pop import *

from settings import *
from GUI import *

### TODO ###

# incorporate litter size into reproduction
# foxes


class VegPatch:

    def __init__(self, ecosystem, centre_x, centre_y, area):

        self.ecosystem = ecosystem
        self.dictionary = self.ecosystem.veg_patches

        self.x = centre_x
        self.y = centre_y
        self.pos = np.array([self.x, self.y])  # position vector
        self.area = area
        self.cal_per_sqr = 500  # calories per unit area
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

        r = 0.02  # growth rate per capita
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
        self.speed = 1  # pixels moved per turn
        self.lifespan = 100  # turns animal exists unless starved or eaten
        self.starvation = 40  # turns animal can survive without eating
        self.calories = 1000  # energy transferred to preditor

        self.birth_rate = 100  # n-1 offspring created every n turns
        self.littersize = 1
        self.burn_rate = 100  # calories burned every turn

        # variable attr
        self.age = 1  # Incremented by 1 for each turn
        self.pos = np.array([x, y])  # position vector
        self.vel = np.array([0, 0])  # velocity vector
        self.grid_ref = "A1"  # default grid ref
        self.total_energy = 10000  # starting energy (declines every turn).  For each turn, animal will eat until total energy level reaches starting energy.
                                   # when total energy reaches zero starvation occurs; animal migrates, turns_starved incremented.
        self.turns_starved = 0  # keep count of nos turns animal in starvation mode ( total_energy = 0)

    def assign_grid(self):

        col_num = self.pos[0] // GRID_SIZE
        row_num = self.pos[1] // GRID_SIZE
        new_grid_ref = a_az[col_num] + str(row_num)
        if new_grid_ref != self.grid_ref:
            self.dictionary[self.grid_ref].remove(self)
            self.dictionary[new_grid_ref].append(self)
            self.grid_ref = new_grid_ref

    def reset_grid(self):
        # set velocity to zero to prevent going off the grid
        if not 0 < self.pos[0] + self.vel[0] < GRID[0]:
            self.vel[0] = 0
        if not 0 < self.pos[1] + self.vel[1] < GRID[1]:
            self.vel[1] = 0

    def move(self):

        self.vel[0] = choice((-1, 1)) * self.speed
        self.vel[1] = choice((-1, 1)) * self.speed

        self.reset_grid()

        self.pos += self.vel
        self.assign_grid()

    def reproduce(self, littersize):

        bell = self.age % self.birth_rate
        if bell == 0:
            for i in range(0, littersize):
                offspring = type(self)(self.ecosystem, self.pos[0], self.pos[1])
                offspring.assign_grid()

    def migrate(self):

        def cart2polar(pos):
            "Translate x, y such that (0, 0) at screen centre.  Then convert to polar coords about screen centre"
            trans_pos = pos - np.array([GRID[0] / 2, GRID[1] / 2])  # translate such the that (0, 0) at centre of the screen
            x, y = trans_pos[0], trans_pos[1]
            r = sqrt(x**2 + y**2)
            theta = atan2(y, x)  # returns theta between -pi < theta < pi
            theta = (theta + 2 * pi) % (2 * pi)  # convert theta to range 0 < theta < 2pi
            n = 1 + (r // (1 * GRID_SIZE))  # n = count of loops of the spiral (1 turning = 2pi radians)
            if n == 0:
                 print("FAIL!")
            theta += 2 * pi * n  # angle + previous loops
            return r, theta

        def polar2cart(r, theta):
            "Convert back to cartesian and translate back to standard ref frame, (0, 0) at top left of screen"
            x = r*cos(theta)
            y = r*sin(theta)
            new_trans_pos = np.array([x, y])
            new_pos = new_trans_pos + np.array([GRID[0] / 2, GRID[1] / 2])  # back to (0, 0) located at top left of screen
            new_pos = new_pos.astype(int)  # np[x, y] float to integer
            return new_pos

        def spiral_arc(pos):
            "calculate new position such that object follows a archimedal spiral path about screen centre over multiple turns"
            rad, ang = cart2polar(pos)
            a = rad / ang  # constant for arch spiral
            if rad < 50:
                self.speed = (fabs(self.speed))  # spiral out (clockwise)
            elif rad > GRID[0]/4:
                self.speed = -(fabs(self.speed))  # spiral in (anticlockwise)
            new_ang = ((((ang + 1) ** (3 / 2)) + (self.speed * 3 / (2 * a))) ** (2 / 3)) - 1
            new_rad = a*new_ang  # corresp radius
            new_pos = polar2cart(new_rad, new_ang)
            # print(rad)
            return new_pos

        new_pos = spiral_arc(self.pos)
        self.vel = new_pos - self.pos
        self.reset_grid()  # reset vel to zero if moving off screen
        self.pos += self.vel
        self.assign_grid()

    def expire(self):
        # TODO Simply function
        dead = False
        self.age += 1

        if self.age > self.lifespan:
            dead = True
        if self.turns_starved > self.starvation:
            dead = True

        if dead:
            self, self.dictionary[self.grid_ref].pop()

    def lifecycle(self, prey):
        " Animal does following actions every turn "
        self.total_energy -= self.burn_rate
        # self.turns_starved += 1
        if self.total_energy < RB_START_ENERGY:
            self.eat(prey)
        if self.total_energy <= 0:
            self.total_energy = 0
            self.turns_starved += 1
            # print(self.turns_starved)

        if self.total_energy > 0:
            self.move()
        else:
            self.migrate()

        self.reproduce(self.littersize)
        self.expire()


class Rabbit(Animal):

    def __init__(self, ecosystem, x, y):
        Animal.__init__(self, ecosystem, x, y)
        # fixed attr
        self.dictionary = self.ecosystem.rbbts  # dictionary in which rabbit instances are stored
        self.dictionary[self.grid_ref].append(self)
        self.territory_rad = 2  # distance in which animal consumes prey
        self.speed = 5
        self.lifespan = 800  # turns animal exists unless starved or eaten
        self.starvation = 60  # turns animal can survive without eating (must be less than birth rate)
        self.calories = 2000  # energy transferred to preditor
        self.A_consm = 60  # area of veg patch comsumed per turn
        self.burn_rate = 100  # calories burned every turn
        self.birth_rate = 200  # n - 1 offspring created every n turns
        self.littersize = 3

        # variable attr
        self.total_energy = RB_START_ENERGY  # starting energy (declines every turn)

    def eat(self, veg_patches):

        for patch in veg_patches:

            target_vec = patch.pos - self.pos
            veg_radius = int(sqrt(patch.area / 3.142))
            if np.linalg.norm(target_vec) - veg_radius <= self.territory_rad:  # target vector magnitude within territorial radius
                in_range = True
            else:
                in_range = False

            if in_range:
                self.total_energy += patch.cal_per_sqr
                # print(self.total_energy)
                self.turns_starved = 0
                patch.area -= self.A_consm
                if patch.area < 1:  # limit such that patch area never completely destroyed
                    patch.area = 1


class Fox(Animal):

    def __init__(self, ecosystem, x, y):

        Animal.__init__(self, ecosystem, x, y)
        # fixed attr
        self.dictionary = self.ecosystem.foxes  # dictionary in which fox instances are stored
        self.dictionary[self.grid_ref].append(self)
        self.territory_rad = 60  # distance in which animal consumes prey
        self.speed = 15
        self.lifespan = 250  # turns animal exists unless starved or eaten
        self.starvation = 40  # turns animal can survive without eating (must be less than birth rate)
        self.burn_rate = 300  # calories burned every turn
        self.birth_rate = 300  # 1/n - 1 offspring created every n turns
        self.littersize = 1

        # variable attr
        self.total_energy = FX_START_ENERGY  # starting energy (declines every turn)

    def eat(self, rbbts):

        for rabbit in rbbts:
            target_vec = rabbit.pos - self.pos
            if np.linalg.norm(target_vec) <= self.territory_rad:  # target vector magnitude within territorial radius
                in_range = True
            else:
                in_range = False

            if in_range:
                self.total_energy += rabbit.calories
                self.turns_starved = 0
                rabbit, ecosystem.rbbts[rabbit.grid_ref].pop()


class Ecosystem:

    def __init__(self, start_veg, start_rbbt, start_fox):

        "create veg_patch inst- assign to grids overlapping patch area,  create rbbt, fox inst at random points- assign to relevant grid"
        self.running = True
        self.turns = 0
        # Initialise dictionary for each species where instances are assigned to grid reference key, depending on x, y locations
        self.veg_patches = {sector: [] for sector in grid_sectors}
        self.rbbts = {sector: [] for sector in grid_sectors}
        self.foxes = {sector: [] for sector in grid_sectors}

        for i in range(0, start_veg):
            veg_patch = VegPatch(self, randrange(0, GRID[0]), randrange(0, GRID[1]), randrange(100, 2000))
            veg_patch.assign_grid()
        for i in range(0, start_rbbt):
            rabbit = Rabbit(self, randrange(0, GRID[0]), randrange(0, GRID[1]))
            # rabbit = Rabbit(self, int(GRID[0]/2), int(GRID[1]/2)+1)
            rabbit.assign_grid()
        for i in range(0, start_fox):
            fox = Fox(self, randrange(0, GRID[0]), randrange(0, GRID[1]))
            fox.assign_grid()

    def population_count(self):
        "Return total population for each species"
        veg_count = sum([len(self.veg_patches[i]) for i in self.veg_patches if isinstance(self.veg_patches[i], list)])
        rbbt_count = sum([len(self.rbbts[i]) for i in self.rbbts if isinstance(self.rbbts[i], list)])
        fox_count = sum([len(self.foxes[i]) for i in self.foxes if isinstance(self.foxes[i], list)])

        return veg_count, rbbt_count, fox_count

    def run(self):
        "Veg patch growth. Move animals, hunt, reproduce"
        start1 = timer()
        veg_count, rbbt_count, fox_count = self.population_count()
        record_population(self.turns, rbbt_count, fox_count)
        self.turns += 1

        for veg_patches in self.veg_patches.values():
            for patch in veg_patches:
                patch.grow()

        for grid_ref, rabbits in self.rbbts.items():
            for rabbit in rabbits:
                rabbit.lifecycle(self.veg_patches[grid_ref])

        for grid_ref, foxes in self.foxes.items():
            for fox in foxes:
                fox.lifecycle(self.rbbts[grid_ref])


def grid_setup():

    a_z = list(string.ascii_uppercase)  # list of strings A-Z
    a_az = a_z + (list((a_z[0]) + letter for letter in a_z))  # A-AZ  (52 possible columns)

    # list of grid refs: A1, A2, A3 etc
    grid_sectors = [(a_az[i] + str(j))
        for i in range(int(GRID[0]/GRID_SIZE))
        for j in range(int(GRID[1]/GRID_SIZE))]

    return a_az, grid_sectors


a_az, grid_sectors = grid_setup()
# ecosystem = Ecosystem(0, 0, 1)
ecosystem = Ecosystem(200, 300, 5)
ecosim = Ecosim()  # pygame animation

while ecosystem.running:
    ecosystem.run()
    ecosim.run(ecosystem)
    if ecosystem.turns > 2000:
        ecosystem.running = False

plot_population()

