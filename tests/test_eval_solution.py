#!/usr/bin/env python
# coding: utf8

""" """

from os import remove

from utils.eval_solution import _get_challenger
from utils.eval_solution import _set_challenger
from utils.eval_solution import _send_notification


def test_get_challenger_not_exist():
    """ Test non existing challenger. """
    score = _get_challenger('not_existing_path')
    assert score == 0


def test_get_challenger():
    """ Test challenger getter. """
    with open('/tmp/challenger.score', 'w') as stream:
        stream.write('69')
    score = _get_challenger('/tmp')
    assert score == 69
    remove('/tmp/challenger.score')


def test_set_challenger():
    """ Test challenger setter. """
    _set_challenger('/tmp', 42)
    with open('/tmp/challenger.score', 'r') as stream:
        assert int(stream.read()) == 42


def test_send_notification(slack_holder):
    """ Test notification sending. """
    pass

