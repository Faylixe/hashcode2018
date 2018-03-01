#!/usr/bin/env python
# coding: utf8

""" """


#pythran export is_valid(str list list,int, int list)
def is_valid(pizza, l, pslice):
    r1, c1, r2, c2 = pslice
    if r2 > len(pizza) or c2 > len(pizza[0]):
        return False
    mushroom = 0
    tomato = 0
    for i in range(r1, r2 + 1):
        for j in range(c1, c2 + 1):
            if pizza[i][j] == 'T':
                tomato += 1
            if pizza[i][j] == 'M':
                mushroom += 1
    return tomato >= l and mushroom >= l


#pythran export overlap(int list, int list)
def overlap(a, b):
    xa1, ya1, xa2, ya2 = a
    xb1, yb1, xb2, yb2 = b
    if ya2 < yb1 or yb2 < ya1:
        return False
    if xa2 < xb1 or xb2 < xa1:
        return False
    return True


#pythran export get_sizes(int, int)
def get_sizes(l, h):
    sizes = []
    areas = [i for i in range(l * 2, h + 1)]
    for area in areas:
        for prime in (1, 2, 3, 5, 7):
            if area % prime == 0:
                s = int(area / prime)
                if (prime, s) not in sizes:
                    sizes.append((prime, s))
                if (s, prime) not in sizes:
                    sizes.append((s, prime))
    return sizes


#pythran export get_candidates(str list list, int list list, int)
def get_candidates(pizza, sizes, l):
    candidates = []
    for size in sizes:
        x = 0
        while x <= len(pizza) - size[0]:
            y = 0
            while y <= len(pizza[0]) - size[1]:
                pslice = (x, y, x + size[0] - 1, y + size[1] - 1)
                if is_valid(pizza, l, pslice):
                    candidates.append(pslice)
                y += 1
            x += 1            
    return candidates


#pythran export get_candidate_score(int list)
def get_candidate_score(candidate):
    r1, c1, r2, c2 = candidate
    w = (r2 - r1) + 1
    h = (c2 - c1) + 1
    return (w * h)


#pythran export solve_greedy_row(int, int, int, int, str list list)
def solve_greedy_row(r, c, l, h, pizza):
    slices = []
    for i in range(r):
        offset, cells, mushroom, tomato = 0, 0, 0, 0
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
