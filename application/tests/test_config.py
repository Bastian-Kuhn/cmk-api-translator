""" Test for right configuration """
import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app # pylint: disable=import-error

class TestDevelopmentConfig(TestCase):
    """ Test Development Config"""
    def create_app(self):
        """ prepare config """
        app.config.from_object('application.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        """ test values """
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue('CLX_CONFIG' in app.config)
        self.assertTrue('IMPORTER_CONFIG' in app.config)
        self.assertTrue(app.config['SPICE_CONFIG']['SPICE_URL'].startswith("https://pmu01-qa-"))
        self.assertFalse(current_app is None)


class TestProductionConfig(TestCase):
    """ Test Production Config """
    def create_app(self):
        """ prepare config """
        app.config.from_object('application.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        """ test values """
        self.assertTrue(app.config['DEBUG'] is False)
        self.assertTrue('CLX_CONFIG' in app.config)
        self.assertTrue('IMPORTER_CONFIG' in app.config)
        self.assertTrue(app.config['SPICE_CONFIG']['SPICE_URL'].startswith("https://ws.pmi-"))
        self.assertTrue(app.config['SESSION_COOKIE_SECURE'] is True)


if __name__ == '__main__':
    unittest.main()
