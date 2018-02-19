#!/usr/bin/env python
# coding: utf8

""" TODO : Document. """

from utils.dataset import DatasetReader


def main():
    """ Place your algorithm here. """
    reader = DatasetReader()
    # 3 ints on the same line.
    a, b, c = reader.next_ints()
    # 1 int on the line only.
    n = reader.next_int()
    # Read the next line as a string.
    s = reader.next_line()
    # Read the next line as a map row
    # returned as a list of char, not string
    r = reader.next_row()
    r[0] = 'X'

if __name__ == '__main__':
    main()
