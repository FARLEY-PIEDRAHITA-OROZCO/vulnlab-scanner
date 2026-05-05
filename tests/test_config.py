"""Pruebas unitarias para el módulo de configuración."""

import unittest
import os
from app.config import Config


class TestConfig(unittest.TestCase):
    """Pruebas para la clase Config."""
    
    def test_config_attributes_exist(self):
        """Verifica que los atributos de configuración existan."""
        self.assertIsNotNone(Config.RATE_LIMIT)
        self.assertIsNotNone(Config.HTTP_TIMEOUT)
        self.assertIsNotNone(Config.REPORTS_DIR)
        self.assertIsNotNone(Config.USER_AGENT)
    
    def test_rate_limit_type(self):
        """Verifica que RATE_LIMIT sea numérico."""
        self.assertIsInstance(Config.RATE_LIMIT, float)
    
    def test_http_timeout_type(self):
        """Verifica que HTTP_TIMEOUT sea entero."""
        self.assertIsInstance(Config.HTTP_TIMEOUT, int)


if __name__ == "__main__":
    unittest.main()
