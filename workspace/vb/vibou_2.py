#!/usr/bin/env python
# coding: utf8

""" """
from __future__ import division
from sys import stdout, stderr


from utils.dataset import load_dataset
from utils.utils import distance, ride_start_pos, ride_end_pos, ride_step_range, ride_distance

def costForVehicule(vehicule, ride, step):

    startPos = ride_start_pos(ride)
    distToStart = distance(startPos, vehicule.position)
    ride_start = ride_step_range(ride)[0]
    lbt = vehicule.busyUntil


    return (lbt + distToStart) - ride_start

class Vehicule:
    def __init__(self, id):
        self.posx = 0
        self.posy = 0
        self.nextPosX = 0
        self.nextPosY = 0

        self.busyUntil = 0
        self.isBusy = False

        self.id = id
        self.rides = []


    def updateStep(self, step):
        if self.isBusy and step >= self.busyUntil:
            self.posx = self.nextPosX
            self.posy = self.nextPosY
            self.isBusy = False

    @property
    def position(self):
        return (self.posx, self.posy)

    def canPerformRide(self, ride, step):
        return not self.isBusy

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
        ride_start = ride_step_range(ride)[0]

        self.nextPosX = endPos[0]
        self.nextPosY = endPos[1]

        distToStart = distance(startPos, self.position)

        if (distToStart + self.busyUntil) <= ride_start:
            distToStart = 0

        rideDistance = distance(startPos, endPos)
        totalDistance = distToStart + rideDistance
        self.busyUntil += totalDistance
        self.rides.append(ride[6])
        self.isBusy = True
        # log('Select Vehicule %s. It will be busy until step %s for total distance of %s (rd: %s)' %(self.id, self.busyUntil, totalDistance, rideDistance))


class VehiculePool:

    def __init__(self, numVehicules):
        self.vehicules = []
        for x in range(0, numVehicules):
            self.vehicules.append(Vehicule(x))

    def closest(self, ride, step):
        closest = None

        bestVehicule = None
        bestCost = None
        for vehicule in self.vehicules:
            if vehicule.canPerformRide(ride, step):
                cost = costForVehicule(vehicule, ride, step)
                # log("vehicule %s cost %s" %(vehicule.id, cost))
                if bestCost is None or cost < bestCost:
                    bestCost = cost
                    bestVehicule = vehicule
                    if(bestCost == 0):
                        break

        if bestVehicule is not None:
            # log("select vehicule %s" % (bestVehicule.id))
            return bestVehicule


    def tick(self, step, max_step):
        remaining = (step / max_step) * 100
        log('======= STEP %s / %s (%.2f)========' %(step, max_step, remaining))
        for vehicule in self.vehicules:
            vehicule.updateStep(step)



def log(message):
    """ Debug logging """
    stderr.write('%s\n' % message)

def steps(pool, max_step):
    skipUntil = None
    for step in range(0, max_step):
        if skipUntil is not None and skipUntil < step:
            continue

        all_busy = True
        minNextStep = None
        for vehicule in pool.vehicules:
            if vehicule.isBusy:
                if minNextStep is None:
                    minNextStep = vehicule.busyUntil
                else:
                    minNextStep = min(minNextStep, vehicule.busyUntil)
            else:
                all_busy = False
                break

        if not all_busy:
            yield step
        else:
            skipUntil = minNextStep
            yield minNextStep




def main():
    r, c, f, n, b, t, rides = load_dataset()

    pool = VehiculePool(f)
    normalized = []
    idx = 0
    for ride in rides:
        normalized.append([ride[0], ride[1], ride[2], ride[3], ride[4], ride[5], idx, False])
        idx += 1
    normalized.sort(key=lambda ride:ride[4])

    max_step = 0
    for ride in normalized:
        max_step = max(max_step, ride[5])

    for step in steps(pool, max_step):
        filtered_rides = filter(lambda r: not r[7] and r[4] <= step and r[5] >= step, normalized)
        if len(filtered_rides) == 0 or step < filtered_rides[0][4]:
            continue

        filtered_rides.sort(key=lambda r: ride_distance(r) , reverse=True)
        pool.tick(step, max_step)
        for ride in filtered_rides:
            # log('--- RIDE %s -(%s, %s) %s --' % (ride[6], ride[4], ride[5], ride[7]))
            vehicule = pool.closest(ride, step)
            if vehicule is not None:
                vehicule.performRide(ride)
                ride[7] = True

    for vehicule in pool.vehicules:
        print('%s %s' % (str(len(vehicule.rides)), ' '.join([str(r) for r in vehicule.rides])))

    log('Remaining Rides: %s' %(len(filter(lambda r: not r[7], normalized))))

if __name__ == '__main__':
    main()
