#!/usr/bin/env python
# coding: utf8

""" """

from sys import stdout

from utils.dataset import load_dataset


def main():
    r, c, l, h, pizza = load_dataset()
    slices = []
    for i in range(r):
        offset = 0
        cells = 0
        mushroom = 0
        tomato = 0
        for j in range(c):
            cells += 1
            if pizza[i][j] == 'T':
                tomato += 1
            elif pizza[i][j] == 'M':
                mushroom += 1
            if mushroom >= l and tomato >= l:
                slices.append((i, offset, i, j))
                offset, tomato, mushroom, cells = j + 1, 0, 0, 0
            if cells == h:
                offset, tomato, mushroom, cells = j + 1, 0, 0, 0
    print(len(slices))
    for pslice in slices:
        print('%d %d %d %d' % pslice)

if __name__ == '__main__':
    main()
