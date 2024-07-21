import random
import inspect
from pprint import pprint
    
# distance moved per turn (x or y random interval)
velocity = 2
    
# loops/turns rabbit exists unless starved or eaten
lifespan = 100

# area around rabbit in which carrots disappear
affect_radius = 5

# total carrots consumed per turn (if in affect_area)
consumption_rate = 8


### rabbits created per loop/turn proportional to carrots consumed
births_per_carrot = 0.5

### foxes created per loop/turn proportional to rabbits consumed
births_per_rabbit = 0.2

##multiply_rate = carrots_consumed * factor

class Carrot():
    
    location = []
    # Incremented by 1 for each turn


class Rabbit():
    
    location = []
    # Incremented by 1 for each turn
    age = 0
    carrots_consumed = 0
    # turns rabbit exists unless starved or eaten
    lifespan = 100
    

class Fox():
    
    location = []
    age = 0
    rabbits_consumed = 0
    lifespan = 50
    
# grid_setup [x,y] #

grid = [150,100]

#Function to create lists of random x, y values for appending to carrot,rabbit,fox_coord lists

def random_xcoords(total):
    x_values = [random.randrange(grid[0]) for i in range(total)]
    
    return x_values

def random_ycoords(total):
    y_values = [random.randrange(grid[1]) for i in range(total)]
    
    return y_values

def move_animals(rabbits):

    for rabbit in rabbits:
    
        #x-coord +/- velocity * 1 turn
        rabbit.location[0] += random.choice((-1,1))*velocity
        if rabbit.location[0] < 0:
            rabbit.location[0] * -1
        #y-coord +/- velocity * 1 turn
        rabbit.location[1] += random.choice((-1,1))*velocity
        if rabbit.location[1] < 0:
            rabbit.location[1] * -1
    

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
    
def CircleOfLife(rabbits,carrots):
    
    move_animals(rabbits)
    
    # copy carrots list for later iterations
    rabbits_copy = rabbits[:]
    
    #Loop through rabbits list
    for rbt_index, rabbit in enumerate(rabbits_copy):

        #Store index positions for rabbits to be deleted once current for loop completes
        rbts_to_delete= []

        # copy carrots list for later iterations
        carrots_copy = carrots[:]
        
        #Loop through carrots list        
        for crt_index, carrot in enumerate(carrots_copy):

            #Store index positions for carrots to be deleted once current for loop completes
            crts_to_delete= []
            # Consume carrots within affect area as per consumption rate
            # Check if carrot in rabbit area of affect. Increment carrots consumed, add carrot index to "crts_to_delete" list if True
            if InAreaOfAffect(rabbit.location[0],rabbit.location[1],carrot.location[0],carrot.location[1]) == True:
                
                rabbit.carrots_consumed += 1
                
                crts_to_delete.append(crt_index)
                
            #check if carrots consumed below consumption rate.  If reached,break the loop
            if rabbit.carrots_consumed == consumption_rate:
                break

##        print("Prey consumed:", rabbit.carrots_consumed)

        #now remove consumed carrots from carrots list
        crts_to_delete.sort()
        crts_to_delete.reverse()
        for i in crts_to_delete:
            del carrots[i]
            
        #update carrots_copy list for further iterations
        carrots_copy = carrots[:]                

        # TO DO- give birth to rabbits in proportion to carrots consumed
        births = rabbit.carrots_consumed*births_per_carrot
        births = int(births)        

##        print(rabbit.carrots_consumed)
##        print(births)
        #assign coords to new born rabbits according to parent rabbit position
        for i in range(0,births):
            
            kitten = Rabbit()
            kitten.location = [rabbit.location[0] + random.choice((-1,1))*velocity , rabbit.location[1] + random.choice((-1,1))*velocity]
            
##            pprint(vars(kitten))
            
            rabbits.append(kitten)

            
        # increment age of rabbit and delete if = to lifespane
        rabbit.age += 2
        
        if rabbit.age == Rabbit.lifespan:
            rbts_to_delete.append(rbt_index)

    #remove expired rabbits from rabbits list
    rbts_to_delete.sort()
    rbts_to_delete.reverse()
    for i in rbts_to_delete:
        del rabbits[i]
    
    

#--TO DO carrots setup--#
carrot_total = 200
carrots = []


#create lists of random x, y values for appending to carrot_coords list
x_carrots = random_xcoords(carrot_total)
y_carrots = random_ycoords(carrot_total)

for i in range(0,carrot_total):

    onecarrot=Carrot()
    
    #add x,y coords to location attribute
    onecarrot.location = [x_carrots[i],y_carrots[i]]
    # add one_carrot class object to all carrots list
    carrots.append(onecarrot)

# copy rabbits list for later iterations
carrots_copy = carrots[:]
  

#--rabbits setup--#
rabbit_total=40
rabbits = []

#create lists of random x, y values for appending to rabbit_coords list
x_rabbits = random_xcoords(rabbit_total)
y_rabbits = random_ycoords(rabbit_total)


for i in range(0,rabbit_total):

    onerabbit=Rabbit()
    
    # add x,y coords to location attribute
    onerabbit.location = [x_rabbits[i],y_rabbits[i]]
    # add one_rabbit class object to all rabbits list
    rabbits.append(onerabbit)


#--foxes setup--#
foxes_total=4
foxes = []

#create lists of random x, y values for appending to rabbit_coords list
x_foxes = random_xcoords(foxes_total)
y_foxes = random_ycoords(foxes_total)
        
for i in range(0,foxes_total):

    onefox=Fox()
    
    # add x,y coords to location attribute
    onefox.location = [x_foxes[i],y_foxes[i]]
    # add one_rabbit class object to all rabbits list
    foxes.append(onefox)


#-----------------------------------------------------------------------------Main Programme Loop--------------------------------------------------------------------------------#
numberOfTurns = 0

print("Carrots:", len(carrots))
print("Rabbits:", len(rabbits))
print("Foxes:", len(foxes))
print("\n")


while numberOfTurns < 10:

    numberOfTurns += 1
    print("Turn:",numberOfTurns)
    
    print("CoL Rabbits")
    CircleOfLife(rabbits,carrots)

    # copy rabbits list for later iterations
    rabbits_copy = rabbits[:]

    print("Col Foxes")
    CircleOfLife(foxes,rabbits)

    print("Carrots:", len(carrots))
    print("Rabbits:", len(rabbits))
    print("Foxes:", len(foxes))


        
##for fox in foxes:    
##    pprint(vars(fox))
 

