#!/usr/bin/env python
# coding: utf8

""" """

from sys import stdout, stderr
from itertools import permutations
from random import choice

from utils.dataset import load_dataset
from utils.score import get_score


def is_valid(pizza, l, pslice, available):
    r1, c1, r2, c2 = pslice
    if r2 > len(pizza) or c2 > len(pizza[0]):
        return False
    mushroom = 0
    tomato = 0
    for i in range(r1, r2 + 1):
        for j in range(c1, c2 + 1):
            if available is not None and not available[i][j]:
                return False
            if pizza[i][j] == 'T':
                tomato += 1
            if pizza[i][j] == 'M':
                mushroom += 1
    return tomato >= l and mushroom >= l


def cut(pizza, size, l, available):
    x = 0
    while x < len(pizza) - size[0]:
        y = 0
        while y < len(pizza[0]) - size[1]:
            pslice = (x, y, x + size[0] - 1, y + size[1] - 1)
            if is_valid(pizza, l, pslice, available):
                yield pslice
            y += 1
        x += 1


def overlap(a, b):
    acells = [(x, y) for x in range(a[0], a[2] + 1) for y in range(a[1], a[3] + 1)]
    bcells = [(x, y) for x in range(b[0], b[2] + 1) for y in range(b[1], b[3] + 1)]
    for cell in acells:
        if cell in bcells:
            return True
    return False


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


def get_candidates(pizza, sizes, l, available=None):
    candidates = []
    for size in sizes:
        stderr.write('Generate candidate for size %sx%s\n' % size)
        for s in cut(pizza, size, l, available):
            candidates.append(s)
    return candidates


def solve_randomly(pizza, sizes, l):
    candidates = get_candidates(pizza, sizes, l)
    stderr.write('%d candidates found\n' % len(candidates))
    solution = []
    while len(candidates) > 0:
        candidate = choice(candidates)
        candidates.remove(candidate)
        valid = True
        for choosen in solution:
            if overlap(choosen, candidate):
                valid = False
                break
        if valid:
            solution.append(candidate)
    return solution


def get_candidate_score(candidate):
    r1, c1, r2, c2 = candidate
    w = (r2 - r1) + 1
    h = (c2 - c1) + 1
    return (w * h)


def main():
    r, c, l, h, pizza = load_dataset()
    stderr.write('Problem constraints : r=%d, c=%d, l=%d, h=%d\n' % (r, c, l, h))
    sizes = get_sizes(l, h)
    stderr.write('Sizes : %s\n' % str(sizes))
    stderr.write('Compute initial solution\n')
    solution = solve_randomly(pizza, sizes, l)
    available = [[True] * c] * r
    for candidate in solution:
        for x in range(candidate[0], candidate[2]):
            for y in range(candidate[1], candidate[3]):
                available[x][y] = False
    stderr.write('Start exploration\n')
    improved = True
    while False:
        improved = False
        for candidate in solution:
            removed_weight = get_candidate_score(candidate)
            for x in range(candidate[0], candidate[2]):
                for y in range(candidate[1], candidate[3]):
                    available[x][y] = True
            candidates = get_candidates(pizza, sizes, l, available)
            candidates.remove(candidate)
            if len(candidates) != 0:
                for replacement in candidates:
                    if get_candidate_score(replacement) > removed_weight:
                        for x in range(replacement[0], replacement[2]):
                            for y in range(replacement[1], replacement[3]):
                                available[x][y] = False
                        improved = True
                        stderr.write('Find new slice remplacement (%d -> %d)\n' % (removed_weight, get_candidate_score(replacement)))
                        break
            if not improved:
                for x in range(candidate[0], candidate[2]):
                    for y in range(candidate[1], candidate[3]):
                        available[x][y] = False
            else:
                break
        if improved:
            candidates = get_candidates(pizza, sizes, l, available)
            while len(candidates) > 0:
                candidate = choice(candidates)
                candidates.remove(candidate)
                for x in range(candidate[0], candidate[2]):
                    for y in range(candidate[1], candidate[3]):
                        available[x][y] = False
                candidates = get_candidates(pizza, sizes, l, available)
            stderr.write('New score : %s\n' % get_score((r, c, l, h, pizza), (len(solution), solution)))
    print(len(solution))
    for pslice in solution:
        print('%d %d %d %d' % pslice)

if __name__ == '__main__':
    main()
