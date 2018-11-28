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
    plt.clf()
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
        




################################################## Driver Code ######################################################


AGVs = []
shelfs = []
shelfPositions = np.array([(75, warehouseHeight - 75 ), (125, warehouseHeight - 75 ), (225, warehouseHeight - 75 ) (275, warehouseHeight - 75 ), (325, warehouseHeight - 75 ) (375, warehouseHeight - 75 ), (425, warehouseHeight - 75 ) (475, warehouseHeight - 75 ), (525, warehouseHeight - 75 ) (575, warehouseHeight - 75 )])

startPosx = np.linspace(0 + laneWidth/2, warehouseWidth - laneWidth/2, nbrOfAGVs)
for i in range(len(startPosx)):
    pos = (startPosx[i], warehouseHeight - 75)
    a = AGV(pos, fullyCharged)
    AGVs.append(a)

plot_AGVs(AGVs)






