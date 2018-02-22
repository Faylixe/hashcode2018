#!/usr/bin/env python
# coding: utf8

""" """

from sys import stdout

from utils.dataset import load_dataset
from utils.score import get_score


def get_row_slices(r, c, l, h, pizza):
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
    return slices


def get_col_slices(r, c, l, h, pizza):
    slices = []
    for j in range(c):
        offset = 0
        cells = 0
        mushroom = 0
        tomato = 0
        for i in range(r):
            cells += 1
            if pizza[i][j] == 'T':
                tomato += 1
            elif pizza[i][j] == 'M':
                mushroom += 1
            if mushroom >= l and tomato >= l:
                slices.append((offset, j, i, j))
                offset, tomato, mushroom, cells = i + 1, 0, 0, 0
            if cells == h:
                offset, tomato, mushroom, cells = i + 1, 0, 0, 0
    return slices


def main():
    r, c, l, h, pizza = load_dataset()
    row_slices = get_row_slices(r, c, l, h, pizza)
    col_slices = get_col_slices(r, c, l, h, pizza)
    row_score = get_score((r, c, l, h, pizza), (len(row_slices), row_slices))
    col_score = get_score((r, c, l, h, pizza), (len(col_slices), col_slices))
    slices = col_slices
    if row_score > col_score:
        slices = row_slices
    print(len(slices))
    for pslice in slices:
        print('%d %d %d %d' % pslice)

if __name__ == '__main__':
    main()
