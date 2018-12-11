################################################# Packages/Libraries ##########################################################
import matplotlib.pyplot as plt
import numpy as np
import random

############################################ Variables and Functions ##########################################################


warehouseWidth = 800
warehouseHeight = 650
shelfWidth = 50
laneWidth = 50
nbrOfAGVs = 6  # Number of vehicles, originally it was set to 6
speed = 10
AGVRadius = 12.5
chargingRate = 0.05
consumingRate = 0.05
thresholdPower = 3.5
fullyCharged = 10
taskFactor = 0.001  # Probability to create a task for each shelf
nNodesx = 6
nNodesy = 3
unloadingTime = 20
loadingTime = 10
removalTime = 50


class AGV(object):

    def __init__(self, pos, fullyCharged):
        self.position = pos
        self.direction = 0
        self.status = 'free'  # free, charging, occupied, loading, unloading
        self.power = fullyCharged
        self.clock = 0
        self.parkdir = 0  # to be able to save direction before loading
        self.hasTask = False


class Shelf(object):

    def __init__(self, pos, priority):
        self.position = pos
        self.status = 'no task'
        self.priority = priority


def update_AGV_direction(a, nodes):
    chargeBias = 1
    if a.power <= thresholdPower:
        chargeBias = 0.25

    nodeNbr = nodes.index(a.position)
    r = np.random.rand()

    if nodeNbr in [0, 2, 4]:
        a.direction = 0
    if nodeNbr in [5, 11]:
        a.direction = -np.pi / 2
    if nodeNbr in [1, 3, 7, 9]:
        if r < 1 / 2:
            a.direction = 0
        else:
            a.direction = -np.pi / 2
    if nodeNbr in [6, 8, 10]:
        if r < chargeBias * 1 / 2:
            a.direction = 0
        else:
            a.direction = np.pi / 2
    if nodeNbr in [14, 16]:
        if r < chargeBias * 1 / 2:
            a.direction = np.pi
        else:
            a.direction = np.pi / 2
    if nodeNbr in [13, 15, 17]:
        a.direction = np.pi
    if nodeNbr == 12:
        a.direction = np.pi / 2
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
            if a.power > consumingRate and a.status == 'occupied':
                a.power = a.power - 1.2 * consumingRate
            elif a.power > consumingRate and a.status != 'occupied':
                a.power = a.power - consumingRate
            else:
                if a.status == 'out of battery':
                    if a.clock >= removalTime:
                        for node in nodes[0:6]:  # Loop through all of the charging nodes
                            nodePos = list(node)
                            nodePos[1] = nodePos[1] + laneWidth
                            nodePos = tuple(nodePos)
                            if isEmpty(nodePos) == True:  # Check if this node is empty
                                a.position = nodePos
                                a.clock = 0
                                a.status = 'charging'
                                break
                    else:
                        a.clock = a.clock + 1
                else:
                    a.power = 0
                    a.clock = 0
                    a.status = 'out of battery'


def check_for_shelf(a, shelfs, shelfPositions):
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
    if check2 in shelfPositions and is_shelf == False:
        shelfNbr = shelfPositions.index(check2)
        if shelfs[shelfNbr].status == 'task':
            a.position = check2
            a.status = 'loading'
            shelfs[shelfNbr].status = 'no task'
            a.parkdir = 0
            is_shelf = True
    return [a, is_shelf]


def move_AGV(AGV, nodes, shelfs, shelfPositions):
    global completed_tasks
    for a in AGV:
        if a.power >= consumingRate:
            if a.status == 'loading':
                if a.clock == loadingTime:
                    pos = list(a.position)
                    pos[0] = pos[0] + laneWidth * np.cos(a.parkdir)
                    a.position = tuple(pos)
                    a.clock = 0
                    a.status = 'occupied'
                    a.hasTask = True
                else:
                    a.clock = a.clock + 1
            elif a.status == 'unloading':
                if (a.clock == unloadingTime):
                    pos = list(a.position)
                    a.direction = np.pi / 2
                    pos[1] = pos[1] + laneWidth * np.sin(a.direction)
                    a.position = tuple(pos)
                    a.clock = 0
                    a.status = 'free'
                    completed_tasks = completed_tasks +1
                if (a.clock < unloadingTime):
                    pos = list(a.position)
                    pos[1] = 0.5 * laneWidth
                    a.position = tuple(pos)
                    a.clock += 1
            elif a.status == 'charging':
                if a.power >= fullyCharged:
                    a.power = fullyCharged
                    pos = list(a.position)
                    pos[1] = pos[1] - laneWidth
                    a.position = tuple(pos)
                    if a.hasTask == True:
                        a.status = 'occupied'
                    else:
                        a.status = 'free'
            elif a.position in nodes:
                nodeNbr = nodes.index(a.position)
                pos = list(a.position)
                pos[1] = pos[1] + laneWidth  # Position where the AGV will move to charge
                if nodeNbr in [0, 1, 2, 3, 4, 5] and a.power <= thresholdPower and isEmpty(pos):
                    a.position = tuple(pos)
                    a.direction = - np.pi / 2
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


def isEmpty(position):
    for a in AGVs:
        if a.position == position:
            return False
    return True


def unload_AGVs(AGV):  # A function to unload the AGVs
    for a in AGV:
        posa = np.array(a.position)
        xa = posa[0]
        ya = posa[1]
        if (a.status == 'occupied') and (ya == 1.5 * laneWidth) and (a.position in nodes[13:18]):
            for b in AGV:  # Check if there is another AGV down which is unloading now
                posb = np.array(b.position)
                xb = posb[0]
                yb = posb[1]
                if (a != b) and (b.status == 'unloading') and (xa == xb):  # Remain occupied if another AGV unloads
                    a.status = 'occupied'
                    return
            a.status = 'unloading'


def plot_AGVs(AGV):
    for a in AGV:
        pos = np.array(a.position)
        x = pos[0]
        y = pos[1]
        if a.status == 'free':
            c = plt.Circle((x, y), AGVRadius, edgecolor='k', facecolor='blue', zorder=1)
        elif a.status == 'occupied':
            c = plt.Circle((x, y), AGVRadius, edgecolor='k', facecolor='red', zorder=1)
        else:
            c = plt.Circle((x, y), AGVRadius, edgecolor='k', facecolor='green')

        fig = plt.gcf()
        ax = fig.gca()
        ax.add_artist(c)
        plt.axis([0, warehouseWidth, 0, warehouseHeight])
    # plt.pause(1)


def map_shelfs(shelf_matrix):
    global shelfPositions
    global shelfPriority
    for (i, j), value in np.ndenumerate(shelf_matrix):
        if (shelf_matrix[i][j] != 0):
            pos = (50 * j + laneWidth / 2, 50 * i + laneWidth / 2)
            shelfPositions.append(pos)
            shelfPriority.append(shelf_matrix[i][j])
    # return shelfPositions


def plot_shelfs(shelfs):  # A function to plot the shelfs
    for s in shelfs:
        pos = list(s.position)
        if (s.status == 'no task'):
            plt.plot(pos[0], pos[1], 'ks', markersize=20)  # Blue for those without a task...
        if (s.status == 'task'):
            plt.plot(pos[0], pos[1], 'rs', markersize=20)  # Red if it has a task!


def create_task(shelfs, taskFactor):  # A function to create tasks for each shelf
    for s in shelfs:
        chance = random.uniform(0, 1)
        scaledTaskFactor = taskFactor / s.priority
        if (scaledTaskFactor > chance) and (s.status == 'no task'):  # Create task only if the shelf has no task
            s.status = 'task'
    return shelfs

def run_test(shelf_test_matrix, task_goal):
    global nodes
    global AGVs
    global shelfs
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
        prio = shelfPriority[i]
        s = Shelf(pos, prio)
        shelfs.append(s)


    # Create Nodes

    for n in range(nNodesy):
        xPos = np.linspace(laneWidth/2, warehouseWidth - laneWidth/2, nNodesx)
        for i in range(len(xPos)):
            pos = (np.int(xPos[i]), warehouseHeight - 75 - np.int(n * (warehouseHeight-150)/(nNodesy-1)))
            nodes.append(pos)



    time = 0
    while completed_tasks < task_goal:
        time = time +1
        plt.figure(1)
        plt.clf()
        TitleString = 'Time: ' + str(time) + ', Completed Tasks: ' + str(completed_tasks)
        plt.title(TitleString)
        plot_shelfs(shelfs)
        plot_AGVs(AGVs)
        plt.pause(0.0005)
        move_AGV(AGVs, nodes, shelfs, shelfPositions)
        update_AGV_power(AGVs)
        # Time to give some tasks to each shelf!
        shelfs = create_task(shelfs, taskFactor)
        unload_AGVs(AGVs)
    return time
################################################## Driver Code ######################################################



shelf_test_matrix = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
                              [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
                              [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
                              [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
                              [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
                              [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
                              [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])




#task_goal_list = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
task_goal_list = [50]
NbrofTests = 5
avg_list = []
for task_goal in task_goal_list:
    print('Goal: ', task_goal)
    timeList = []
    for i in range(NbrofTests):
        print(i+1)
        completed_tasks = 0
        shelfPositions = []
        shelfPriority = []
        nodes = []
        AGVs = []
        shelfs = []
        timeList.append(run_test(shelf_test_matrix,task_goal))


    timeList = np.array(timeList)
    print('Times: ',  timeList)
    avgTime = np.sum(timeList)/NbrofTests
    print('Avg Time: ',avgTime)
    avg_list.append(avgTime)


plt.figure(3)
plt.plot(task_goal_list, avg_list, 'k.')
plt.show()

