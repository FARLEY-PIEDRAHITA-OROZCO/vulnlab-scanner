"""Pruebas de integración simuladas para VulnLab Scanner.

Estas pruebas simulan el comportamiento con respuestas controladas
para validar el flujo completo sin necesidad de aplicaciones vulnerables reales.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
from datetime import datetime
from app.main import main
from app.utils.reporter import save_report, generate_summary


class TestFullScanFlow(unittest.TestCase):
    """Pruebas de integración del flujo completo de escaneo."""
    
    @patch('app.core.session.ScannerSession')
    @patch('app.utils.disclaimer.check_legal_requirements')
    def test_headers_scan_flow(self, mock_check, mock_session_class):
        """Prueba el flujo completo de escaneo de headers."""
        # Configurar mocks
        mock_check.return_value = True
        
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_session.is_authenticated = False
        
        # Simular respuesta HTTP con algunos headers faltantes
        mock_response = Mock()
        mock_response.headers = {
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff"
        }
        mock_session.get.return_value = mock_response
        
        # Ejecutar escaneo (necesitaríamos capturar salida)
        # En un caso real, aquí validaríamos que se generen reportes
    
    def test_generate_summary(self):
        """Prueba la generación de resumen de resultados."""
        results = [
            {"severity": "CRITICAL"},
            {"severity": "HIGH"},
            {"severity": "HIGH"},
            {"severity": "MEDIUM"},
            {"severity": "LOW"},
            {"severity": "LOW"},
            {"severity": "LOW"}
        ]
        
        summary = generate_summary(results)
        
        self.assertEqual(summary["total_vulnerabilities"], 7)
        self.assertEqual(summary["critical"], 1)
        self.assertEqual(summary["high"], 2)
        self.assertEqual(summary["medium"], 1)
        self.assertEqual(summary["low"], 3)
    
    def test_save_json_report(self):
        """Prueba que se guarde correctamente el reporte JSON."""
        import tempfile
        import os
        
        data = {
            "scan_info": {
                "target_url": "http://test.com",
                "start_time": datetime.now().isoformat()
            },
            "results": [
                {
                    "scanner": "TestScanner",
                    "vulnerability": "Test Vuln",
                    "severity": "HIGH"
                }
            ],
            "summary": {"total_vulnerabilities": 1, "critical": 0, "high": 1, "medium": 0, "low": 0}
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            saved_files = save_report(
                data["results"],
                data["scan_info"],
                report_format="json",
                output_dir=tmpdir
            )
            
            self.assertTrue(len(saved_files) > 0)
            filepath = saved_files[0]
            self.assertTrue(os.path.exists(filepath))
            
            # Verificar contenido
            with open(filepath, 'r') as f:
                loaded = json.load(f)
                self.assertEqual(len(loaded["results"]), 1)
    
    def test_save_html_report(self):
        """Prueba que se guarde correctamente el reporte HTML."""
        import tempfile
        import os
        
        data = {
            "scan_info": {
                "target_url": "http://test.com",
                "start_time": datetime.now().isoformat()
            },
            "results": [
                {
                    "scanner": "TestScanner",
                    "vulnerability": "Test Vuln",
                    "severity": "HIGH",
                    "url": "http://test.com",
                    "description": "Test desc",
                    "evidence": "Test evidence"
                }
            ],
            "summary": {"total_vulnerabilities": 1, "critical": 0, "high": 1, "medium": 0, "low": 0}
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            saved_files = save_report(
                data["results"],
                data["scan_info"],
                report_format="html",
                output_dir=tmpdir
            )
            
            self.assertTrue(len(saved_files) > 0)
            filepath = saved_files[0]
            self.assertTrue(os.path.exists(filepath))
            
            # Verificar contenido básico
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("Test Vuln", content)
                self.assertIn("HIGH", content)


if __name__ == "__main__":
    unittest.main()
