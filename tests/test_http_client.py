"""Pruebas unitarias para el cliente HTTP."""

import unittest
from unittest.mock import Mock, patch
import requests
from app.core.http import HTTPClient


class TestHTTPClient(unittest.TestCase):
    """Pruebas para HTTPClient."""
    
    def setUp(self):
        """Configuración antes de cada prueba."""
        self.client = HTTPClient(rate_limit=0.01)
    
    def tearDown(self):
        """Limpieza después de cada prueba."""
        self.client.close()
    
    @patch('app.core.http.requests.Session.get')
    def test_get_request(self, mock_get):
        """Verifica que se realice una petición GET."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        response = self.client.get("http://test.com")
        self.assertEqual(response.status_code, 200)
        mock_get.assert_called_once()
    
    @patch('app.core.http.requests.Session.post')
    def test_post_request(self, mock_post):
        """Verifica que se realice una petición POST."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        response = self.client.post("http://test.com", data={"key": "value"})
        self.assertEqual(response.status_code, 200)
        mock_post.assert_called_once()
    
    def test_rate_limit(self):
        """Verifica que el rate limiting funcione."""
        import time
        client = HTTPClient(rate_limit=0.5)
        
        start = time.time()
        # La primera petición no espera
        # La segunda sí debe esperar
        client._apply_rate_limit()
        time.sleep(0.1)  # Simular poco tiempo pasado
        client._apply_rate_limit()  # Esta debe esperar ~0.4s más
        elapsed = time.time() - start
        
        # No podemos medir exactamente, pero debe ser > 0.4
        self.assertGreater(elapsed, 0.4)
        client.close()


if __name__ == "__main__":
    unittest.main()
