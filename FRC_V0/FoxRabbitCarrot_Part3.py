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

                #--instance methods--#


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


        def inAofA(self,prey):

                            

                if (prey.location[0]-self.location[0])**2 + (prey.location[1]-self.location[1])**2 <= self.affect_radius**2:                                            
                    
##                        print ("1.",self.FID, self.location)
##                        print ("2.",(prey.RID, prey.location[0],prey.location[1]),)
                        return True
                else:
                        return False

        def hunt(self,prey):

                if self.inAofA(prey) == True:
                        self.prey_consumed += 1
##                        print("Prey consumed:",self.prey_consumed)
                        return True
                    

        #--To DO--
        #Eat objects within AoA
        #Give birth additional animals at location dending on objects consumed
        #Increment age
        #Delete animal if lifespan exceeded
             
class Rabbit(Animal):
        
        #--Rabbit class attributes--#

        #class variable: Tag
        #tag used to give unique id to each new rabbit instance
        RTag = 1

        # distance moved per turn (x or y random interval)
        velocity = 2
        # turns animal exists unless starved or eaten
        lifespan = 100
        # area around e.g. rabbit, in which carrots disappear
        affect_radius = 5
        # max carrots rabbit consumes per turn (if in affect_area)
        consumption_rate = 8
        # rabbits created per loop/turn proportional to carrots consumed
        births_per_carrot = 0.5      

        #--Rabbit instance attributes--#

        # actual carrots eaten
        prey_consumed = 0
    

        def __init__(self):

                Animal.__init__(self)
                # e.g. RID = R001 #
                self.RID = "R"+str(Rabbit.RTag).zfill(3)
                Rabbit.RTag += 1
 
    
class Fox(Animal):
        
    
        #--Fox class attributes--#
        #tag used to give unique id to each new fox instance
        FTag = 1

        velocity = 4
        lifespan = 50
        affect_radius = 8
        consumption_rate = 4
        prey_consumed = 0
        births_per_rabbit = 0.2

        #--Fox instance attributes--#

        #actual rabbits eaten
        prey_consumed = 0

        def __init__(self):

                Animal.__init__(self)
                #e.g. FID = F001 #
                self.FID = "F"+str(Fox.FTag).zfill(3)
                Fox.FTag += 1    

    
class Population():
        
        def __init__(self, total, Animal):
                
                #total population count
                self.total = total
                self.initial_animals = []

                #create instances of animals
                for i in range(0,self.total):

                        #create class instance
                        oneanimal=Animal()
                        #call set_location to assign x,y cooord
                        oneanimal.set_location()

                        #add onerabbit to initial_rabbits list
                        self.initial_animals.append(oneanimal)

                self.current_population = self.initial_animals[:]
            

        def move(self):

                for animal in self.current_population:
                        animal.move()


        def hunt(self,rbbt_population):

                for animal in self.current_population:

##                        print("\n Rabbits left:",len(rbbt_population.current_population), "\n")
                        
                        # Store index positions for hunted rabbits to be deleteled once current for loop completes
                        dead_rabbits = []
                        
                        for rabbit in rbbt_population.current_population:
                                

                                if animal.hunt(rabbit) == True:

                                        dead_rabbits.append(rbbt_population.current_population.index(rabbit))

##                                        print("Rabbit index",rbbt_population.current_population.index(rabbit))

                                # check if rabbits killed below consumpation rate; break loop accordingly
                                if animal.prey_consumed == animal.consumption_rate:
##                                        print("Foxy full up!")
                                        break

                        # now remove dead rabbits from rabbit population
                        dead_rabbits.sort()
                        dead_rabbits.reverse()
##                        print(dead_rabbits)
                        for i in dead_rabbits:
                                
                                del rbbt_population.current_population[i]
                                

#Function for main programme loop:
#   a) Move rabbits 
#   b) for each rabbit:
#       1) Loop through all carrots
#       2) Remove carrots within rabbit area of affect, add to carrots_consumed
#       3) Create addtional rabbits at rabbit location depending on carrots consumed
#       4) Increment rabbit age and delete rabbit if lifespan exceeded

   
# -----------------------grid_setup [x,y] ----------------------------------#
grid = [150,100]

#------------------------TO DO carrots setup--------------------------------#
carrot_total = 200  

#------------------------Rabbits setup--------------------------------#
rbbt_population = Population(80,Rabbit)

#------------------------Foxes setup----------------------------------#
fox_population = Population(8,Fox)

#---------------------------------------------------------------------------#


def run_ecosystem():
        
        rbbt_population.move()

        fox_population.hunt(rbbt_population)
        fox_population.move()

	
#-----------------------------------------------------------------------------Main Programme Loop--------------------------------------------------------------------------------#



numberOfTurns = 0

while len(rbbt_population.current_population) > 0:
        
        numberOfTurns += 1
        
        run_ecosystem()
    
print("Turns until all rabbits killed %s:" % numberOfTurns)

