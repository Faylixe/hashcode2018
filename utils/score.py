#!/usr/bin/env python
# coding: utf8

""" Solution scoring functions. """

__author__ = 'fv'


def load_solution(path):
    """ Load and returns solution from given path.

    :param path: Path of the solution file to load.
    """
    if not exists(path):
        raise IOError('Solution file %s not found' % path)
    with open(path, 'r') as stream:
        raise NotImplementedError()


def get_score_from_file(dataset, solution_path):
    """ Computes the expeceted score for the given
    problem dataset / solution files pair.

    :param dataset: Dataset to get solution score for.
    :param solution_path: Path of the solution to get score for.
    :returns: Score of the given solution.
    """
    solution = load_solution(solution_path)
    return get_score(dataset, solution)


def get_score(dataset, solution):
    """ Computes the expeceted score for the given
    problem instance / solution pair.

    :param dataset: Problem instance.
    :param path: Solution to get score for.
    :returns: Score of the given solution.
    """
    raise NotImplementedError()
