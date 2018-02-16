#!/usr/bin/env python
# coding: utf8

"""
    run workspace_owner dataset_name
"""

from os.path import exists, join
from sys import argv

_DATASET_DIRECTORY = 'dataset'
_WORKSPACE_DIRECTORY = 'workspace'


def _is_workspace_valid(workspace):
    """ Predicates that check if the given workspace exists.

    :param workspace: Workspace to check validity for.
    :returns: True if the given workspace exists, False otherwise.
    """
    return exists(join(_WORKSPACE_DIRECTORY, workspace))


def _is_dataset_valid(workspace):
    """ Predicates that check if the given workspace exists.

    :param workspace: Workspace to check validity for.
    :returns: True if the given workspace exists, False otherwise.
    """
    return exists(join(_DATASET_DIRECTORY, workspace))


if __name__ == '__main__':
    if len(argv) < 2:
        pass
    workspace = argv[0]
    if not _is_workspace_valid(workspace):
        pass
    dataset = argv[1]
    if not _is_dataset_valid(dataset):
        pass
    # TODO : Import workspace.
    # TODO : Run over dataset.