#!/usr/bin/env python
# coding: utf8

""" Solution scoring functions. """

from utils.dataset import DatasetReader
from utils.dataset import load_dataset_from_file

__author__ = 'fv'


def load_solution_from_file(path):
    """ Load and returns solution from given path.

    :param path: Path of the solution file to load.
    """
    with open(path, 'r') as stream:
        reader = DatasetReader(stream)
        rides = []
        while True:
            try:
                rides.append(reader.next_ints())
            except ValueError:
                break
        return rides


def get_score_from_file(dataset_path, solution_path):
    """ Computes the expeceted score for the given
    problem dataset / solution files pair.

    :param dataset: Dataset to get solution score for.
    :param solution_path: Path of the solution to get score for.
    :returns: Score of the given solution.
    """
    solution = load_solution_from_file(solution_path)
    dataset = load_dataset_from_file(dataset_path)
    return get_score(dataset, solution)


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
            print
            if step <= re:
                score += spent
    return score