#!/usr/bin/env python
# coding: utf8

""" """

from sys import stdout, stderr, stdin


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


def load_dataset_from_file(path):
    """ Loads the dataset from the given file.

    :returns: Dataset file path.
    """
    with open(path, 'r') as stream:
        return load_dataset(stream)


def load_dataset(stream=stdin):
    """ Loads the dataset from the standard input.

    :returns: Dataset instance in a generic format.
    """
    reader = DatasetReader(stream)
    r, c, f, n, b, t = reader.next_ints()
    rides = []
    for i in range(n):
        a, b, x, y, s, u = reader.next_ints()
        rides.append((a, b, x, y, s, u))
    return r, c, f, n, b, t, rides


def log(message):
    """ Debug logging """
    stderr.write('%s\n' % message)

def get_score(dataset, solution):
    """ Computes the expeceted score for the given
    problem instance / solution pair.

    :param dataset: Problem instance.
    :param path: Solution to get score for.
    :returns: Score of the given solution.
    """
    r, c, f, n, b, t, R = dataset
    score = 0
    for vehicle in solution:
        step = 0
        rides = [vehicle[i] for i in range(1, len(vehicle))]
        for ride in rides:
            if step >= t:
                break
            ra, rb, rx, ry, rs, re = R[ride]

            if rs >= step:
                step = rs
                score += b
            spent = abs(ra - rx) + abs(rb - ry)
            step += spent
            if step < re:
                score += spent
    return score

class Vehicle:
    def __init__(self, i):
        self.i = i
        self.x = 0
        self.y = 0
        self.s = 0
        self.r = []

def solve_greedy(dataset):
    r, c, f, n, b, t, rides = dataset
    idx = 0
    normalized = []
    for ride in rides:
        normalized.append([idx, ride[0], ride[1], ride[2], ride[3], ride[4], ride[5]])
        idx += 1
    normalized.sort(key=lambda ride:ride[5])
    vehicles = []
    for i in range(f):
        vehicles.append(Vehicle(i))
    solution = []
    for i in range(f):
        solution.append([])
    current = 0
    for ride in normalized:
        i, ra, rb, rx, ry, rs, re = ride
        spent = abs(ra - rx) + abs(rb - ry)
        candidate = sorted(vehicles, key=lambda v: v.s + abs(v.x - ra) + abs(v.y - rb))[0]
        if candidate.s + spent <= re:
            solution[candidate.i].append(i)
            if candidate.s < rs:
                candidate.s= rs
            candidate.s += spent
    return solution


def closest(p, r, v, n):
    best = -1
    best_d = 100000000000000000
    for i in range(n):
        if not v[i]:
            ra, rb, rx, ry, rs, re = r[i]
            d = abs(p[0] - ra) + abs(p[1] - rb)
            if d < best_d:
                best_d = d
                best = i
    return best


def main():
    dataset = load_dataset()
    r, c, f, n, b, t, rides = dataset
    visited = [False] * n    
    for i in range(f):
        subsolution = []
        step = 0
        pos = (0, 0)
        while step <= t:
            current = closest(pos, rides, visited, n)
            if current == -1:
                break
            subsolution.append(current)
            visited[current] = True
            step += abs(pos[0] - rides[current][0]) + abs(pos[1] - rides[current][1])
            if step < rides[current][4]:
                step = rides[current][4]
            pos = (rides[current][2], rides[current][3])
            step += abs(rides[current][0] - rides[current][2]) + abs(rides[current][1] - rides[current][3])
        print('%s %s' % (str(len(subsolution)), ' '.join([str(r) for r in subsolution])))
    #for ride in solution:
    #    print('%s %s' % (str(len(ride)), ' '.join([str(r) for r in ride])))

if __name__ == '__main__':
    main()
