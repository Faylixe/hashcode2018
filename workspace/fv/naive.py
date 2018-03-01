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
    print("1 0")
    for i in range(f - 1):
        print("0")


if __name__ == '__main__':
    main()
