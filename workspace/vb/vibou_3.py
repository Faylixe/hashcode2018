#!/usr/bin/env python
# coding: utf8

""" """

from sys import stdout, stderr

from utils.dataset import load_dataset
from utils.utils import distance, ride_start_pos, ride_end_pos, ride_step_range


def log(message):
    """ Debug logging """
    stderr.write('%s\n' % message)


def main():
    r, c, f, n, b, t, rides = load_dataset()

    for v in range(0, f):





if __name__ == '__main__':
    main()
