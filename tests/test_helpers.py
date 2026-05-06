"""Pruebas unitarias para helpers."""

import unittest
from app.utils.helpers import is_valid_url


class TestIsValidUrl(unittest.TestCase):
    """Pruebas para is_valid_url."""

    def test_valid_http_url(self):
        """URL HTTP válida."""
        self.assertTrue(is_valid_url("http://example.com"))

    def test_valid_https_url(self):
        """URL HTTPS válida."""
        self.assertTrue(is_valid_url("https://example.com/path?q=1"))

    def test_valid_url_with_port(self):
        """URL con puerto válida."""
        self.assertTrue(is_valid_url("http://localhost:8080"))

    def test_invalid_url_no_protocol(self):
        """URL sin protocolo."""
        self.assertFalse(is_valid_url("example.com"))

    def test_invalid_url_ftp(self):
        """Protocolo FTP no válido."""
        self.assertFalse(is_valid_url("ftp://example.com"))

    def test_invalid_url_empty(self):
        """URL vacía."""
        self.assertFalse(is_valid_url(""))

    def test_invalid_url_none(self):
        """None como entrada."""
        self.assertFalse(is_valid_url(""))


if __name__ == "__main__":
    unittest.main()
