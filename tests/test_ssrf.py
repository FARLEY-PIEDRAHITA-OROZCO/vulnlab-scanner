"""Pruebas unitarias para el escáner SSRF (A10)."""

import unittest
from unittest.mock import Mock, patch
from app.scanner.ssrf import SSRFScanner
from app.utils.payloads import SSRF_PAYLOADS


class TestSSRFScanner(unittest.TestCase):
    """Pruebas para SSRFScanner."""
    
    def setUp(self):
        """Configuración antes de cada prueba."""
        self.mock_session = Mock()
        self.scanner = SSRFScanner(
            "http://test.com/page?url=http://example.com",
            self.mock_session,
            dry_run=True
        )
    
    def test_initialization(self):
        """Verifica la inicialización correcta."""
        self.assertEqual(self.scanner.name, "SSRFScanner")
        self.assertEqual(self.scanner.target_url, "http://test.com/page?url=http://example.com")
        self.assertTrue(self.scanner.dry_run)
        self.assertGreater(len(self.scanner.payloads), 0)
        self.assertGreater(len(self.scanner.internal_ips), 0)
    
    def test_get_payloads(self):
        """Verifica que se obtengan los payloads correctos."""
        payloads = self.scanner.get_payloads()
        self.assertEqual(len(payloads), len(SSRF_PAYLOADS))
    
    def test_inject_param(self):
        """Verifica la inyección de parámetros en URL."""
        original = "http://test.com/page?name=test"
        result = self.scanner._inject_param(original, "url", "http://localhost/")
        
        self.assertIn("url=http%3A%2F%2Flocalhost%2F", result)
    
    def test_ssrf_param_dry_run(self):
        """Verifica que en modo dry-run no se hagan peticiones."""
        result = self.scanner._test_ssrf_param("url", "http://localhost/")
        
        self.assertFalse(result)
        self.mock_session.get.assert_not_called()
    
    def test_ssrf_param_detection(self):
        """Verifica detección de SSRF via parámetros."""
        self.scanner.dry_run = False
        
        # Simular respuesta con indicador de SSRF
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Welcome to localhost! Root access available."
        self.mock_session.get.return_value = mock_response
        
        result = self.scanner._test_ssrf_param("url", "http://127.0.0.1/")
        
        self.assertTrue(result)
        self.assertEqual(len(self.scanner.results), 1)
        self.assertEqual(self.scanner.results[0]["severity"], "HIGH")
        self.assertIn("SSRF", self.scanner.results[0]["vulnerability"])
    
    def test_ssrf_no_vuln(self):
        """Verifica que no reporte si no hay vulnerabilidad."""
        self.scanner.dry_run = False
        
        # Simular respuesta sin indicadores
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Normal page content"
        self.mock_session.get.return_value = mock_response
        
        result = self.scanner._test_ssrf_param("url", "http://example.com/")
        
        self.assertFalse(result)
        self.assertEqual(len(self.scanner.results), 0)
    
    def test_dangerous_schemes_dry_run(self):
        """Verifica que en modo dry-run no se prueben esquemas."""
        result = self.scanner._test_dangerous_schemes()
        
        self.assertFalse(result)
        self.mock_session.get.assert_not_called()
    
    def test_scan_dry_run(self):
        """Verifica que el escaneo en dry-run no genere resultados."""
        results = self.scanner.scan()
        
        self.assertEqual(len(results), 0)
        self.mock_session.get.assert_not_called()
    
    def test_get_url_params(self):
        """Verifica extracción de parámetros de URL."""
        url = "http://test.com/page?url=http://example.com&name=test"
        params = self.scanner._get_url_params(url)
        
        self.assertIn("url", params)
        self.assertIn("name", params)


if __name__ == "__main__":
    unittest.main()
