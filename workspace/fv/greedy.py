#!/usr/bin/env python
# coding: utf8

""" """

from sys import stdout, stderr

from utils.dataset import load_dataset


def log(message):
    """ Debug logging """
    stderr.write('%s\n' % message)


def main():
    r, c, f, n, b, t, rides = load_dataset()
    idx = 0
    normalized = []
    for ride in rides:
        normalized.append([idx, ride[0], ride[1], ride[2], ride[3], ride[4], ride[5]])
        idx += 1
    normalized.sort(key=lambda ride:ride[5])
    vehicles = [0] * f
    solution = []
    for i in range(f):
        solution.append([])
    current = 0
    for ride in normalized:
        i, ra, rb, rx, ry, rs, re = ride
        candidate = vehicles.index(min(vehicles))
        # TODO : Check if feasible.
        solution[candidate].append(i)
        if vehicles[candidate] < rs:
            vehicles[candidate] = rs
        vehicles[candidate] += abs(ra - rx) + abs(rb - ry)
    for ride in solution:
        print('%s %s' % (str(len(ride)), ' '.join([str(r) for r in ride])))


if __name__ == '__main__':
    main()
