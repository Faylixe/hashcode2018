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
            print('RARA')
            if step <= re:
                score += spent
    return score


def solve_greedy(dataset):
    r, c, f, n, b, t, rides = dataset
    idx = 0
    normalized = []
    for ride in rides:
        normalized.append([idx, ride[0], ride[1], ride[2], ride[3], ride[4], ride[5]])
        idx += 1
    normalized.sort(key=lambda ride:ride[5])
    vehicles = [0] * f
    solution = []
    for i in range(f):
        solution.append([])
    current = 0
    for ride in normalized:
        i, ra, rb, rx, ry, rs, re = ride
        candidate = vehicles.index(min(vehicles))
        # TODO : Check if feasible.
        solution[candidate].append(i)
        if vehicles[candidate] < rs:
            vehicles[candidate] = rs
        vehicles[candidate] += abs(ra - rx) + abs(rb - ry)
    return solution


def main():
    dataset = load_dataset()
    r, c, f, n, b, t, rides = dataset
    solution = solve_greedy(dataset)
    score = get_score(dataset, solution)
    print('Final Score : %s' % score)

if __name__ == '__main__':
    main()
