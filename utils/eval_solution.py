#!/usr/bin/env python
# coding: utf8

""" Solution evaluation and managment module. """

from getpass import getuser
from os import getcwd
from os.path import dirname, exists, join
from sys import argv

from utils.configuration import configuration
from utils.judge import JudgeSite
from utils.score import get_score_from_file
from utils.slack import notify

__author__ = 'fv'

_DATASET_PATH = 'dataset'
_CHALLENGER_PATH = 'challenger.score'
_SCORE_FILE = '%s.score'
_MIN_SCORE = 0


def _get_challenger_score(directory):
    """ Reads a challenger file in the given directory if exists.
    Returning minimum score otherwise.

    :param directory: Target directory to read challenger file from.
    :returns: Challenger score as best solution known for this dataset.
    """
    path = join(directory, _CHALLENGER_PATH)
    if not exists(path):
        return _MIN_SCORE
    with open(path, 'r') as stream:
        return int(stream.read())


def _set_challenger_score(directory, score):
    """ Sets the challenger score for the given directory.

    :param directory: Directory to write challenger in.
    :param score: New challenger score.
    """
    path = join(directory, _CHALLENGER_PATH)
    with open(path, 'w') as stream:
        stream.write(str(score))


def _send_notification(dataset, score, target):
    """ Post a notification of new solution file.

    :param dataset: Dataset new challenger arrived for.
    :param score: Associated score.
    :param target: Target solution file.
    """
    lines = [
        'New solution for dataset %s (Score : %s)' % (dataset, score),
        'Solution file : %s' % target
    ]
    user = getuser()
    message = '\n'.join(lines)
    notify(message, user=user)


if __name__ == '__main__':
    """ TODO : Document ."""
    dataset = argv[0]
    solution = argv[1]
    directory = join(_DATASET_PATH, dataset)
    with open(_SCORE_FILE % solution, 'w') as stream:
        stream.write(score)
    score = get_score_from_file(dataset, solution)
    if score > _get_challenger(directory):
        _set_challenger(directory, score)
        # TODO : Write current challenger script into compilation file
    _send_notification(dataset, score)
    with JudgeSite(configuration.ROUND) as judge:
        judge.login(
            configuration.GOOGLE_USERNAME,
            configuration.GOOGLE_PASSWORD)
        judge.upload(dataset, join(getcwd(), solution))
