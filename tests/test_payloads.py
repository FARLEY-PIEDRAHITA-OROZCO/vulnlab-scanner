"""Pruebas unitarias para el módulo de payloads."""

import unittest
from app.utils.payloads import XSS_PAYLOADS, SQLI_PAYLOADS, HEADERS_CHECKS


class TestPayloads(unittest.TestCase):
    """Pruebas para verificar la estructura de los payloads."""
    
    def test_xss_payloads_not_empty(self):
        """Verifica que existan payloads XSS."""
        self.assertGreater(len(XSS_PAYLOADS), 0)
    
    def test_xss_payloads_structure(self):
        """Verifica la estructura de los payloads XSS."""
        for payload in XSS_PAYLOADS:
            self.assertIn("type", payload)
            self.assertIn("value", payload)
    
    def test_sqli_payloads_not_empty(self):
        """Verifica que existan payloads SQLi."""
        self.assertGreater(len(SQLI_PAYLOADS), 0)
    
    def test_sqli_payloads_structure(self):
        """Verifica la estructura de los payloads SQLi."""
        for payload in SQLI_PAYLOADS:
            self.assertIn("type", payload)
            self.assertIn("value", payload)
    
    def test_headers_checks_not_empty(self):
        """Verifica que existan verificaciones de headers."""
        self.assertGreater(len(HEADERS_CHECKS), 0)
    
    def test_headers_checks_structure(self):
        """Verifica la estructura de las verificaciones de headers."""
        for check in HEADERS_CHECKS:
            self.assertIn("header", check)
            self.assertIn("recommendation", check)
            self.assertIn("severity", check)


if __name__ == "__main__":
    unittest.main()
