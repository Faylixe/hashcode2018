#!/usr/bin/env python
# coding: utf8

""" """

from sys import stdout
from itertools import permutations

from utils.dataset import load_dataset
from utils.score import get_score


def is_valid(pizza, l, state, pslice):
    r1, c1, r2, c2 = pslice
    if r2 > len(state) or c2 > len(state[0]):
        return False
    mushroom = 0
    tomato = 0
    for i in range(r1, r2):
        for j in range(c1, c2):
            if not state[i][j]:
                return False
            if pizza[i][j] == 'T':
                tomato += 1
            if pizza[i][j] == 'M':
                mushroom += 1
    return tomato >= l and mushroom >= l


def cut(r, c, l, size, state, pizza):
    i = 0
    j = 0
    while i < r:
        row_used = False
        while j < c:
            pslice = (i, j, i + size[0], j + size[1])
            if is_valid(pizza, l, state, pslice):
                yield pslice
                row_used = True
                j += size[1]
            else:
                j += 1
        if row_used:
            i += size[0]
        else:
            i += 1


def get_slices(r, c, l, h, pizza, size, state):
    slices = []
    for pslice in cut(r, c, l, size, state, pizza):
        slices.append(pslice)
        r1, c1, r2, c2 = pslice
        for i in range(r1, r2):
            for j in range(c1, c2):
                state[i][j] = False
    return slices


def main():
    r, c, l, h, pizza = load_dataset()
    sizes = ((4, 3), (3, 4), (2, 7), (7, 2), (1, 14), (14, 1), (2, 6), (6, 2), (1, 12), (12, 1))
    best_score = 0
    best_slices = None
    for ordered in permutations(sizes):
        state = [[True] * c] * r
        slices = []
        for size in ordered:
            for pslice in get_slices(r, c, l, h, pizza, size, state):
                slices.append(pslice)
        score = get_score((r, c, l, h, pizza), (len(slices), slices))
        if score > best_score:
            best_score = score
            best_slices = slices
    print(len(best_slices))
    for pslice in best_slices:
        print('%d %d %d %d' % pslice)

if __name__ == '__main__':
    main()
