#!/usr/bin/env python
# coding: utf8

""" Tests utils.eval_solution. """

from getpass import getuser
from json import loads
from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile

from utils.eval_solution import _get_challenger_score
from utils.eval_solution import _set_challenger_score
from utils.eval_solution import _send_notification
from utils.eval_solution import evaluate

__author__ = 'fv'


def test_get_challenger_score_not_exist():
    """ Test non existing challenger. """
    score = _get_challenger_score('not_existing_path')
    assert score == 0


def test_get_challenger_score():
    """ Test challenger getter. """
    with open('/tmp/challenger.score', 'w') as stream:
        stream.write('69')
    score = _get_challenger_score('/tmp')
    assert score == 69
    remove('/tmp/challenger.score')


def test_set_challenger_score():
    """ Test challenger setter. """
    _set_challenger_score('/tmp', 42)
    with open('/tmp/challenger.score', 'r') as stream:
        assert int(stream.read()) == 42
    remove('/tmp/challenger.score')


def _verify_payload(payload, expected):
    """ Check the given slack payload. """
    assert payload is not None
    decoded = loads(payload.decode('utf-8'))
    assert decoded['attachments'][0]['text'] == expected


def test_send_notification(slack_holder):
    """ Test notification sending. """
    _send_notification('testset', 69, 'best_solution_ever.txt')
    expected = 'New solution for dataset testset (Score : 69)\n'
    expected += 'Solution file : best_solution_ever.txt'
    _verify_payload(slack_holder.payload, expected)


class _MockJudge(object):
    """ Simple mock class for JudgeSite. """

    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
        
    def login(self, username, password):
        self._logged = (username, password)

    def upload(self, dataset, solution):
        self._uploaded = (dataset, solution)


def test_evaluate(slack_holder):
    """ Test solution evaluation function. """
    judge = _MockJudge()
    with NamedTemporaryFile() as solution:
        evaluate(
            'test',
            solution.name,
            lambda _: judge,
            lambda d, s: 1)
        assert judge._logged is not None
        assert judge._logged[0] == 'foo@gmail.com'
        assert judge._logged[1] == 'bar'
        assert judge._uploaded is not None
        assert judge._uploaded[0] == 'test'
        assert judge._uploaded[1] == solution.name
        assert exists(solution.name + '.score')
        assert exists('/tmp/test/challenger.score')
        assert exists('/tmp/test/challenger.solution')
        with open(solution.name + '.score', 'r') as stream:
            assert int(stream.read()) == 1
        with open('/tmp/test/challenger.score') as stream:
            assert int(stream.read()) == 1
        remove('/tmp/test/challenger.score')
        remove('/tmp/test/challenger.solution')
