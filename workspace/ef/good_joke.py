#!/usr/bin/env python
# coding: utf8

""" """

from sys import stdout, stderr

from utils.dataset import load_dataset
from utils.utils import distance

def log(message):
    """ Debug logging """
    stderr.write('%s\n' % message)

class Ride:
    def __init__(self, ride_id, ride_array):
        a, b, x, y, s, u = ride_array
        self.id = ride_id
        self.start_pos = (a, b)
        self.end_pos = (x, y)
        self.early_start = s
        self.latest_end = u
        self.done = False

class Vehicule:
    def __init__(self, id, bonus, steps):
        self.id = id
        self.pos = (0, 0)
        self.remaining_steps = steps
        self.done_rides = []
        self.bonus = bonus
        self.current_gain = 0

    def possible(self, ride):
        time_to_go = distance(self.pos, ride.start_pos)
        true_start = time_to_go + (ride.early_start - time_to_go)
        true_end = true_start + distance(ride.start_pos, ride.end_pos)
        if true_start >= ride.early_start and true_end <= ride.latest_end and (self.remaining_steps - true_end) >= 0:
            return self.gain(ride, true_start)
        else:
            return -1

    def gain(self, ride, true_start):
        g = self.current_gain + distance(ride.start_pos, ride.end_pos)
        if true_start == ride.start_pos:
            g += self.bonus
        return g

    def do(self, ride):
        if self.possible(ride) >= 0:
            time_to_go = distance(self.pos, ride.start_pos)
            true_start = time_to_go + (ride.early_start - time_to_go)
            true_end = true_start + distance(ride.start_pos, ride.end_pos)
            self.pos = ride.end_pos 
            self.remaining_steps -= true_end
            self.done_rides.append(ride.id)
            self.current_gain = self.gain(ride, true_start)
            ride.done = True


def main():
    r, c, f, n, b, t, rides = load_dataset()
    vehicules = []
    for vehicule_id in range(f):
        vehicules.append(Vehicule(vehicule_id, b, t))
    rides_new = []
    for ride_id, ride_array in enumerate(rides):
        rides_new.append(Ride(ride_id, ride_array))

    rides_new = sorted(rides_new, key=lambda r: distance(r.start_pos, r.end_pos), reverse=False)

    for ride in rides_new:
        candidates = []
        for vehicule in vehicules:
            score = vehicule.possible(ride)
            if score >= 0:
                candidates.append((vehicule, score))
        if len(candidates) > 0:
            candidates = sorted(candidates, key=lambda c: c[1], reverse=True)
            top = candidates[0]
            top[0].do(ride)

    for vehicule in vehicules:
        N = len(vehicule.done_rides)
        if N == 0:
            print("0")
        else:
            print("{} {}".format(N, " ".join([ str(r_id) for r_id in vehicule.done_rides])))


if __name__ == '__main__':
    main()
