#!/usr/bin/env python
# coding: utf8

""" """

from sys import stdout, stderr

from utils.dataset import load_dataset
from utils.utils import distance, ride_start_pos, ride_end_pos, ride_step_range

def costForVehicule(vehicule, ride):
    startPos = ride_start_pos(ride)
    endPos = ride_end_pos(ride)
    distToStart = distance(startPos, vehicule.position)
    rideDistance = distance(startPos, endPos)

    return distToStart + rideDistance

class Vehicule:
    def __init__(id):
        self.posx = 0
        self.posy = 0

        self.nextPosX = None
        self.nextPosY = None
        self.busyUntil = 0
        self.id = id
        self.rides = []

    @property
    def position():
        return (self.posx, self.posy)

    def canPerformRide(ride):
        if self.nextPosX is None:
            return True

        startPos = ride_start_pos(ride)
        endPos = ride_end_pos(ride)

        realStart = max(startPos, self.busyUntil)
        rideDistance = distance(startPos, endPos)

        time = realStart - rideDistance
        return time >= 0



    def performRide(ride):
        startPos = ride_start_pos(ride)
        endPos = ride_end_pos(ride)
        self.nextPosX = endPos[0]
        self.nextPosY = endPos[1]
        distToStart = distance(startPos, self.position)
        rideDistance = distance(startPos, endPos)

        self.busyUntil += distToStart + rideDistance
        self.rides.append(ride[6])


class VehiculePool:

    def __init__(numVehicules):
        self.vehicules = []
        for x in range(0, numVehicules):
            self.vehicules.append(Vehicule(x))

    def closest(ride):
        closest = None

        bestVehicule = None
        bestCost = None
        for vehicule in self.vehicules:
            if vehicule.canPerformRide(ride):
                cost = costForVehicule(vehicule, ride)
                if bestCost is None || cost < bestCost:
                    bestVehicule = vehicule
                    break

        if bestVehicule is not None:
            return bestVehicule







def log(message):
    """ Debug logging """
    stderr.write('%s\n' % message)


def main():
    r, c, f, n, b, t, rides = load_dataset()

    pool = VehiculePool(f)
    normalized = []
    for ride in rides:
        normalized.append([ride[0], ride[1], ride[2], ride[3], ride[4], ride[5], idx])
        idx += 1
    normalized.sort(key=lambda ride:ride[4])

    for ride in normalized:
        vehicule = pool.closest(ride)
        vehicule.performRide(ride)

    for vehicule in pool.vehicules:
        print('%s %s' % (str(len(vehicule.rides)), ' '.join([str(r) for r in vehicule.rides])))

if __name__ == '__main__':
    main()
