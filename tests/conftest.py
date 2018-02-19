#!/usr/bin/env python
# coding: utf-8

""" Test utils.configuration """

from http.server import BaseHTTPRequestHandler, HTTPServer
from os import environ
from pytest import fixture
from requests import codes
from threading import Thread

__author__ = 'fv'

environ['GOOGLE_USERNAME'] = 'foo@gmail.com'
environ['GOOGLE_PASSWORD'] = 'bar'
environ['SLACK_WEBHOOK'] = 'http://localhost:6969'
environ['ROUND'] = '1'


class _PayloadHolder(object):
    """ Simple holder class. """
    pass


@fixture
def slack_holder():
    """ Run a server that can handle request. """
    _holder = _PayloadHolder()

    class MockSlackServer(BaseHTTPRequestHandler):
        """ Simple mock server that receive slack notification payload. """

        def do_POST(self):
            """ Handle POST method. """
            length = int(self.headers['Content-Length'])
            _holder.payload = self.rfile.read(length)
            self.send_response(codes.ok)
            self.end_headers()

    _slack_server = HTTPServer(('localhost', 6969), MockSlackServer)
    _thread = Thread(target=_slack_server.serve_forever)
    _thread.setDaemon(True)
    _thread.start()
    yield _holder
    _slack_server.shutdown()
