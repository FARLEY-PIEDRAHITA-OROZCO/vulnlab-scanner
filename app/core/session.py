"""Gestión de sesiones y autenticación para VulnLab Scanner.

Soporta login automático con credenciales y mantiene la sesión
activa durante todo el escaneo.
"""

import requests
from app.core.http import HTTPClient
from app.config import Config
from app.utils.logger import info, success, error, warning
from app.utils.helpers import is_valid_url


class ScannerSession:
    """Gestión de sesiones con soporte de autenticación.
    
    Attributes:
        http_client: Cliente HTTP con rate limiting.
        is_authenticated: Indica si el login fue exitoso.
        login_url: URL de la página de login.
    """
    
    def __init__(self, rate_limit: float = None):
        """Inicializa la sesión del escáner.
        
        Args:
            rate_limit: Tiempo entre peticiones (usa Config si es None).
        """
        self.http_client = HTTPClient(rate_limit)
        self.is_authenticated = False
        self.login_url = None
    
    def login(self, login_url: str, username: str, password: str,
              user_field: str = "username", pass_field: str = "password") -> bool:
        """Realiza login automático y mantiene la sesión.
        
        Args:
            login_url: URL de la página de login.
            username: Nombre de usuario.
            password: Contraseña.
            user_field: Nombre del campo de usuario en el formulario.
            pass_field: Nombre del campo de contraseña en el formulario.
            
        Returns:
            True si el login fue exitoso, False en caso contrario.
        """
        if not is_valid_url(login_url):
            error("La URL de login no es válida")
            return False
        
        self.login_url = login_url
        info(f"Intentando login en: {login_url}")
        
        try:
            # Obtener página de login para tokens CSRF si existen
            login_page = self.http_client.get(login_url)
            
            # Datos del formulario
            login_data = {
                user_field: username,
                pass_field: password
            }
            
            # Enviar credenciales
            response = self.http_client.post(login_url, data=login_data)
            
            # Verificar si el login fue exitoso
            if response.status_code == 200 or response.status_code == 302:
                # Verificación básica: si no hay redirección a login nuevamente
                if "login" not in response.url.lower():
                    self.is_authenticated = True
                    success("Login exitoso - Sesión iniciada")
                    return True
                else:
                    warning("Posible fallo de autenticación (redirigido a login)")
                    return False
            else:
                error(f"Login falló con código: {response.status_code}")
                return False
                
        except Exception as e:
            error(f"Error durante el login: {str(e)}")
            return False
    
    def get(self, url: str, params: dict = None, **kwargs) -> "requests.Response":
        """Realiza petición GET manteniendo la sesión.
        
        Args:
            url: URL objetivo.
            params: Parámetros de consulta.
            **kwargs: Argumentos adicionales.
            
        Returns:
            Objeto Response de requests.
        """
        return self.http_client.get(url, params, **kwargs)
    
    def post(self, url: str, data: dict = None, **kwargs) -> "requests.Response":
        """Realiza petición POST manteniendo la sesión.
        
        Args:
            url: URL objetivo.
            data: Datos del formulario.
            **kwargs: Argumentos adicionales.
            
        Returns:
            Objeto Response de requests.
        """
        return self.http_client.post(url, data, **kwargs)
    
    def close(self):
        """Cierra la sesión HTTP."""
        self.http_client.close()
        self.is_authenticated = False
        info("Sesión cerrada")
