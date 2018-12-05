################################################# Packages/Libraries ##########################################################
import matplotlib.pyplot as plt
import numpy as np
import random


############################################ Variables and Functions ##########################################################


warehouseWidth = 900
warehouseHeight = 550
shelfWidth = 50
laneWidth = 50
nbrOfAGVs = 6
speed = 2
AGVRadius = 12.5
chargingRate = 0.05
consumingRate = 0.005
thresholdPower = 3.5
fullyCharged = 10
taskFactor = .05   #Probability to create a task for each shelf
nNodesx = 6
nNodesy = 3
unloadingTime = 20
loadingTime = 10


class AGV(object):

    def __init__(self, pos, fullyCharged):
        self.position = pos
        self.direction = - np.pi/2
        self.status = 'free'  # free, charging, occupied, loading, unloading
        self.power = fullyCharged
        self.clock = 0

class Shelf(object):

    def __init__(self, pos, priority):
        self.position = pos
        self.status = 'no task'
        self.priority = 1

def update_AGV_direction(a, nodes):
    chargeBias = 1
    if a.power <= thresholdPower:
        chargeBias = 1.8

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
    return a


def update_AGV_position(a):
    pos = list(a.position)
    pos[0] = pos[0] + speed * np.cos(a.direction)
    pos[1] = pos[1] + speed * np.sin(a.direction)
    a.position = tuple(pos)
    return a


#def check_for_shelf(a,shelfs):

#    return a

def move_AGV(AGV, nodes, shelfPositions):
    for a in AGV:
        # if charging, loading, unloading:
        if a.status == 'loading':
            if a.clock == loadingTime:
                pos = list(a.position)
                pos[1] = laneWidth*np.cos(a.direction)
                a.position = tuple(pos)
                a.clock = 0
                a.status = 'occupied'
            else:
                a.clock = a.clock + 1
        elif a.status == 'unloading':
            if a.clock == unloadingTime:
                pos = list(a.position)
                pos[1] = laneWidth*np.cos(np.pi/2)
                a.position = tuple(pos)
                a.clock = 0
                a.status == 'free'
            else:
                a.clock = a.clock + 1
        elif a.status == 'charging':
            if a.power == fullyCharged:
                pos = list(a.position)
                pos[1] = laneWidth*np.cos(a.direction)
                a.position = tuple(pos)
        elif a.position in nodes:
            if a.power < thresholdPower:
                nodeNbr = nodes.index(a.position)
                if nodeNbr in [0,1,2,3,4,5]:
                    pos = list(a.position)
                    pos[1] = laneWidth * np.sin(np.pi/2)
                    a.position = tuple(pos)
                    a.direction = - np.pi/2
                    a.status = 'charging'
            else:
                a = update_AGV_direction(a, nodes)
                a = update_AGV_position(a)
        else:
            a = update_AGV_position(a)
    return AGV

# else for each agv:
    #check if on loading, charging or uloading position, move to appropriate pos
    # update direction
    # check if any agv in the way
    # if no:
    #   update position


#




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

def map_shelfs(shelf_matrix):
    global shelfPositions
    for (i,j), value in np.ndenumerate(shelf_matrix):
        if(shelf_matrix[i][j] == 1):
            pos = (50*j, 50*i)
            shelfPositions.append(pos)


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

#shelfPositions = [(75, warehouseHeight - 125 ), (125, warehouseHeight - 125 ), (225, warehouseHeight - 125 ), (275, warehouseHeight - 125 ), (325, warehouseHeight - 125 ), (375, warehouseHeight - 125 ), (425, warehouseHeight - 125 ), (475, warehouseHeight - 125 ), (525, warehouseHeight - 125 ), (575, warehouseHeight - 125 )]
shelfPositions = []
shelf_test_matrix = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
map_shelfs(shelf_test_matrix)

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

#print(nodes)
#plt.plot(nodes[:,0],nodes[:,1], 'o')


for i in range(100):
    plt.figure(2)
    plt.clf()
    plot_AGVs(AGVs)
    plot_shelfs(shelfs)
    plt.pause(0.005)
    AGV = move_AGV(AGVs, nodes, shelfPositions)







