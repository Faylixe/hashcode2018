#!/usr/bin/env python
# coding: utf8

""" Dataset parsing functions. """

from os.path import join

_DATASET_DIRECTORY = 'dataset'


def get_dataset_file(dataset):
    """ Retrieves the input file associated to the given dataset.

    :param dataset: Dataset to get input file for.
    :returns: Path of the input file for the given dataset.
    """
    return join(_DATASET_DIRECTORY, dataset)
