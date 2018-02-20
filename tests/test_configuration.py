#!/usr/bin/env python
# coding: utf-8

""" Test utils.configuration """

from utils.configuration import configuration

__author__ = 'fv'


def test_configuration():
    """ Test configuration attribute. """
    assert configuration.SELENIUM_DRIVER == 'silent'
    assert configuration.GOOGLE_USERNAME == 'foo@gmail.com'
    assert configuration.GOOGLE_PASSWORD == 'bar'
    assert configuration.SLACK_WEBHOOK == 'http://localhost:6969'
    assert configuration.ROUND == '1'
    assert configuration.DATASET_PATH == '/tmp/dataset'
    assert configuration.SOLUTION_PATH == '/tmp'
