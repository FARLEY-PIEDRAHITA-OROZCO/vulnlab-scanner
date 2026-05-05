"""Pruebas unitarias para el escáner SQL Injection."""

import unittest
from unittest.mock import Mock, patch
from app.scanner.sqli import SQLiScanner
from app.utils.payloads import SQLI_PAYLOADS


class TestSQLiScanner(unittest.TestCase):
    """Pruebas para SQLiScanner."""
    
    def setUp(self):
        """Configuración antes de cada prueba."""
        self.mock_session = Mock()
        self.scanner = SQLiScanner(
            "http://test.com/search?id=1",
            self.mock_session,
            dry_run=True
        )
    
    def test_initialization(self):
        """Verifica la inicialización correcta."""
        self.assertEqual(self.scanner.name, "SQLiScanner")
        self.assertEqual(self.scanner.target_url, "http://test.com/search?id=1")
        self.assertTrue(self.scanner.dry_run)
        self.assertGreater(len(self.scanner.payloads), 0)
        self.assertGreater(len(self.scanner.error_indicators), 0)
    
    def test_get_payloads(self):
        """Verifica que se obtengan los payloads correctos."""
        payloads = self.scanner.get_payloads()
        self.assertEqual(len(payloads), len(SQLI_PAYLOADS))
    
    def test_dry_run_mode(self):
        """Verifica que en modo dry-run no se hagan peticiones."""
        results = self.scanner.scan()
        self.mock_session.get.assert_not_called()
    
    def test_inject_payload(self):
        """Verifica la inyección de payloads en URL."""
        url = "http://test.com/search?id=1"
        result = self.scanner._inject_payload(url, "id", "' OR '1'='1")
        
        # Verificar que el payload se inyectó (no verificar codificación exacta)
        self.assertIn("id=", result)
        self.assertIn("OR", result)
    
    def test_error_based_detection(self):
        """Verifica la detección basada en errores."""
        self.scanner.dry_run = False
        
        # Simular respuesta con error SQL
        mock_response = Mock()
        mock_response.text = "You have an error in your SQL syntax"
        self.mock_session.get.return_value = mock_response
        
        result = self.scanner._check_error_based(
            "http://test.com?id=1",
            "id",
            {"type": "error_based", "value": "' OR '1'='1"}
        )
        
        self.assertTrue(result)
        self.assertEqual(len(self.scanner.results), 1)
        self.assertEqual(self.scanner.results[0]["severity"], "CRITICAL")
    
    def test_scan_no_params(self):
        """Verifica el comportamiento sin parámetros en URL."""
        scanner = SQLiScanner("http://test.com/", self.mock_session)
        results = scanner.scan()
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
