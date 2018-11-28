################################################# Packages/Libraries ##########################################################
import matplotlib.pyplot as plt
import numpy as np


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


class AGV(object):

    def __init__(self, pos, fullyCharged):
        self.position = pos
        self.status = 'free'
        self.power = fullyCharged

class Shelf(object):

    def __init__(self, pos, priority):
        self.position = pos
        self.status = 'no task'
        self.priority = 1

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


def plot_shelfs(shelfs):
    for s in shelfs:
        pos = list(s.position)
        plt.plot(pos[0], pos[1], 'rs')


################################################## Driver Code ######################################################


AGVs = []
shelfs = []

shelfPositions = [(75, warehouseHeight - 125 ), (125, warehouseHeight - 125 ), (225, warehouseHeight - 125 ), (275, warehouseHeight - 125 ), (325, warehouseHeight - 125 ), (375, warehouseHeight - 125 ), (425, warehouseHeight - 125 ), (475, warehouseHeight - 125 ), (525, warehouseHeight - 125 ), (575, warehouseHeight - 125 )]
#print(shelfPositions)

startPosx = np.linspace(0 + laneWidth/2, warehouseWidth - laneWidth/2, nbrOfAGVs)
for i in range(len(startPosx)):
    pos = (startPosx[i], warehouseHeight - 75)
    a = AGV(pos, fullyCharged)
    AGVs.append(a)


for i in range(len(shelfPositions)):
    pos = shelfPositions[i]
    s = Shelf(pos, 1)
    shelfs.append(s)


plt.figure(2)
plt.clf()
plot_AGVs(AGVs)
plot_shelfs(shelfs)
plt.show()





