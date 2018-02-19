#!/usr/bin/env python
# coding: utf-8

""" This modules exposes tools for logging into Slack. """

from requests import post

from utils.configuration import configuration

_ICON = 'https://s3-us-west-2.amazonaws.com/slack-files2/avatars/2018-02-13/313621315392_9b0b9b611d28e342530a_132.png'
_USER = 'Kware Judge'


def notify(message, level='good', user=_USER):
    """ Sends a post into dedicated slack channel
    using given level and message.

    :param message: Message to post.
    :param level: (Optional) Message level.
    :param user: (Optional) Message poster.
    """
    _payload = {
        'icon_url': _ICON,
        'username': user,
        'attachments': [{
            'text': text,
            'color': level,
            'mrkdwn_in': ['text']
        }]
    }
    post(configuration.SLACK_WEBHOOK, json=_payload)
