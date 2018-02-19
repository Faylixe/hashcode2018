#!/usr/bin/env python
# coding: utf8

""" Utility functions for reading standard input. """

from sys import stdin


class DatasetReader(object):
    """ Utility class for fast input reading. """

    def __init__(self):
        """ Default constructor. Read the whole standard input. """
        self._lines = stdin.readlines()

    def next_int(self):
        """ Returns the next line as a single int. """
        return self.next_ints()[0]

    def next_ints(self):
        """ Returns the next line as integer list. """
        if len(self._lines) == 0:
            raise ValueError()
        return [int(x) for x in self._lines.pop(0).split()]

    def next_line(self):
        """ Returns the next line as a string. """
        if len(self._lines) == 0:
            raise ValueError()
        return self._lines.pop(0)

    def next_row(self):
        """ Returns the next line as a map row. """
        if len(self._lines) == 0:
            raise ValueError()
        return [c for c in self._lines.pop(0)]
