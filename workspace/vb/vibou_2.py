#!/usr/bin/env python
# coding: utf8

""" """

from sys import stdout, stderr

from utils.dataset import load_dataset
from utils.utils import distance, ride_start_pos, ride_end_pos, ride_step_range

def costForVehicule(vehicule, ride):
    startPos = ride_start_pos(ride)
    distToStart = distance(startPos, vehicule.position)
    ride_start = ride_step_range(ride)[0]
    lbt = vehicule.lastBusyStep


    return (lbt + distToStart) - ride_start

class Vehicule:
    def __init__(self, id):
        self.posx = 0
        self.posy = 0
        self.lastBusyStep = 0

        self.nextPosX = 0
        self.nextPosY = 0
        self.busyUntil = 0
        self.isBusy = False
        self.id = id
        self.rides = []

    def updateStep(self, step):
        if step >= self.busyUntil:
            self.posx = self.nextPosX
            self.posy = self.nextPosY
            self.lastBusyStep = step - 1
            self.isBusy = False

    @property
    def position(self):
        if(self.isBusy):
            return (self.nextPosX, self.nextPosY)

        return (self.posx, self.posy)

    def canPerformRide(self, ride):
        if self.isBusy:
            return False

        return True

        # startPos = ride_start_pos(ride)
        # endPos = ride_end_pos(ride)
        # range = ride_step_range(ride)

        # realStart = max(range[0], self.busyUntil)
        # rideDistance = distance(startPos, endPos)

        # time = realStart - rideDistance
        # return time >= 0



    def performRide(self, ride):
        startPos = ride_start_pos(ride)
        endPos = ride_end_pos(ride)

        self.nextPosX = endPos[0]
        self.nextPosY = endPos[1]

        distToStart = distance(startPos, self.position)
        rideDistance = distance(startPos, endPos)
        totalDistance = distToStart + rideDistance
        self.busyUntil += totalDistance
        self.rides.append(ride[6])
        self.isBusy = True


class VehiculePool:

    def __init__(self, numVehicules):
        self.vehicules = []
        for x in range(0, numVehicules):
            self.vehicules.append(Vehicule(x))

    def closest(self, ride):
        closest = None

        bestVehicule = None
        bestCost = None
        for vehicule in self.vehicules:
            if vehicule.canPerformRide(ride):
                cost = costForVehicule(vehicule, ride)
                log("vehicule %s cost %s" %(vehicule.id, cost))
                if bestCost is None or cost < bestCost:
                    bestVehicule = vehicule

        if bestVehicule is not None:
            log("select vehicule %s" % (bestVehicule.id))
            return bestVehicule


    def tick(self, step):
        log('======= STEP %s ========' %(step))
        for vehicule in self.vehicules:
            vehicule.updateStep(step)





def log(message):
    """ Debug logging """
    stderr.write('%s\n' % message)


def main():
    r, c, f, n, b, t, rides = load_dataset()

    pool = VehiculePool(f)
    normalized = []
    idx = 0
    for ride in rides:
        normalized.append([ride[0], ride[1], ride[2], ride[3], ride[4], ride[5], idx])
        idx += 1
    normalized.sort(key=lambda ride:ride[4])

    step = -1
    for ride in normalized:
        if(ride[4] != step):
            step = ride[4]
            pool.tick(step)

        log('--- Ride ---')
        vehicule = None
        while(vehicule is None):
            vehicule = pool.closest(ride)
            if vehicule is None:
                step += 1
                pool.tick(step)

        if vehicule is not None:
            vehicule.performRide(ride)

    for vehicule in pool.vehicules:
        print('%s %s' % (str(len(vehicule.rides)), ' '.join([str(r) for r in vehicule.rides])))

if __name__ == '__main__':
    main()
