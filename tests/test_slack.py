#!/usr/bin/env python
# coding: utf-8

""" Test utils.slack """

from utils.slack import notify
from json import loads


def test_notify(slack_holder):
    """ Test notification function. """
    notify('Test message', level='good', user='Unit test')
    assert slack_holder.payload is not None
    payload = loads(slack_holder.payload.decode('utf-8'))
    assert payload['username'] == 'Unit test'
    assert len(payload['attachments']) == 1
    assert payload['attachments'][0]['text'] == 'Test message'
    assert payload['attachments'][0]['color'] == 'good'
