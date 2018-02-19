#!/usr/bin/env python
# coding: utf8

"""
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

from sys import stdout

from utils.dataset import load_dataset


def main():
    dataset = load_dataset()
    # TODO : solve problem, write to stdout.


if __name__ == '__main__':
    main()
