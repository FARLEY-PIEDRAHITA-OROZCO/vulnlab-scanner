"""Pruebas unitarias para el escáner XSS."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from app.scanner.xss import XSSScanner
from app.utils.payloads import XSS_PAYLOADS


class TestXSSScanner(unittest.TestCase):
    """Pruebas para XSSScanner."""
    
    def setUp(self):
        """Configuración antes de cada prueba."""
        self.mock_session = Mock()
        self.scanner = XSSScanner(
            "http://test.com/search?q=test", 
            self.mock_session,
            dry_run=True
        )
    
    def test_initialization(self):
        """Verifica la inicialización correcta."""
        self.assertEqual(self.scanner.name, "XSSScanner")
        self.assertEqual(self.scanner.target_url, "http://test.com/search?q=test")
        self.assertTrue(self.scanner.dry_run)
        self.assertGreater(len(self.scanner.payloads), 0)
    
    def test_get_payloads(self):
        """Verifica que se obtengan los payloads correctos."""
        payloads = self.scanner.get_payloads()
        self.assertEqual(len(payloads), len(XSS_PAYLOADS))
    
    def test_dry_run_mode(self):
        """Verifica que en modo dry-run no se hagan peticiones."""
        results = self.scanner.scan()
        # En dry-run no debe haber resultados reales
        self.mock_session.get.assert_not_called()
    
    @patch('app.scanner.xss.XSSScanner._inject_payload')
    @patch('app.scanner.xss.XSSScanner._check_reflected_xss')
    def test_scan_with_params(self, mock_check, mock_inject):
        """Verifica que se escaneen los parámetros."""
        # Cambiar a modo no dry-run
        self.scanner.dry_run = False
        
        # Simular que no se encuentran vulnerabilidades
        mock_check.return_value = False
        
        results = self.scanner.scan()
        # Debe haber llamado a _check_reflected_xss al menos una vez
        mock_check.assert_called()
    
    def test_inject_payload(self):
        """Verifica la inyección de payloads en URL."""
        url = "http://test.com/search?q=test"
        result = self.scanner._inject_payload(url, "q", "<script>alert(1)</script>")
        
        self.assertIn("q=%3Cscript%3Ealert%281%29%3C%2Fscript%3E", result)
    
    def test_scan_no_params(self):
        """Verifica el comportamiento sin parámetros en URL."""
        scanner = XSSScanner("http://test.com/", self.mock_session)
        results = scanner.scan()
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
