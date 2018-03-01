#!/usr/bin/env python
# coding: utf8

""" """

from sys import stdout, stderr
from itertools import permutations
from random import choice, shuffle

from utils.dataset import load_dataset
from utils.score import get_score

from workspace.fv import tools


def is_available(available, candidate):
    for x in range(candidate[0], candidate[2] + 1):
        for y in range(candidate[1], candidate[3] + 1):
            if not available[x][y]:
                return False
    return True


def set_available(available, candidate, status):
    for x in range(candidate[0], candidate[2] + 1):
        for y in range(candidate[1], candidate[3] + 1):
            available[x][y] = status


def main():
    r, c, l, h, pizza = load_dataset()
    stderr.write('Problem constraints : r=%d, c=%d, l=%d, h=%d\n' % (r, c, l, h))
    sizes = tools.get_sizes(l, h)
    stderr.write('Sizes : %s\n' % str(sizes))
    stderr.write('Compute initial solution\n')
    solution = tools.solve_greedy_row(r, c, l, h, pizza)

def main_old():
    r, c, l, h, pizza = load_dataset()
    stderr.write('Start exploration\n')
    improved = True
    while improved:
        stderr.write('\tStart neighboorhood exploration iteration\n')
        improved = False
        best_score = get_score((r, c, l, h, pizza), (len(solution), solution))
        best_neighboor = None
        best_added = []
        best_removed = None
        for candidate in solution:
            new_solution = [s for s in solution]
            new_solution.remove(candidate)
            set_available(available, candidate, True)
            candidates = get_candidates(pizza, sizes, l, available)
            candidates.remove(candidate)
            replaced = []
            shuffle(candidates)
            for replacement in candidates:
                if is_available(available, replacement):
                    replaced.append(replacement)
                    new_solution.append(replacement)
                    set_available(available, replacement, False)
            score = get_score((r, c, l, h, pizza), (len(new_solution), new_solution))
            if score > best_score:
                stderr.write('\tFind local neighboorhood solution optimization (%d -> %d)\n' % (best_score, score))
                best_score = score
                best_neighboor = new_solution
                best_removed = candidate
                best_added = [a for a in replaced]
            for replacement in replaced:
                set_available(available, replacement, True)
            set_available(available, candidate, False)
        if best_neighboor is not None:
            solution = best_neighboor
            set_available(available, best_removed, True)
            for replacement in best_added:
                set_available(available, replacement, False)
            improved = True
    print(len(solution))
    for pslice in solution:
        print('%d %d %d %d' % pslice)
    stderr.write('Score : %d\n' % get_score((r, c, l, h, pizza), (len(solution), solution)))

if __name__ == '__main__':
    main()
