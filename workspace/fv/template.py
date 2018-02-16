#!/usr/bin/env python
# coding: utf8

""" TODO : Document your approach here. """

from utils.dataset import get_dataset_file
from utils.solution import write_solution

from os.path import exists, join
from sys import argv


def _solve(input):
    """ Solution building function.
    Contains the main algorithm execution.

    :param input: Input file to read instance from.
    :returns: Returns solution built for the given instance.
    """
    with open(input, 'r') as stream:
        # TODO : Read input data from stream.
        pass
    solution = None
    # TODO : Build and return solution
    return solution


def _get_solution_writer(solution):
    """ Builds and returns a writer function for the
    given solution. Such function should take an
    output stream as unique parameter and write solution
    into this stream according to expected format.

    :param solution: Solution to get writer function for.
    """
    def _writer(stream):
        # TODO : Write your solution in the given stream.
        pass
    return _writer


if __name__ == '__main__':
    if len(argv) == 0:
        raise ValueError('Expected dataset parameter not found')
    dataset = argv[0]
    input = get_dataset_file(dataset)
    if not exists(input):
        raise IOError('Cannot find dataset file %s' % input)
    solution = _solve(input)
    writer = _get_solution_writer(solution)
    write_solution(dataset, writer)
