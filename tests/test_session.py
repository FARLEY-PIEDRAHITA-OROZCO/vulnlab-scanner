"""Pruebas unitarias para ScannerSession."""

import unittest
from unittest.mock import Mock, patch
from app.core.session import ScannerSession


class TestScannerSession(unittest.TestCase):
    """Pruebas para la clase ScannerSession."""

    def setUp(self):
        """Configuración antes de cada prueba."""
        # Mockear HTTPClient para que devuelva un mock_client
        self.mock_client = Mock()
        with patch('app.core.session.HTTPClient', return_value=self.mock_client):
            self.session = ScannerSession()

    def test_initialization(self):
        """Verifica inicialización correcta."""
        self.assertIsNotNone(self.session)
        self.assertIsNotNone(self.session.http_client)
        self.assertFalse(self.session.is_authenticated)

    def test_login_success(self):
        """Verifica login exitoso."""
        # Configurar mock response para POST
        mock_response = Mock()
        mock_response.status_code = 302
        mock_response.url = "http://example.com/dashboard"
        self.mock_client.post.return_value = mock_response

        result = self.session.login("http://example.com/login", "user", "pass")
        self.assertTrue(result)
        self.assertTrue(self.session.is_authenticated)

    def test_login_failure(self):
        """Verifica login fallido."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = "http://example.com/login"
        self.mock_client.post.return_value = mock_response

        result = self.session.login("http://example.com/login", "user", "wrong")
        self.assertFalse(result)
        self.assertFalse(self.session.is_authenticated)

    def test_get_request(self):
        """Verifica petición GET."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "OK"
        self.mock_client.get.return_value = mock_response

        response = self.session.get("http://example.com")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "OK")

    def test_post_request(self):
        """Verifica petición POST."""
        mock_response = Mock()
        mock_response.status_code = 200
        self.mock_client.post.return_value = mock_response

        response = self.session.post("http://example.com", data={"key": "value"})
        self.assertEqual(response.status_code, 200)

    def test_close(self):
        """Verifica cierre de sesión."""
        self.mock_client.close = Mock()
        try:
            self.session.close()
            self.mock_client.close.assert_called_once()
        except Exception as e:
            self.fail(f"close() lanzó excepción: {e}")


if __name__ == "__main__":
    unittest.main()
