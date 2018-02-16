#!/usr/bin/env python
# coding: utf-8

""" This modules exposes tools for logging into Slack. """

from requests import post

_WEBHOOK = 'https://hooks.slack.com/services/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'
_ICON = 'https://s3-us-west-2.amazonaws.com/slack-files2/avatars/2018-02-13/313621315392_9b0b9b611d28e342530a_132.png'
_USER = 'Kware Judge'


def notify(message, level='good'):
    """ Sends a post into dedicated slack channel
    using given level and message.

    :param message: Message to post.
    :param level: (Optional) Message level.
    """
    _payload = {
        'icon_url': _ICON,
        'username': _USER,
        'attachments': [{
            'text': text,
            'color': level,
            'mrkdwn_in': ['text']
        }]
    }
    post(_WEBHOOK, json=_payload)
