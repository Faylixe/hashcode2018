#!/usr/bin/env python
# coding: utf8

""" Functional test for utils.judge """

# Force Firefox usage.
from os import environ
environ['SELENIUM_DRIVER'] = 'firefox'

from getpass import getpass

from utils.judge import JudgeSite


def test_login():
    """ Test authentification. """
    email = 'felix.voituret@gmail.com'
    password = getpass()
    with JudgeSite('1') as judge:
        judge.login(email, password)


if __name__ == '__main__':
    test_login()
