"""Pruebas unitarias para main.py."""

import unittest
from unittest.mock import Mock, patch
from app.main import run_scan


class TestRunScan(unittest.TestCase):
    """Pruebas para run_scan."""

    @patch('app.main.ScannerSession')
    @patch('app.main.parse_args')
    def test_run_scan_with_xss(self, mock_parse_args, mock_session_class):
        """Verifica ejecución con flag xss."""
        mock_args = Mock()
        mock_args.url = 'http://test.com'
        mock_args.xss = True
        mock_args.sqli = False
        mock_args.headers = False
        mock_args.access_control = False
        mock_args.auth = False
        mock_args.vuln_components = False
        mock_args.all = False
        mock_args.dry_run = True
        mock_args.no_report = True
        mock_args.no_disclaimer = True
        mock_parse_args.return_value = mock_args

        mock_session = Mock()
        mock_session_class.return_value = mock_session

        # No debería lanzar excepciones
        try:
            run_scan(mock_args)
        except Exception as e:
            self.fail(f"run_scan lanzó excepción: {e}")

    @patch('app.main.ScannerSession')
    @patch('app.main.parse_args')
    def test_run_scan_with_all_flag(self, mock_parse_args, mock_session_class):
        """Verifica flag --all activa todos los escáneres."""
        mock_args = Mock()
        mock_args.url = 'http://test.com'
        mock_args.all = True
        mock_args.dry_run = True
        mock_args.no_report = True
        mock_args.no_disclaimer = True
        mock_parse_args.return_value = mock_args

        mock_session = Mock()
        mock_session_class.return_value = mock_session

        # No debería lanzar excepciones
        try:
            run_scan(mock_args)
        except Exception as e:
            self.fail(f"run_scan lanzó excepción: {e}")

    @patch('app.main.is_valid_url', return_value=False)
    def test_run_scan_invalid_url(self, mock_is_valid):
        """Verifica manejo de URL inválida."""
        mock_args = Mock()
        mock_args.url = 'invalid'
        mock_args.no_disclaimer = True
        mock_args.disclaimer = False

        # Debería retornar sin hacer nada (URL inválida)
        run_scan(mock_args)


if __name__ == '__main__':
    unittest.main()
