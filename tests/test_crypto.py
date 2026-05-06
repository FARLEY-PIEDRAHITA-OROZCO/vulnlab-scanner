"""Pruebas unitarias para el escáner de Cryptographic Failures (A02)."""

import unittest
from unittest.mock import Mock, patch
from app.scanner.crypto import CryptoScanner
from app.utils.payloads import CRYPTO_PAYLOADS


class TestCryptoScanner(unittest.TestCase):
    """Pruebas para CryptoScanner."""
    
    def setUp(self):
        """Configuración antes de cada prueba."""
        self.mock_session = Mock()
        self.scanner = CryptoScanner(
            "https://test.com",
            self.mock_session,
            dry_run=True
        )
    
    def test_initialization(self):
        """Verifica la inicialización correcta."""
        self.assertEqual(self.scanner.name, "CryptoScanner")
        self.assertEqual(self.scanner.target_url, "https://test.com")
        self.assertTrue(self.scanner.dry_run)
        self.assertGreater(len(self.scanner.payloads), 0)
    
    def test_get_payloads(self):
        """Verifica que se obtengan los payloads correctos."""
        payloads = self.scanner.get_payloads()
        self.assertEqual(len(payloads), len(CRYPTO_PAYLOADS))
    
    def test_https_missing_detection(self):
        """Verifica detección de HTTPS faltante."""
        scanner = CryptoScanner("http://test.com", self.mock_session, dry_run=False)
        
        results = scanner.scan()
        
        self.assertGreater(len(results), 0)
        self.assertIn("HTTPS", results[0]["vulnerability"])
        self.assertEqual(results[0]["severity"], "HIGH")
    
    def test_https_present(self):
        """Verifica que no reporte vulnerabilidad si usa HTTPS."""
        scanner = CryptoScanner("https://test.com", self.mock_session, dry_run=False)
        
        # Simular respuesta sin cookies problemáticas
        mock_response = Mock()
        mock_response.cookies = []
        self.mock_session.get.return_value = mock_response
        
        results = scanner.scan()
        
        # No debe reportar "Missing HTTPS"
        vuln_names = [r["vulnerability"] for r in results]
        self.assertNotIn("Missing HTTPS", vuln_names)
    
    def test_cookie_secure_missing(self):
        """Verifica detección de cookies sin flag Secure."""
        self.scanner.dry_run = False
        
        # Simular cookie sin flag Secure
        mock_cookie = Mock()
        mock_cookie.name = "sessionid"
        mock_cookie.secure = False
        
        mock_response = Mock()
        mock_response.cookies = [mock_cookie]
        self.mock_session.get.return_value = mock_response
        
        result = self.scanner._check_cookies_secure()
        
        self.assertTrue(result)
        self.assertEqual(len(self.scanner.results), 1)
        self.assertEqual(self.scanner.results[0]["severity"], "MEDIUM")
        self.assertIn("Secure", self.scanner.results[0]["vulnerability"])
    
    def test_cookie_secure_present(self):
        """Verifica que no reporte si las cookies tienen Secure."""
        self.scanner.dry_run = False
        
        # Simular cookie con flag Secure
        mock_cookie = Mock()
        mock_cookie.secure = True
        
        mock_response = Mock()
        mock_response.cookies = [mock_cookie]
        self.mock_session.get.return_value = mock_response
        
        result = self.scanner._check_cookies_secure()
        
        self.assertFalse(result)
        self.assertEqual(len(self.scanner.results), 0)
    
    def test_sensitive_in_url_detection(self):
        """Verifica detección de credenciales en URL."""
        scanner = CryptoScanner(
            "http://test.com/login?password=123456",
            self.mock_session,
            dry_run=False
        )
        
        result = scanner._check_sensitive_in_url()
        
        self.assertTrue(result)
        self.assertEqual(len(scanner.results), 1)
        self.assertEqual(scanner.results[0]["severity"], "HIGH")
        self.assertIn("Sensitive", scanner.results[0]["vulnerability"])
    
    def test_sensitive_in_url_not_present(self):
        """Verifica que no reporte si no hay credenciales en URL."""
        self.scanner.dry_run = False
        
        result = self.scanner._check_sensitive_in_url()
        
        self.assertFalse(result)
        self.assertEqual(len(self.scanner.results), 0)
    
    def test_credentials_in_url_basic_auth(self):
        """Verifica detección de user:pass@host en URL."""
        scanner = CryptoScanner(
            "http://admin:password@test.com",
            self.mock_session,
            dry_run=False
        )
        
        result = scanner._check_sensitive_in_url()
        
        self.assertTrue(result)
        self.assertEqual(scanner.results[0]["severity"], "CRITICAL")
        self.assertIn("Credentials", scanner.results[0]["vulnerability"])
    
    def test_scan_dry_run(self):
        """Verifica que en modo dry-run no se hagan peticiones."""
        results = self.scanner.scan()
        
        self.assertEqual(len(results), 0)
        self.mock_session.get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
