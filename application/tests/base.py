"""
Basic Unitest configuration and helpers
"""
# pylint: disable=no-self-use
import json
from flask_testing import TestCase
from manage import app


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        """ Prepare configfile """
        app.config.from_object('application.config.TestingConfig')
        return app

    def request_get(self, url, headers):
        """ Helper for get Requests """
        with self.client:
            result = self.client.get(url, headers=headers)
            return json.loads(result.data.decode())

    def request_post(self, url, data, additional_headers):
        """ Helper for post Requests """
        headers = {"Content-Type" : "application/json"}
        headers.update(additional_headers)
        with self.client:
            result = self.client.post(url, data=json.dumps(data), headers=headers)
            return json.loads(result.data.decode())
