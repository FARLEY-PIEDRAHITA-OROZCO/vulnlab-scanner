"""Pruebas unitarias para la interfaz CLI."""

import unittest
from unittest.mock import patch, Mock
from app.cli import parse_args


class TestCliParseArgs(unittest.TestCase):
    """Pruebas para parse_args."""

    def test_default_values(self):
        """Verifica valores por defecto."""
        with patch('sys.argv', ['vulnlab-scan']):
            args = parse_args()
            self.assertFalse(args.xss)
            self.assertFalse(args.sqli)
            self.assertFalse(args.headers)
            self.assertFalse(args.access_control)
            self.assertFalse(args.auth)
            self.assertFalse(args.vuln_components)
            self.assertFalse(args.all)
            self.assertFalse(args.dry_run)
            self.assertTrue(args.report, 'ambos')
            self.assertTrue(args.output_dir, 'reports')

    def test_xss_flag(self):
        """Verifica flag -x/--xss."""
        with patch('sys.argv', ['vulnlab-scan', '-x', '-u', 'http://test.com']):
            args = parse_args()
            self.assertTrue(args.xss)

    def test_all_flag(self):
        """Verifica flag -a/--all."""
        with patch('sys.argv', ['vulnlab-scan', '-a', '-u', 'http://test.com']):
            args = parse_args()
            self.assertTrue(args.all)

    def test_url_required(self):
        """Verifica que URL es requerida."""
        with patch('sys.argv', ['vulnlab-scan', '--disclaimer']):
            args = parse_args()
            self.assertIsNone(args.url)

    def test_login_credentials(self):
        """Verifica flags de autenticación."""
        with patch('sys.argv', [
            'vulnlab-scan', '-u', 'http://test.com',
            '--login-url', 'http://test.com/login',
            '--username', 'admin', '--password', 'secret'
        ]):
            args = parse_args()
            self.assertEqual(args.login_url, 'http://test.com/login')
            self.assertEqual(args.username, 'admin')
            self.assertEqual(args.password, 'secret')

    def test_report_format(self):
        """Verifica formato de reporte."""
        with patch('sys.argv', ['vulnlab-scan', '-u', 'http://test.com', '--report', 'json']):
            args = parse_args()
            self.assertEqual(args.report, 'json')


if __name__ == '__main__':
    unittest.main()
