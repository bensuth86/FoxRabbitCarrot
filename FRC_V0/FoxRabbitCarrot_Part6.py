import random
import inspect
import time

from tkinter import *

from pprint import pprint


##---Parent Class---##

class Animal():

        
        #--instance attributes--#

        def __init__(self):
                
                # location as [x,y]

                self.x = random.randrange(50,grid[0])                 
                self.y = random.randrange(50,grid[1])                 
                
                # Incremented by 1 for each turn
                self.age = 0
                # food instance count (carrot for rabbit, rabbit for fox)
                self.fooditem_consumed = 0        

        #--instance methods--#


        def move(self):

                                        
                # change x position #
                self.x += random.choice((-1,1))*self.velocity
                # reset if x coord is off the grid
                if self.x < 0:
                    self.x = self.x * -1
                elif self.x > grid[0]:
                    self.x = (2*grid[0]) - self.x

                # change y position #
                self.y += random.choice((-1,1))*self.velocity
                # reset if y coord is off the grid
                if self.y < 0:
                    self.y = self.y * -1
                elif self.y > grid[1]:
                    self.y = (2*grid[1]) - self.y


        def inAofA(self,prey):

                            

                if (prey.x-self.x)**2 + (prey.y-self.y)**2 <= self.affect_radius**2:
                        
                        
##                        print ("1.",self.FID, self.x,self.y)
##                        print ("2.",(prey.RID, prey.x,prey.y),)                  
                                                
                        return True
                else:
                        return False
                

        def hunt(self,prey):

                if self.inAofA(prey) == True:
                        self.prey_consumed += 1
##                        print("Prey consumed:",self.prey_consumed)
                        return True



class Carrot():

        def __init__(self):

                # location as [x,y]
                self.x = random.randrange(50,grid[0])                 
                self.y = random.randrange(50,grid[1])
                

        def plot_carrot(self):

                #TKINTER display
                x = self.x                
                y = self.y
                d = 1

                self.point = canvas.create_polygon(x-d,y-d,x+d,y-d,x,y+5, fill="orange")

        
                
             
class Rabbit(Animal):

        def __init__(self):
                #Tag Setup
                Animal.__init__(self)
                # e.g. RID = R001 #
                self.RID = "R"+str(Rabbit.RTag).zfill(3)
                Rabbit.RTag += 1
                
        
        #--Rabbit class attributes--#

        #class variable: Tag
        RTag = 1  #tag used to give unique id to each new rabbit instance
        
        velocity = 10  # distance moved per turn (x or y random interval)        
        lifespan = 50  # turns animal exists unless starved or eaten        
        affect_radius = 5  # area around e.g. rabbit, in which carrots disappear        
        consumption_rate = 20  # max carrots rabbit consumes per turn (if in affect_area)        
        births_per_meal = 0.5  # rabbits created per loop/turn proportional to carrots consumed         

        #--Rabbit instance attributes--#
        
        prey_consumed = 0 # actual carrots eaten
        birthpoints = 0   # calculated under Population.hunt (births_per_meal*prey_consumed) - new rabbit created when, birthpoints == 1
        age = 0 

        def plot_rabbit(self):

                #TKINTER display
                x = self.x                
                y = self.y
                a = self.affect_radius

                self.point = canvas.create_oval(x-2,y-2,x+2,y+2, fill="blue")
                self.AoA = canvas.create_oval(x-a,y-a,x+a,y+a, outline = "blue", fill="")
##                self.showRID = canvas.create_text(x+20,y-20,text=self.RID,fill = "blue")
 
    
class Fox(Animal):

        def __init__(self):
                # Tag Setup
                Animal.__init__(self)
                #e.g. FID = F001 #
                self.FID = "F"+str(Fox.FTag).zfill(3)
                Fox.FTag += 1    

        #--Fox class attributes--#
        #tag used to give unique id to each new fox instance
        FTag = 1

        velocity = 4
        lifespan = 100
        affect_radius = 50
        consumption_rate = 12
                
        births_per_meal = 0.25
 
        #--Fox instance attributes--#

        #actual rabbits eaten
        prey_consumed = 0
        birthpoints = 0
        age = 0

        def plot_fox(self):

                #TKINTER display
                x = self.x
                y = self.y
                a = self.affect_radius
                self.point = canvas.create_oval(x-3,y-3,x+3,y+3, fill="red")
##                self.AoA = canvas.create_oval(x-a,y-a,x+a,y+a, outline = "red", fill="")
##                self.showFID = canvas.create_text(x+20,y-20,text=self.FID,fill = "red")
##                self.showpreycon = canvas.create_text(x-20,y+20,text=self.prey_consumed,fill = "red")

class Carrot_population():

        def __init__(self, total):

                self.total = total
                self.initial_carrots = []

                #creat e carrot instances
                for i in range(0,self.total):

                        onecarrot = Carrot()
                        self.initial_carrots.append(onecarrot) #add onecarrot to initial_carrots list              

                self.current_population = self.initial_carrots[:]

        growth_rate=0.05
        rot_rate =0.03

        # carrots reproduce as % of current population e.g. 5% of population - rate = 0.005
        def pollinate(self):
                
                newcarrots = []
                n = self.growth_rate * len(self.current_population) # total new carrots to create
                n = int(n)
                

                for i in range(0, n):

                        onecarrot = Carrot()
                        newcarrots.append(onecarrot)

                self.current_population += newcarrots

        # after x turns remove % of carrots from current population
        def rot(self):

                turns=30
                if numberOfTurns % turns == 0: # for every 30 turns                        
                        
                        rottencarrots = len(self.current_population) / ((1+self.rot_rate)**turns)
                        
                        del self.current_population[int(rottencarrots):]

        
 #  Controls animal popultations                   
class Population():
        
        def __init__(self, total, Animal):
                
                #total population count
                self.total = total
                self.initial_animals = []

                #create instances of animals
                for i in range(0,self.total):

                        #create class instance
                        oneanimal=Animal()

                        #add onerabbit to initial_rabbits list
                        self.initial_animals.append(oneanimal)

                self.current_population = self.initial_animals[:]
            

        def move(self,species):

                species.move()


        def hunt(self,species,rbbt_population):


                dead_rabbits = []  # Store index positions for hunted rabbits to be deleteled once current for loop completes
                
                for rabbit in rbbt_population.current_population:
                        
                        if species.hunt(rabbit) == True: # prey consumed incremented by one

                                dead_rabbits.append(rbbt_population.current_population.index(rabbit))
                        
                        if species.prey_consumed == species.consumption_rate: # check if rabbits killed below consumpation rate; break loop accordingly

                                break

                # update birthpoints
                species.birthpoints += (species.prey_consumed * species.births_per_meal)

                # now remove dead rabbits from rabbit population
                dead_rabbits.sort()
                dead_rabbits.reverse()
               
                for i in dead_rabbits:
                        
                        del rbbt_population.current_population[i]
                
                 #reset prey_consumed to zero for next main loop turn
                species.prey_consumed = 0


        def reproduce(self,species):
                
                births_pending = int(species.birthpoints // 1) # animals to be born e.g. 2.5 // 1 = 2 births pending
                species.birthpoints = species.birthpoints%1 # remaining birthpoints: 2.5 % 1 = 0.5

                litter = [] # store newly created instances to add to all_births

                for i in range(0,births_pending):
                        
                        offspring = type(species)()  # create new instance depending on mother's class type i.e. fox or rabbit
                                               
                        #set location based on mother animals x, y coords
                        offspring.x = species.x + random.choice((-3,3))
                        offspring.y = species.y + random.choice((-3,3))

                        litter.append(offspring)
                

                return litter

                        

        def lifecycle(self,rbbt_population):

                all_births = [] #newly created per fox/ rabbit
                earmarked = [] #store fox/ rabbit that exceeded lifespan
                
                for species in self.current_population:

                        self.move(species)
                        self.hunt(species,rbbt_population)
                        
                        all_births += self.reproduce(species) # adds litter for each animal instance to all_births for current turn

                        species.age += 1 #increment age, check against lifespan
                        
                        if species.age == species.lifespan:
                                
                                earmarked.append(self.current_population.index(species)) # store index position of old fox/rabbit

                #remove earmarked fox/ rabbit from current population
                earmarked.sort()
                earmarked.reverse()

                for i in earmarked:

                        del self.current_population[i]

                # append new born fox/rabbit to current population
                self.current_population += all_births
                
                                

#Function for main programme loop:
#   a) Move foxes 
#   b) for each fox:
#       1) Loop through all rabbits
#       2) Remove rabbits within fox area of affect, add to rabbits_consumed
#       3) Create addtional foxes at fox location depending on rabbits consumed
#       4) Increment fox age and delete fox if lifespan exceeded

   
# -----------------------grid_setup [x,y] ----------------------------------#
grid = [1400,700]

#------------------Tkinter canvas setup-----------------------------------#
tk = Tk()
canvas = Canvas(tk, width = grid[0]+50, height = grid[1]+50)
tk.title("FoxRabbitCarrot")
canvas.pack()
       

#------------------------carrots setup-----------------------------#
crrt_population = Carrot_population(1000)

#------------------------Rabbits setup-------------------------------------#
rbbt_population = Population(400,Rabbit)

#------------------------Foxes setup---------------------------------------#
fox_population = Population(20,Fox)

#-----------------------------------------------------------------------------#

def plot_all():

        canvas.delete("all")
        for carrot in crrt_population.current_population:
                carrot.plot_carrot()
                
        for rabbit in rbbt_population.current_population:
                rabbit.plot_rabbit()

        for fox in fox_population.current_population:
                fox.plot_fox()

        tk.update()

        
def run_ecosystem():

        
        plot_all()        

        crrt_population.pollinate()
                                  
        rbbt_population.lifecycle(crrt_population)

        fox_population.lifecycle(rbbt_population)

        crrt_population.rot()

	
#-----------------------------------------------------------------------------Main Programme Loop--------------------------------------------------------------------------------#


numberOfTurns = 0

##while numberOfTurns < 2:
##        
##        numberOfTurns += 1
##        
##        run_ecosystem()
##        time.sleep(5)



while len(rbbt_population.current_population) > 0:
        
        numberOfTurns += 1
        run_ecosystem()
##        time.sleep(0.01)
    
print("Turns until all rabbits killed %s:" % numberOfTurns)

tk.mainloop()
