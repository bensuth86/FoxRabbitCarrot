import random
import inspect
from pprint import pprint


##---Parent Class---##

class Animal():

    #--instance attributes--#

    def __init__(self):
        # location as [x,y]
        self.location = [0,0]
        # Incremented by 1 for each turn
        self.age = 0
        # food instance count (carrot for rabbit, rabbit for fox)
        self.fooditem_consumed = 0 

    #--class attributes--#

    # distance moved per turn (x or y random interval)
    velocity = 1
    # turns animal exists unless starved or eaten
    lifespan = 1
    # area around e.g. rabbit, in which carrots disappear
    affect_radius = 5
    # total carrots consumed per turn (if in affect_area)
    consumption_rate = 8
    # rabbits created per loop/turn proportional to carrots consumed
    births_per_carrot = 0.5  
    
    

    #--methods--#

    def set_location(self):
        
        # initial x coordinate    
        x_value = random.randrange(grid[0])        
        self.location[0] = x_value
        # initial y coordinate  
        y_value = random.randrange(grid[1])        
        self.location[1] = y_value

    def move(self):
                
        # change x position #
        self.location[0] += random.choice((-1,1))*self.velocity
        # reset if x coord is off the grid
        if self.location[0] < 0:
            self.location[0] = self.location[0] * -1
        elif self.location[0] > grid[0]:
            self.location[0] = (2*grid[0]) - self.location[0]

        # change y position #
        self.location[1] += random.choice((-1,1))*self.velocity
        # reset if y coord is off the grid
        if self.location[1] < 0:
            self.location[1] = self.location[1] * -1
        elif self.location[1] > grid[1]:
            self.location[1] = (2*grid[1]) - self.location[1]

    #--To DO--
        #Eat objects within AoA
        #Give birth additional animals at location dending on objects consumed
        #Increment age
        #Delete animal if lifespan exceeded

     
class Rabbit(Animal):

    velocity = 2    
    lifespan = 100  
    affect_radius = 5
    consumption_rate = 8
    births_per_carrot = 0.5    
 
    
class Fox(Animal):

    velocity = 4
    lifespan = 50
    affect_radius = 8
    consumption_rate = 4
    births_per_rabbit = 0.2
    
    
class Population():
        
    def __init__(self, initial_rabbits):
        
        self.initial_animals = initial_rabbits

    def set_locations(self):

        for animal in self.initial_animals:
            animal.set_location()

    def move(self):

        for animal in self.initial_animals:
            animal.move()
            
    
   

#function to check if coord in area of affect
def InAreaOfAffect(x1,y1,x2,y2):

    if (x2-x1)**2 + (y2-y1)**2 <= affect_radius**2:
        return True
    else:
        return False

#Function for main programme loop:
#   a) Move rabbits 
#   b) for each rabbit:
#       1) Loop through all carrots
#       2) Remove carrots within rabbit area of affect, add to carrots_consumed
#       3) Create addtional rabbits at rabbit location depending on carrots consumed
#       4) Increment rabbit age and delete rabbit if lifespan exceeded
    
def setup_populations(total, Animal):

    initial_animals = []

    #create instances of animals
    for i in range(0,total):

        #create class instance
        oneanimal=Animal()
        #add onerabbit to initial_rabbits list
        initial_animals.append(oneanimal)

   #add initial_rabbits to instance of population class
    animal_population = Population(initial_animals)
    #set initial animal positions
    animal_population.set_locations()

    return animal_population
    
    
# -----------------------grid_setup [x,y] -----------------------------#
grid = [150,100]

#------------------------TO DO carrots setup----------------------------#
carrot_total = 200  

#------------------------TO DO rabbits setup----------------------------------#



rbbt_population = setup_populations(40,Rabbit)

print("\nRabbits\n\n")
for rabbit in rbbt_population.initial_animals:
	pprint(vars(rabbit))

rbbt_population.move()
print("\nRelocated Rabbits\n\n")
for rabbit in rbbt_population.initial_animals:
	pprint(vars(rabbit))

#------------------------TO DO foxes setup----------------------------------#



fox_population = setup_populations(4,Fox)

print("\nFoxes\n\n")
for fox in fox_population.initial_animals:
	pprint(vars(fox))
	
fox_population.move()
print("\nRelocated Foxes\n\n")
for fox in fox_population.initial_animals:
	pprint(vars(fox))



	
#-----------------------------------------------------------------------------Main Programme Loop--------------------------------------------------------------------------------#

##rbbt_population.move()

##numberOfTurns = 0
##
##print("Carrots:", len(carrots))
##print("Rabbits:", len(rabbits))
##print("Foxes:", len(foxes))
##print("\n")
##
##
##while numberOfTurns < 10:
##
##    numberOfTurns += 1
##    print("Turn:",numberOfTurns)
##    
##    print("CoL Rabbits")
##    CircleOfLife(rabbits,carrots)
##
##    # copy rabbits list for later iterations
##    rabbits_copy = rabbits[:]
##
##    print("Col Foxes")
##    CircleOfLife(foxes,rabbits)
##
##    print("Carrots:", len(carrots))
##    print("Rabbits:", len(rabbits))
##    print("Foxes:", len(foxes))


        
##for fox in foxes:    
##    pprint(vars(fox))
 

