#!/usr/bin/env python
# coding: utf-8

""" This modules exposes a singleton for configuration values. """

from os import getenv

__author__ = 'fv'


class _Configuration(object):
    """ Configuration parameter namespace."""

    SELENIUM_DRIVER = getenv('SELENIUM_DRIVER', 'silent')
    SLACK_WEBHOOK = getenv('SLACK_WEBHOOK')
    GOOGLE_USERNAME = getenv('GOOGLE_USERNAME')
    GOOGLE_PASSWORD = getenv('GOOGLE_PASSWORD')
    ROUND = getenv('ROUND')
    DATASET_PATH = getenv('DATASET_PATH', 'dataset')
    SOLUTION_PATH = getenv('SOLUTION_PATH', 'solution')

configuration = _Configuration()
