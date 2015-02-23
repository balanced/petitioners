# This Python file uses the following encoding: utf-8
from __future__ import unicode_literals

import unittest

import flask
from werkzeug.test import Client
from werkzeug.wrappers import Response

import petitioners


TRACE_HEADER = 'X-Trace-Request'
TRACE_PREFIX = 'OHHM-'


@petitioners.register_flask_app(TRACE_HEADER, TRACE_PREFIX)
class FlaskApp(flask.Flask):
    pass


def hello_world():
    return 'Hello 漢語!'


class BaseTestCase(unittest.TestCase):
    pass


class ServerTestCase(BaseTestCase):

    def setUp(self):
        super(ServerTestCase, self).setUp()

        self.app = FlaskApp(__name__)
        self.app.route('/', methods=['POST', 'GET'])(hello_world)
        ctx = self.app.test_request_context()
        ctx.push()
        self.addCleanup(ctx.pop)
        self.client = Client(self.app, response_wrapper=Response)

    def test_trace_generated(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(TRACE_HEADER, response.headers.keys())

    def test_trace_is_unique_per_request(self):
        response = self.client.get('/')
        value1 = response.headers[TRACE_HEADER]
        response = self.client.get('/')
        value2 = response.headers[TRACE_HEADER]
        self.assertNotEqual(value1, value2)

    def test_trace_prefixing(self):
        response = self.client.get('/')
        value = response.headers[TRACE_HEADER]
        self.assertTrue(value.startswith(TRACE_PREFIX), value)

    def test_multiple_requests_appended(self):
        headers = {TRACE_HEADER: 'Trace123'}
        response = self.client.get('/', headers=headers)
        value = response.headers[TRACE_HEADER]
        self.assertTrue(value.startswith('Trace123,' + TRACE_PREFIX))
