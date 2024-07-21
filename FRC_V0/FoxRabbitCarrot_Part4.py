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
                        
                        
                        print ("1.",self.FID, self.x,self.y)
                        print ("2.",(prey.RID, prey.x,prey.y),)                  
                                                
                        return True
                else:
                        return False
                

        def hunt(self,prey):

                if self.inAofA(prey) == True:
                        self.prey_consumed += 1
##                        print("Prey consumed:",self.prey_consumed)
                        return True

                        

        #--To DO--
        
        #Give birth additional animals at location dending on objects consumed
        #Increment age
        #Delete animal if lifespan exceeded
             
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
        lifespan = 100  # turns animal exists unless starved or eaten        
        affect_radius = 5  # area around e.g. rabbit, in which carrots disappear        
        consumption_rate = 8  # max carrots rabbit consumes per turn (if in affect_area)        
        births_per_meal = 0.5  # rabbits created per loop/turn proportional to carrots consumed         

        #--Rabbit instance attributes--#
        
        prey_consumed = 0 # actual carrots eaten
        birthpoints = 0   # calculated under Population.hunt (births_per_meal*prey_consumed) - new rabbit created once equal to 1 

        def plot_rabbit(self):

                #TKINTER display
                x = self.x                
                y = self.y

                self.point = canvas.create_oval(x-2,y-2,x+2,y+2, fill="blue")
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
        lifespan = 50
        affect_radius = 50
        consumption_rate = 4
        prey_consumed = 0
        
        births_per_meal = 0.25
 
        #--Fox instance attributes--#

        #actual rabbits eaten
        prey_consumed = 0
        birthpoints = 0

        def plot_fox(self):

                #TKINTER display
                x = self.x
                y = self.y
                a = self.affect_radius
                self.point = canvas.create_oval(x-3,y-3,x+3,y+3, fill="red")
                self.AoA = canvas.create_oval(x-a,y-a,x+a,y+a, outline = "red", fill="")
                self.showFID = canvas.create_text(x+20,y-20,text=self.FID,fill = "red")
                self.showpreycon = canvas.create_text(x-20,y+20,text=self.prey_consumed,fill = "red")

                    
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
                 
            

        def move(self):

                for animal in self.current_population:
                        animal.move()
                        #update Tkinter display
                        


        def hunt(self,rbbt_population):

                for animal in self.current_population:

##                        print("\n Rabbits left:",len(rbbt_population.current_population), "\n")
                        
                        
                        dead_rabbits = []  # Store index positions for hunted rabbits to be deleteled once current for loop completes
                        
                        for rabbit in rbbt_population.current_population:
                                
                                if animal.hunt(rabbit) == True: # prey consumed incremented by one

                                        dead_rabbits.append(rbbt_population.current_population.index(rabbit))

##                                        print("Rabbit index",rbbt_population.current_population.index(rabbit))
                                
                                if animal.prey_consumed == animal.consumption_rate: # check if rabbits killed below consumpation rate; break loop accordingly
##                                        print("Foxy full up!")
                                        break

                        # update birthpoints
                        animal.birthpoints += (animal.prey_consumed * animal.births_per_meal)

                        # now remove dead rabbits from rabbit population
                        dead_rabbits.sort()
                        dead_rabbits.reverse()
                       
                        for i in dead_rabbits:
                                
                                del rbbt_population.current_population[i]
                        
                         #reset prey_consumed to zero for next main loop turn
##                        animal.prey_consumed = 0


        def reproduce(self):

                births_pending = int(birthpoints // 1)
                pass

                
                

                

#Function for main programme loop:
#   a) Move rabbits 
#   b) for each rabbit:
#       1) Loop through all carrots
#       2) Remove carrots within rabbit area of affect, add to carrots_consumed
#       3) TO DO Create addtional rabbits at rabbit location depending on carrots consumed
#       4) TO DO Increment rabbit age and delete rabbit if lifespan exceeded

   
# -----------------------grid_setup [x,y] ----------------------------------#
grid = [1200,600]

#------------------Tkinter canvas setup-----------------------------------#
tk = Tk()
canvas = Canvas(tk, width = grid[0]+50, height = grid[1]+50)
tk.title("FoxRabbitCarrot")
canvas.pack()
       

#------------------------TO DO carrots setup-----------------------------#
carrot_total = 200  

#------------------------Rabbits setup-------------------------------------#
rbbt_population = Population(400,Rabbit)

#------------------------Foxes setup---------------------------------------#
fox_population = Population(40,Fox)

#-----------------------------------------------------------------------------#

def plot_all():

        canvas.delete("all")        
        for rabbit in rbbt_population.current_population:
                rabbit.plot_rabbit()

        for fox in fox_population.current_population:
                fox.plot_fox()

        tk.update()




def run_ecosystem():

        
        plot_all()
        
        rbbt_population.move()
        fox_population.move()
               
        fox_population.hunt(rbbt_population)

        plot_all()
                
        
        

	
#-----------------------------------------------------------------------------Main Programme Loop--------------------------------------------------------------------------------#


numberOfTurns = 0

while numberOfTurns < 1:
        
        numberOfTurns += 1
        
        run_ecosystem()
        time.sleep(0.1)



##while len(rbbt_population.current_population) > 0:
##        
##        numberOfTurns += 1
##        run_ecosystem()
####        time.sleep(0.001)
##    
##print("Turns until all rabbits killed %s:" % numberOfTurns)
##
##tk.mainloop()
