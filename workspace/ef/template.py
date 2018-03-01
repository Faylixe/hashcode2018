#!/usr/bin/env python
# coding: utf8

""" """

from sys import stdout, stderr

from utils.dataset import load_dataset


def log(message):
    """ Debug logging """
    stderr.write('%s\n' % message)


def main():
    dataset = load_dataset()
    # TODO : solve problem, write to stdout.


if __name__ == '__main__':
    main()
