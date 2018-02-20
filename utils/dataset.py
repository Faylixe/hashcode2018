#!/usr/bin/env python
# coding: utf8

""" Utility functions for reading standard input. """

from sys import stdin

__author__ = 'fv'


class DatasetReader(object):
    """ Utility class for fast input reading.
    
    WARNING
    ~~~~~~~

    Use DatasetReader class for reading standard input which ensure fastest
    input reading. And use sys.stdout.write() instead of print() for fastest
    standard output writing.

    @see https://algocoding.wordpress.com/2015/04/23/fast-io-methods-for-competitive-programming/

    EXEMPLE
    ~~~~~~~

    reader = DatasetReader()        
    a, b, c = reader.next_ints()    # 3 ints on the same line.
    n = reader.next_int()           # 1 int on the line only.
    s = reader.next_line()          # Read the next line as a string.
    r = reader.next_row()           # Read the next line as a map row
    stdout.write('BLABLA')          # FASTER THAN PRINT !
    """

    def __init__(self, stream=stdin):
        """ Default constructor. Read the whole standard input. """
        self._lines = [line.rstrip() for line in stream]

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


def load_dataset(stream=stdin):
    """ Loads the dataset from the standard input.

    :returns: Dataset instance in a generic format.
    """
    reader = DatasetReader(stream)
    raise NotImplementedError()
