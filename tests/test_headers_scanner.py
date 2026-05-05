"""Pruebas unitarias para el escáner de Headers."""

import unittest
from unittest.mock import Mock, patch
from app.scanner.headers import HeadersScanner
from app.utils.payloads import HEADERS_CHECKS


class TestHeadersScanner(unittest.TestCase):
    """Pruebas para HeadersScanner."""
    
    def setUp(self):
        """Configuración antes de cada prueba."""
        self.mock_session = Mock()
        self.scanner = HeadersScanner(
            "http://test.com",
            self.mock_session,
            dry_run=False
        )
    
    def test_initialization(self):
        """Verifica la inicialización correcta."""
        self.assertEqual(self.scanner.name, "HeadersScanner")
        self.assertEqual(self.scanner.target_url, "http://test.com")
        self.assertFalse(self.scanner.dry_run)
        self.assertEqual(len(self.scanner.checks), len(HEADERS_CHECKS))
    
    def test_get_payloads(self):
        """Verifica que se obtengan las verificaciones correctas."""
        checks = self.scanner.get_payloads()
        self.assertEqual(len(checks), len(HEADERS_CHECKS))
    
    def test_missing_headers(self):
        """Verifica la detección de headers faltantes."""
        # Simular respuesta sin headers de seguridad
        mock_response = Mock()
        mock_response.headers = {}  # Sin headers
        self.mock_session.get.return_value = mock_response
        
        results = self.scanner.scan()
        
        # Debe detectar todos los headers como faltantes
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertIn("Missing Security Header", result["vulnerability"])
    
    def test_present_headers(self):
        """Verifica el comportamiento cuando los headers están presentes."""
        # Simular respuesta con algunos headers
        mock_response = Mock()
        mock_response.headers = {
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff"
        }
        self.mock_session.get.return_value = mock_response
        
        # Limpiar resultados anteriores
        self.scanner.clear_results()
        results = self.scanner.scan()
        
        # Los headers presentes no deben aparecer como vulnerabilidades
        missing = [r for r in results if "Missing" in r["vulnerability"]]
        self.assertLess(len(missing), len(HEADERS_CHECKS))
    
    def test_dry_run_mode(self):
        """Verifica que en modo dry-run no se hagan peticiones."""
        self.scanner.dry_run = True
        results = self.scanner.scan()
        self.mock_session.get.assert_not_called()
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
