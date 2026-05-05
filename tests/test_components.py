"""Pruebas unitarias para el escáner de Vulnerable Components (A06)."""

import unittest
from unittest.mock import Mock, patch
from app.scanner.components import ComponentsScanner
from app.utils.payloads import COMPONENTS_PAYLOADS


class TestComponentsScanner(unittest.TestCase):
    """Pruebas para ComponentsScanner."""
    
    def setUp(self):
        """Configuración antes de cada prueba."""
        self.mock_session = Mock()
        self.scanner = ComponentsScanner(
            "http://test.com",
            self.mock_session,
            dry_run=True
        )
    
    def test_initialization(self):
        """Verifica la inicialización correcta."""
        self.assertEqual(self.scanner.name, "ComponentsScanner")
        self.assertEqual(self.scanner.target_url, "http://test.com")
        self.assertTrue(self.scanner.dry_run)
        self.assertGreater(len(self.scanner.payloads), 0)
    
    def test_get_payloads(self):
        """Verifica que se obtengan los payloads correctos."""
        payloads = self.scanner.get_payloads()
        self.assertEqual(len(payloads), len(COMPONENTS_PAYLOADS))
    
    def test_extract_scripts(self):
        """Verifica extracción de scripts JS."""
        html = '<script src="https://cdn.com/jquery/1.11.3/jquery.min.js"></script>'
        scripts = self.scanner._extract_scripts(html)
        
        self.assertEqual(len(scripts), 1)
        self.assertIn("jquery/1.11.3/jquery.min.js", scripts[0])
    
    def test_extract_cdns(self):
        """Verifica extracción de CDNs."""
        html = '<script src="https://cdn.com/bootstrap/2.3.1/bootstrap.min.js"></script>'
        cdns = self.scanner._extract_cdns(html)
        
        self.assertGreater(len(cdns), 0)
        self.assertIn("Bootstrap", [name for name, ver in cdns])
    
    def test_check_technology_headers(self):
        """Verifica detección de tecnologías por headers."""
        headers = {
            "X-Powered-By": "ASP.NET",
            "Server": "Microsoft-IIS/10.0"
        }
        
        tech = self.scanner._check_technology_headers(headers)
        
        self.assertGreater(len(tech), 0)
    
    def test_check_version_vulnerable(self):
        """Verifica detección de versiones vulnerables."""
        # jQuery 1.11.3 es vulnerable
        result = self.scanner._check_version_vulnerable("jQuery", "1.11.3")
        self.assertTrue(result)
        
        # jQuery 3.6.0 no es vulnerable (en nuestra lista)
        result = self.scanner._check_version_vulnerable("jQuery", "3.6.0")
        self.assertFalse(result)
    
    def test_scan_dry_run(self):
        """Verifica modo dry-run."""
        results = self.scanner.scan()
        
        self.mock_session.get.assert_not_called()
        self.assertEqual(len(results), 0)
    
    def test_scan_with_technology_headers(self):
        """Verifica detección de tecnologías via headers."""
        self.scanner.dry_run = False
        
        mock_response = Mock()
        mock_response.text = "<html><head></head><body>Test</body></html>"
        mock_response.headers = {
            "X-Powered-By": "ASP.NET"
        }
        self.mock_session.get.return_value = mock_response
        
        results = self.scanner.scan()
        
        # Debe detectar al menos la tecnología por headers
        self.assertGreater(len(results), 0)
    
    def test_scan_with_vulnerable_js(self):
        """Verifica detección de JS vulnerable."""
        self.scanner.dry_run = False
        
        html_content = '''
        <html>
            <head>
                <script src="https://code.jquery.com/jquery-1.11.3.min.js"></script>
            </head>
            <body>Test</body>
        </html>
        '''
        
        mock_response = Mock()
        mock_response.text = html_content
        mock_response.headers = {}
        self.mock_session.get.return_value = mock_response
        
        results = self.scanner.scan()
        
        # Debe detectar jQuery vulnerable
        vuln_names = [r["vulnerability"] for r in results]
        self.assertIn("Outdated Component Detected", vuln_names)


if __name__ == '__main__':
    unittest.main()
