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
    solution = []
    for i in range(f):
        solution.append([])
    current = 0
    for ride in normalized:
        solution[current].append(ride[0])
        current += 1
        if current == f:
            current = 0
    for ride in solution:
        print('%s %s' % (str(len(ride)), ' '.join([str(r) for r in ride])))


if __name__ == '__main__':
    main()
