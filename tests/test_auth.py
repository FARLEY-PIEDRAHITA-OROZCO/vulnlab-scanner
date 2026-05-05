"""Pruebas unitarias para el escáner de Auth Failures (A07)."""

import unittest
from unittest.mock import Mock, patch
from app.scanner.auth import AuthScanner
from app.utils.payloads import AUTH_PAYLOADS


class TestAuthScanner(unittest.TestCase):
    """Pruebas para AuthScanner."""
    
    def setUp(self):
        """Configuración antes de cada prueba."""
        self.mock_session = Mock()
        self.scanner = AuthScanner(
            "http://test.com/login",
            self.mock_session,
            dry_run=True
        )
    
    def test_initialization(self):
        """Verifica la inicialización correcta."""
        self.assertEqual(self.scanner.name, "AuthScanner")
        self.assertEqual(self.scanner.target_url, "http://test.com/login")
        self.assertTrue(self.scanner.dry_run)
        self.assertGreater(len(self.scanner.payloads), 0)
        self.assertGreater(len(self.scanner.login_paths), 0)
    
    def test_get_payloads(self):
        """Verifica que se obtengan los payloads correctos."""
        payloads = self.scanner.get_payloads()
        self.assertEqual(len(payloads), len(AUTH_PAYLOADS))
    
    def test_weak_passwords_dry_run(self):
        """Verifica que en modo dry-run no se hagan peticiones."""
        result = self.scanner._test_weak_passwords("http://test.com/login")
        
        self.assertFalse(result)
        self.mock_session.get.assert_not_called()
        self.mock_session.post.assert_not_called()
    
    def test_brute_force_dry_run(self):
        """Verifica que en modo dry-run no se pruebe fuerza bruta."""
        result = self.scanner._test_brute_force("http://test.com/login")
        
        self.assertFalse(result)
        self.mock_session.post.assert_not_called()
    
    def test_session_management_dry_run(self):
        """Verifica que en modo dry-run no se verifiquen sesiones."""
        result = self.scanner._test_session_management("http://test.com/login")
        
        self.assertFalse(result)
        self.mock_session.get.assert_not_called()
        self.mock_session.post.assert_not_called()
    
    def test_weak_passwords_detection(self):
        """Verifica la detección de credenciales débiles."""
        self.scanner.dry_run = False
        
        # Simular respuesta exitosa (200) sin redirección a login
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = "http://test.com/dashboard"
        self.mock_session.post.return_value = mock_response
        
        result = self.scanner._test_weak_passwords("http://test.com/login")
        
        self.assertTrue(result)
        self.assertEqual(len(self.scanner.results), 1)
        self.assertEqual(self.scanner.results[0]["severity"], "CRITICAL")
        self.assertIn("Credentials", self.scanner.results[0]["vulnerability"])
    
    def test_brute_force_detection(self):
        """Verifica que se detecte falta de protección contra fuerza bruta."""
        self.scanner.dry_run = False
        
        # Simular 3 intentos fallidos sin bloqueo
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = "http://test.com/login"
        mock_response.text = "Incorrect password"
        self.mock_session.post.return_value = mock_response
        
        result = self.scanner._test_brute_force("http://test.com/login")
        
        # No reporta como vulnerabilidad automáticamente
        self.assertFalse(result)
        self.assertEqual(len(self.scanner.results), 0)
    
    def test_session_management_detection(self):
        """Verifica la detección de problemas en gestión de sesiones."""
        self.scanner.dry_run = False
        
        # Simular login exitoso y verificar cookies
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = "http://test.com/dashboard"
        
        # Simular cookie sin HttpOnly ni Secure
        mock_cookie = Mock()
        mock_cookie.name = "session"
        mock_cookie.value = "abc123"
        mock_cookie.has_nonstandard_attr.return_value = False
        mock_cookie.secure = False
        mock_response.cookies = [mock_cookie]
        
        self.mock_session.post.return_value = mock_response
        
        result = self.scanner._test_session_management("http://test.com/login")
        
        self.assertTrue(result)
        self.assertGreater(len(self.scanner.results), 0)
    
    def test_scan_with_login_url(self):
        """Verifica el flujo completo de escaneo con URL de login."""
        self.scanner.dry_run = False
        
        # Simular que se encuentra /login
        mock_get_response = Mock()
        mock_get_response.status_code = 200
        self.mock_session.get.return_value = mock_get_response
        
        # Simular credenciales débiles
        mock_post_response = Mock()
        mock_post_response.status_code = 200
        mock_post_response.url = "http://test.com/dashboard"
        mock_post_response.cookies = []
        self.mock_session.post.return_value = mock_post_response
        
        results = self.scanner.scan()
        
        # Debe detectar al menos 1 vulnerabilidad
        self.assertGreater(len(results), 0)
    
    def test_scan_no_login_url(self):
        """Verifica el escaneo cuando no se encuentra URL de login."""
        scanner = AuthScanner(
            "http://test.com/about",
            self.mock_session,
            dry_run=True
        )
        
        results = scanner.scan()
        # No debe encontrar nada porque no hay login
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
