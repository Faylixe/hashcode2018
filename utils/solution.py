#!/usr/bin/env python
# coding: utf8

""" Solution evaluation and managment module. """

from getpass import getuser
from os import getcwd, listdir, makedirs
from os.path import exists, isfile, join

from utils.configuration import configuration
from utils.judge import JudgeSite
from utils.score import get_score
from utils.slack import notify

_SOLUTION_DIRECTORY = 'solution'
_CHALLENGER_PATH = 'challenger.score'
_SOLUTION_FILE = '%s-%s-%s.out'
_SCORE_FILE = '%s.score'
_MIN_SCORE = 0


def _get_solution_directory(dataset):
    """ Retrieves a solution directory for the given
    dataset. If such directory does not exist it will be
    then created.

    :param dataset: Dataset to get solution directory for.
    :returns: Solution directory for the given dataset.
    """
    path = join(_SOLUTION_DIRECTORY, dataset)
    if not exists(path):
        makedirs(path)
    return path


def _get_challenger(directory):
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


def _set_challenger(directory, score):
    """ Sets the challenger score for the given directory.

    :param directory: Directory to write challenger in.
    :param score: New challenger score.
    """
    path = join(directory, _CHALLENGER_PATH)
    with open(path, 'r') as stream:
        stream.write(str(score))


def _send_notification(dataset, score, target):
    """ Post a notification of new best score.

    :param dataset: Dataset new challenger arrived for.
    :param score: New best score to defeat.
    :param target: Target solution file.
    """
    lines = [
        'New challenger score for dataset %s : %s' % (dataset, score),
        'Solution file : %s' % target
    ]
    user = getuser()
    message = '\n'.join(lines)
    notify(message, user=user)


def write_solution(dataset, writer, signature='anonymous'):
    """ Writes a solution file for the given dataset
    using the given writer function. Such function only
    takes in parameter a writing stream where solution
    should be written in.

    :param dataset: Dataset to write solution for.
    :param writer: Solution monadic writing function that takes a stream.
    :param signature: (Optional) Algorithm signature to label file with.
    """
    directory = _get_solution_directory(dataset)
    n = len(filter(isfile, listdir(directory)))
    name = _SOLUTION_FILE % (dataset, n, signature)
    target = join(directory, name)
    with open(target, 'w') as stream:
        writer(stream)
    with open(_SCORE_FILE % target, 'w') as stream:
        stream.write(score)
    score = get_score(dataset, target)
    if score > _get_challenger(directory):
        _set_challenger(directory, score)
        _send_notification(dataset, score)
        with JudgeSite(configuration.ROUND) as judge:
            judge.login(
                configuration.GOOGLE_USERNAME,
                configuration.GOOGLE_PASSWORD)
            judge.upload(dataset, join(getcwd, target))
