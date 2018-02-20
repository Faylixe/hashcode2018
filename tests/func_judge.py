#!/usr/bin/env python
# coding: utf8

""" Functional test for utils.judge """

# Force Firefox usage.
from os import environ
#environ['SELENIUM_DRIVER'] = 'firefox'

from getpass import getpass

from utils.judge import JudgeSite


def test_login():
    """ Test authentification. """
    round = '5736842779426816'
    email = 'felix.voituret@gmail.com'
    password = getpass()
    with open('/tmp/exemple.out', 'w') as stream:
        stream.write('1\n0 0 1 1')
    with JudgeSite(round) as judge:
        judge.login(email, password)
        judge.upload('example', '/tmp/exemple.out')


if __name__ == '__main__':
    test_login()
