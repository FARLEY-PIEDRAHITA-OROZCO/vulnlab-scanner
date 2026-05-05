"""Pruebas unitarias para la clase BaseScanner."""

import unittest
from unittest.mock import Mock, MagicMock
from app.scanner.base import BaseScanner
from datetime import datetime


class MockScanner(BaseScanner):
    """Scanner de prueba para probar la clase base."""
    
    def scan(self):
        return self.results
    
    def get_payloads(self):
        return []


class TestBaseScanner(unittest.TestCase):
    """Pruebas para BaseScanner."""
    
    def setUp(self):
        """Configuración antes de cada prueba."""
        self.mock_session = Mock()
        self.scanner = MockScanner("http://test.com", self.mock_session)
    
    def test_initialization(self):
        """Verifica la inicialización correcta."""
        self.assertEqual(self.scanner.name, "MockScanner")
        self.assertEqual(self.scanner.target_url, "http://test.com")
        self.assertEqual(self.scanner.results, [])
        self.assertFalse(self.scanner.dry_run)
    
    def test_add_result(self):
        """Verifica que se agreguen resultados correctamente."""
        self.scanner.add_result(
            vuln_name="Test Vuln",
            severity="HIGH",
            description="Test desc",
            evidence="Test evidence"
        )
        
        self.assertEqual(len(self.scanner.results), 1)
        result = self.scanner.results[0]
        self.assertEqual(result["vulnerability"], "Test Vuln")
        self.assertEqual(result["severity"], "HIGH")
        self.assertEqual(result["url"], "http://test.com")
        self.assertIn("timestamp", result)
    
    def test_get_results(self):
        """Verifica que get_results retorne los resultados."""
        self.scanner.add_result("Vuln1", "HIGH", "Desc1")
        results = self.scanner.get_results()
        self.assertEqual(len(results), 1)
    
    def test_clear_results(self):
        """Verifica que clear_results limpie los resultados."""
        self.scanner.add_result("Vuln1", "HIGH", "Desc1")
        self.scanner.clear_results()
        self.assertEqual(len(self.scanner.results), 0)
    
    def test_dry_run_mode(self):
        """Verifica el modo dry-run."""
        scanner = MockScanner("http://test.com", self.mock_session, dry_run=True)
        self.assertTrue(scanner.dry_run)


if __name__ == "__main__":
    unittest.main()
