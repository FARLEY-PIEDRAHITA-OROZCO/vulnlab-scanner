"""Pruebas unitarias para el escáner de Access Control (A01)."""

import unittest
from unittest.mock import Mock, patch
from app.scanner.access_control import AccessControlScanner
from app.utils.payloads import ACCESS_CONTROL_PAYLOADS


class TestAccessControlScanner(unittest.TestCase):
    """Pruebas para AccessControlScanner."""
    
    def setUp(self):
        """Configuración antes de cada prueba."""
        self.mock_session = Mock()
        self.scanner = AccessControlScanner(
            "http://test.com/user/123/profile",
            self.mock_session,
            dry_run=True
        )
    
    def test_initialization(self):
        """Verifica la inicialización correcta."""
        self.assertEqual(self.scanner.name, "AccessControlScanner")
        self.assertEqual(self.scanner.target_url, "http://test.com/user/123/profile")
        self.assertTrue(self.scanner.dry_run)
        self.assertGreater(len(self.scanner.payloads), 0)
        self.assertEqual(len(self.scanner.tested_urls), 0)
    
    def test_get_payloads(self):
        """Verifica que se obtengan los payloads correctos."""
        payloads = self.scanner.get_payloads()
        self.assertEqual(len(payloads), len(ACCESS_CONTROL_PAYLOADS))
    
    def test_extract_ids_from_url_with_path_ids(self):
        """Verifica extracción de IDs numéricos en el path."""
        url = "http://test.com/user/123/profile"
        ids = self.scanner._extract_ids_from_url(url)
        
        self.assertGreater(len(ids), 0)
        # Verificar que contiene el ID original y el modificado
        id_values = [(orig, test) for type, orig, test in ids]
        self.assertIn(("123", "124"), id_values)
    
    def test_extract_ids_from_url_with_param_ids(self):
        """Verifica extracción de IDs en parámetros."""
        url = "http://test.com/view?id=456"
        ids = self.scanner._extract_ids_from_url(url)
        
        self.assertGreater(len(ids), 0)
        id_values = [(orig, test) for type, orig, test in ids]
        self.assertIn(("456", "457"), id_values)
    
    def test_extract_ids_from_url_no_ids(self):
        """Verifica comportamiento sin IDs."""
        url = "http://test.com/about"
        ids = self.scanner._extract_ids_from_url(url)
        
        self.assertEqual(len(ids), 0)
    
    def test_idor_dry_run(self):
        """Verifica que en modo dry-run no se hagan peticiones."""
        url = "http://test.com/user/123"
        result = self.scanner._test_idor(url, "path", "123", "124")
        
        self.assertFalse(result)
        self.mock_session.get.assert_not_called()
    
    def test_idor_detection(self):
        """Verifica detección real de IDOR."""
        self.scanner.dry_run = False
        
        # Simular respuesta exitosa (200) sin login
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = "http://test.com/user/124/profile"
        self.mock_session.get.return_value = mock_response
        
        result = self.scanner._test_idor(
            "http://test.com/user/123/profile",
            "path", "123", "124"
        )
        
        self.assertTrue(result)
        self.assertEqual(len(self.scanner.results), 1)
        self.assertEqual(self.scanner.results[0]["severity"], "HIGH")
        self.assertIn("IDOR", self.scanner.results[0]["vulnerability"])
    
    def test_privilege_escalation_dry_run(self):
        """Verifica que en modo dry-run no se prueben rutas admin."""
        result = self.scanner._test_privilege_escalation("http://test.com")
        
        self.assertFalse(result)
        self.mock_session.get.assert_not_called()
    
    def test_privilege_escalation_detection(self):
        """Verifica detección de escalación de privilegios."""
        self.scanner.dry_run = False
        
        # Simular acceso a /admin sin login
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = "http://test.com/admin"
        self.mock_session.get.return_value = mock_response
        
        result = self.scanner._test_privilege_escalation("http://test.com")
        
        self.assertTrue(result)
        self.assertEqual(len(self.scanner.results), 1)
        self.assertEqual(self.scanner.results[0]["severity"], "CRITICAL")
        self.assertIn("Privilege", self.scanner.results[0]["vulnerability"])
    
    def test_scan_with_ids(self):
        """Verifica el flujo completo de escaneo con IDs."""
        self.scanner.dry_run = False
        
        # Simular respuesta para IDOR
        mock_response_idor = Mock()
        mock_response_idor.status_code = 200
        mock_response_idor.url = "http://test.com/user/124"
        self.mock_session.get.return_value = mock_response_idor
        
        # Simular acceso a /admin
        mock_response_admin = Mock()
        mock_response_admin.status_code = 200
        mock_response_admin.url = "http://test.com/admin"
        
        def side_effect(url, **kwargs):
            if "admin" in url:
                return mock_response_admin
            return mock_response_idor
        
        self.mock_session.get.side_effect = side_effect
        
        results = self.scanner.scan()
        
        # Debe detectar al menos 1 vulnerabilidad
        self.assertGreater(len(results), 0)
    
    def test_scan_no_ids(self):
        """Verifica el escaneo sin IDs para probar."""
        scanner = AccessControlScanner(
            "http://test.com/about",
            self.mock_session
        )
        scanner.dry_run = True
        
        results = scanner.scan()
        # No debe encontrar nada porque no hay IDs
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
