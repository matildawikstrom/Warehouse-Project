################################################# Packages/Libraries ##########################################################
import matplotlib.pyplot as plt
import numpy as np
import random


############################################ Variables and Functions ##########################################################


warehouseWidth = 800
warehouseHeight = 600
shelfWidth = 50
laneWidth = 50
nbrOfAGVs = 6          #Number of vehicles, originally it was set to 6
speed = 5
AGVRadius = 12.5
chargingRate = 0.2
consumingRate = 0.2
thresholdPower = 3.5
fullyCharged = 10
taskFactor = 0.0005   #Probability to create a task for each shelf
nNodesx = 6
nNodesy = 3
unloadingTime = 20
loadingTime = 10
completed_tasks = 0
simulationTime = 1200



class AGV(object):

    def __init__(self, pos, fullyCharged):
        self.position = pos
        self.direction = 0
        self.status = 'free'  # free, charging, occupied, loading, unloading
        self.power = fullyCharged
        self.clock = 0
        self.parkdir = 0 #to be able to save direction before loading

class Shelf(object):

    def __init__(self, pos, priority):
        self.position = pos
        self.status = 'no task'
        self.priority = 1

def update_AGV_direction(a, nodes):
    chargeBias = 1
    if a.power <= thresholdPower:
        chargeBias = 0.25

    nodeNbr = nodes.index(a.position)
    r = np.random.rand()

    if nodeNbr in [0, 2, 4]:
        a.direction = 0
    if nodeNbr in [5, 11]:
            a.direction = -np.pi/2
    if nodeNbr in [1, 3, 7, 9]:
        if r < 1/2:
            a.direction = 0
        else:
            a.direction = -np.pi/2
    if nodeNbr in [6, 8, 10]:
        if r < chargeBias*1/2:
            a.direction = 0
        else:
            a.direction = np.pi/2
    if nodeNbr in [14, 16]:
        if r < chargeBias*1/2:
            a.direction = np.pi
        else:
            a.direction = np.pi/2
    if nodeNbr in [13, 15, 17]:
        a.direction = np.pi
    if nodeNbr == 12:
        a.direction = np.pi/2
    return a


def update_AGV_position(a):
    pos = list(a.position)
    pos[0] = pos[0] + speed * np.cos(a.direction)
    pos[1] = pos[1] + speed * np.sin(a.direction)
    a.position = tuple(pos)
    return a

def update_AGV_power(AGVs):
    for a in AGVs:
        if a.status == 'charging':
            a.power = a.power + chargingRate
        else:
            if a.power > consumingRate:
                a.power = a.power - consumingRate
            else:
                a.power = 0
        print(a.power)


def check_for_shelf(a,shelfs, shelfPositions):
    pos = list(a.position)
    check1 = tuple([pos[0] + laneWidth, pos[1]])
    check2 = tuple([pos[0] - laneWidth, pos[1]])
    is_shelf = False
    if check1 in shelfPositions:
        shelfNbr = shelfPositions.index(check1)
        if shelfs[shelfNbr].status == 'task':
            a.position = check1
            a.status = 'loading'
            shelfs[shelfNbr].status = 'no task'
            a.parkdir = np.pi
            is_shelf = True
    if check2 in shelfPositions:
        print('yes')
        shelfNbr = shelfPositions.index(check2)
        if shelfs[shelfNbr].status == 'task':
            a.position = check2
            a.status = 'loading'
            shelfs[shelfNbr].status = 'no task'
            a.parkdir = 0
            is_shelf = True
    return [a, is_shelf]


def move_AGV(AGV, nodes,shelfs, shelfPositions):
    for a in AGV:
        # if charging, loading, unloading:
        if a.status == 'loading':
            if a.clock == loadingTime:
                pos = list(a.position)
                pos[0] = pos[0] + laneWidth*np.cos(a.parkdir)
                a.position = tuple(pos)
                a.clock = 0
                a.status = 'occupied'
            else:
                a.clock = a.clock + 1
        elif a.status == 'unloading':
            if a.clock == unloadingTime:
                pos = list(a.position)
                pos[0] = pos[0] + laneWidth*np.cos(a.parkdir)
                a.position = tuple(pos)
                a.clock = 0
                a.status == 'free'
            else:
                a.clock = a.clock + 1
        elif a.status == 'charging':
            if a.power >= fullyCharged:
                a.power = fullyCharged
                pos = list(a.position)
                pos[1] = pos[1] - laneWidth
                a.position = tuple(pos)
                a.status = 'free'
        elif a.position in nodes:
            if a.power <= thresholdPower:
                nodeNbr = nodes.index(a.position)
                if nodeNbr in [0,1,2,3,4,5]:
                    pos = list(a.position)
                    pos[1] = pos[1] + laneWidth
                    a.position = tuple(pos)
                    a.direction = - np.pi/2
                    a.status = 'charging'
            else:
                a = update_AGV_direction(a, nodes)
                a = update_AGV_position(a)
        elif a.status == 'free':
            tmp = check_for_shelf(a, shelfs, shelfPositions)
            if tmp[1] == False:
                a = update_AGV_position(a)
        else:
            a = update_AGV_position(a)
    return AGV


def plot_AGVs(AGV):
    for a in AGV:
        pos = np.array(a.position)
        x = pos[0]
        y = pos[1]
        if a.status == 'free':
            c = plt.Circle((x, y), AGVRadius, edgecolor='k', facecolor='blue', zorder=1000)
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
            pos = (50*j+laneWidth/2, 50*i+laneWidth/2)
            shelfPositions.append(pos)
    return shelfPositions


def plot_shelfs(shelfs):        #A function to plot the shelfs
    for s in shelfs:
        pos = list(s.position)
        if (s.status == 'no task'):
            plt.plot(pos[0], pos[1], 'ks', markersize=20)  #Blue for those without a task...
        if (s.status == 'task'):
            plt.plot(pos[0], pos[1], 'rs', markersize=20)  #Red if it has a task!
        

def create_task(shelfs):     #A function to create tasks for each shelf
    for s in shelfs:
        chance = random.uniform(0,1)
        if (taskFactor > chance) and (s.status == 'no task'):   #Create task only if the shelf has no task
            s.status = 'task'
    return shelfs
                

################################################## Driver Code ######################################################


AGVs = []
shelfs = []
shelfPositions = []
shelf_test_matrix = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
                              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
shelfPositions = map_shelfs(shelf_test_matrix)

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
shelfs = create_task(shelfs)

# Create Nodes
nodes = []
for n in range(nNodesy):
    xPos = np.linspace(laneWidth/2, warehouseWidth - laneWidth/2, nNodesx)
    for i in range(len(xPos)):
        pos = (np.int(xPos[i]), warehouseHeight - 75 - np.int(n * (warehouseHeight-100)/(nNodesy-1)))
        nodes.append(pos)

#print(nodes)
#plt.plot(nodes[:,0],nodes[:,1], 'o')
print(shelfPositions)

for i in range(simulationTime):
    #print(i)
    plt.figure(2)
    plt.clf()
    plot_shelfs(shelfs)
    plot_AGVs(AGVs)
    plt.pause(0.0005)
    move_AGV(AGVs, nodes, shelfs, shelfPositions)
    update_AGV_power(AGVs)
    # Time to give some tasks to each shelf!
    shelfs = create_task(shelfs)








