"""Cliente HTTP wrapper para VulnLab Scanner.

Proporciona una interfaz segura para realizar peticiones HTTP
con manejo de errores, rate limiting y reintentos.
"""

import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from app.config import Config
from app.utils.logger import error, warning, info


class HTTPClient:
    """Cliente HTTP con rate limiting y manejo de errores.
    
    Attributes:
        session: Sesión de requests con configuración personalizada.
        rate_limit: Tiempo de espera entre peticiones (segundos).
    """
    
    def __init__(self, rate_limit: float = None):
        """Inicializa el cliente HTTP.
        
        Args:
            rate_limit: Tiempo entre peticiones. Si es None, usa Config.RATE_LIMIT.
        """
        self.rate_limit = rate_limit if rate_limit is not None else Config.RATE_LIMIT
        self.last_request_time = 0
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Crea una sesión de requests con configuración de reintentos.
        
        Returns:
            Sesión de requests configurada.
        """
        session = requests.Session()
        
        retry_strategy = Retry(
            total=Config.MAX_RETRIES,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        session.headers.update({
            "User-Agent": Config.USER_AGENT
        })
        
        return session
    
    def _apply_rate_limit(self):
        """Aplica rate limiting esperando el tiempo necesario."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit:
            time.sleep(self.rate_limit - time_since_last)
        
        self.last_request_time = time.time()
    
    def get(self, url: str, params: dict = None, **kwargs) -> requests.Response:
        """Realiza una petición GET con rate limiting.
        
        Args:
            url: URL objetivo.
            params: Parámetros de consulta.
            **kwargs: Argumentos adicionales para requests.
            
        Returns:
            Objeto Response de requests.
            
        Raises:
            requests.RequestException: Si la petición falla.
        """
        self._apply_rate_limit()
        
        try:
            timeout = kwargs.pop("timeout", Config.HTTP_TIMEOUT)
            response = self.session.get(url, params=params, timeout=timeout, **kwargs)
            return response
        except requests.exceptions.Timeout:
            error(f"Timeout en petición GET a {url}")
            raise
        except requests.exceptions.RequestException as e:
            error(f"Error en petición GET a {url}: {str(e)}")
            raise
    
    def post(self, url: str, data: dict = None, **kwargs) -> requests.Response:
        """Realiza una petición POST con rate limiting.
        
        Args:
            url: URL objetivo.
            data: Datos del formulario.
            **kwargs: Argumentos adicionales para requests.
            
        Returns:
            Objeto Response de requests.
        """
        self._apply_rate_limit()
        
        try:
            timeout = kwargs.pop("timeout", Config.HTTP_TIMEOUT)
            response = self.session.post(url, data=data, timeout=timeout, **kwargs)
            return response
        except requests.exceptions.Timeout:
            error(f"Timeout en petición POST a {url}")
            raise
        except requests.exceptions.RequestException as e:
            error(f"Error en petición POST a {url}: {str(e)}")
            raise
    
    def close(self):
        """Cierra la sesión HTTP."""
        self.session.close()
