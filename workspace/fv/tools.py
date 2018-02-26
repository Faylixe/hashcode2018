#!/usr/bin/env python
# coding: utf8

""" """


#pythran export is_valid(str list list,int, int list, bool list list)
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
    while x <= len(pizza) - size[0]:
        y = 0
        while y <= len(pizza[0]) - size[1]:
            pslice = (x, y, x + size[0] - 1, y + size[1] - 1)
            if is_valid(pizza, l, pslice, available):
                yield pslice
            y += 1
        x += 1


#pythran export overlap(int list, int list)
def overlap(a, b):
    xa1, ya1, xa2, ya2 = a
    xb1, yb1, xb2, yb2 = b
    if ya2 < yb1 or yb2 < ya1:
        return False
    if xa2 < xb1 or xb2 < xa1:
        return False
    return True


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


#pythran export get_candidates(int list list, int list list, int, bool list list)
def get_candidates(pizza, sizes, l, available=None):
    candidates = []
    for size in sizes:
        for s in cut(pizza, size, l, available):
            candidates.append(s)
    return candidates


#pythran export is_available(bool list list, int list)
def is_available(available, candidate):
    for x in range(candidate[0], candidate[2] + 1):
        for y in range(candidate[1], candidate[3] + 1):
            if not available[x][y]:
                return False
    return True


def solve_randomly(pizza, sizes, l):
    candidates = get_candidates(pizza, sizes, l)
    stderr.write('%d candidates found\n' % len(candidates))
    solution = []
    available = [[True] * len(pizza[0])] * len(pizza)
    shuffle(candidates)
    for candidate in candidates:
        if is_available(available, candidate):
            solution.append(candidate)
            for x in range(candidate[0], candidate[2] + 1):
                for y in range(candidate[1], candidate[3] + 1):
                    available[x][y] = False
    return solution, available


def log_solution(solution):
    stderr.write('%s\n' % str(solution))


def log_available(available):
    for row in available:
        stderr.write('%s\n' % str(row))


def get_candidate_score(candidate):
    r1, c1, r2, c2 = candidate
    w = (r2 - r1) + 1
    h = (c2 - c1) + 1
    return (w * h)


def set_available(available, candidate, status):
    for x in range(candidate[0], candidate[2] + 1):
        for y in range(candidate[1], candidate[3] + 1):
            available[x][y] = status


def solve_greedy_row(r, c, l, h, pizza):
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
    available = [[True] * c for i in range(r)]
    for candidate in slices:
        set_available(available, candidate, False)
    return slices, available


def main():
    r, c, l, h, pizza = load_dataset()
    stderr.write('Problem constraints : r=%d, c=%d, l=%d, h=%d\n' % (r, c, l, h))
    sizes = get_sizes(l, h)
    stderr.write('Sizes : %s\n' % str(sizes))
    stderr.write('Compute initial solution\n')
    solution, available = solve_greedy_row(r, c, l, h, pizza) # solve_randomly(pizza, sizes, l)
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

