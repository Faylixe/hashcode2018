#!/usr/bin/env python
# coding: utf8

""" """

from sys import stdout

from utils.dataset import load_dataset


def main():
    dataset = load_dataset()
    stdout.write('3\n0 0 2 1\n0 2 2 2\n0 3 2 4')


if __name__ == '__main__':
    main()
