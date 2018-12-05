################################################# Packages/Libraries ##########################################################
import matplotlib.pyplot as plt
import numpy as np
import random


############################################ Variables and Functions ##########################################################


warehouseWidth = 880
warehouseHeight = 550
laneWidth = 50
nbrOfAGVs = 6
speed = 4
AGVRadius = 12.5
chargingRate = 0.05
consumingRate = 0.005
thresholdPower = 3.5
fullyCharged = 10
taskFactor = .05   #Probability to create a task for each shelf
nNodesx = 6
nNodesy = 3



class AGV(object):

    def __init__(self, pos, fullyCharged):
        self.position = pos
        self.direction = - np.pi/2
        self.status = 'free'
        self.power = fullyCharged

class Shelf(object):

    def __init__(self, pos, priority):
        self.position = pos
        self.status = 'no task'
        self.priority = 1

def update_AGV_position(AGV, nodes):
    for a in AGV:
        chargeBias = 1
        if a.power <= 3.5:
            chargeBias = 1.8
        if a.position in nodes:
            nodeNbr = nodes.index(a.position)
            r = np.random.rand()

            if nodeNbr == 0 or nodeNbr == 2 or nodeNbr == 4:
                a.direction = 0
            if nodeNbr == 5 or nodeNbr == 11:
                    a.direction = -np.pi/2
            if nodeNbr == 13 or nodeNbr == 15 or nodeNbr == 17:
                a.direction = np.pi
            if nodeNbr == 1 or nodeNbr == 3 or nodeNbr == 7 or nodeNbr == 9:
                if r < 1/2:
                    a.direction = 0
                else:
                    a.direction = -np.pi/2
            if nodeNbr == 6 or nodeNbr == 8 or nodeNbr == 10:
                if r < chargeBias*1/2:
                    a.direction = 0
                else:
                    a.direction = np.pi/2
            if nodeNbr == 12 or nodeNbr == 14 or nodeNbr == 16:
                if r < chargeBias*1/2:
                    a.direction = np.pi
                else:
                    a.direction = np.pi /2
            if nodeNbr == 13 or nodeNbr == 15:
                if r < 1/2:
                    a.direction = np.pi
                else:
                    a.direction = -np.pi /2





def plot_AGVs(AGV):
    for a in AGV:
        pos = np.array(a.position)
        x = pos[0]
        y = pos[1]
        if a.status == 'free':
            c = plt.Circle((x, y), AGVRadius, edgecolor='k', facecolor='blue')
        elif a.status == 'occupied':
            c = plt.Circle((x, y), AGVRadius, edgecolor='k', facecolor='red')
        else:
            c = plt.Circle((x, y), AGVRadius, edgecolor='k', facecolor='green')

        fig = plt.gcf()
        ax = fig.gca()
        ax.add_artist(c)
        plt.axis([0, warehouseWidth, 0 , warehouseHeight])
    #plt.pause(1)


def plot_shelfs(shelfs):        #A function to plot the shelfs
    for s in shelfs:
        pos = list(s.position)
        if (s.status == 'no task'):
            plt.plot(pos[0], pos[1], 'rs')  #Red for those with no task...
        if (s.status == 'task'):
            plt.plot(pos[0], pos[1], 'ys')  #Yellow if it has a task!
        

def create_task(shelf):     #A function to create tasks for each shelf
    for s in shelfs:
        chance = random.uniform(0, 1)
        if (taskFactor > chance) and (s.status == 'no task'):   #Create task only if the shelf has no task
            s.status = 'task'

                


################################################## Driver Code ######################################################


AGVs = []
shelfs = []

shelfPositions = [(75, warehouseHeight - 125 ), (125, warehouseHeight - 125 ), (225, warehouseHeight - 125 ), (275, warehouseHeight - 125 ), (325, warehouseHeight - 125 ), (375, warehouseHeight - 125 ), (425, warehouseHeight - 125 ), (475, warehouseHeight - 125 ), (525, warehouseHeight - 125 ), (575, warehouseHeight - 125 )]
#print(shelfPositions)

# Initialize AGVs
startPosx = np.linspace(0 + laneWidth/2, warehouseWidth - laneWidth/2, nbrOfAGVs)
for i in range(len(startPosx)):
    pos = (startPosx[i], warehouseHeight - 75)
    a = AGV(pos, fullyCharged)
    AGVs.append(a)


#Update the list 'shelfs' to contain each shelf here:
for i in range(len(shelfPositions)):
    pos = shelfPositions[i]
    s = Shelf(pos, 1)
    shelfs.append(s)


# Time to give some tasks to each shelf!
for s in range(len(shelfs)):
    create_task(s)

# Create Nodes
nodes = []
for n in range(nNodesy):
    xPos = np.linspace(laneWidth/2, warehouseWidth - laneWidth/2, nNodesx)
    for i in range(len(xPos)):
        pos = (np.int(xPos[i]), warehouseHeight - 75 - np.int(n * (warehouseHeight-100)/(nNodesy-1)))
        nodes.append(pos)

print(nodes)
#plt.plot(nodes[:,0],nodes[:,1], 'o')



plt.figure(2)
plt.clf()
plot_AGVs(AGVs)
plot_shelfs(shelfs)
plt.show()





