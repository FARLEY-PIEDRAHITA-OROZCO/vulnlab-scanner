"""Módulo de configuración centralizada para VulnLab Scanner.

Carga variables de entorno desde .env y define valores por defecto
para toda la aplicación.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Clase de configuración con valores por defecto y variables de entorno."""
    
    # Rate limiting (segundos entre peticiones)
    RATE_LIMIT = float(os.getenv("RATE_LIMIT", "0.5"))
    
    # Timeout para peticiones HTTP (segundos) - usa DEFAULT_TIMEOUT del .env
    HTTP_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
    
    # Directorio de salida de reportes
    REPORTS_DIR = os.getenv("REPORTS_DIR", "./reports")
    
    # Formato de reporte por defecto
    REPORT_FORMAT = os.getenv("REPORT_FORMAT", "ambos")
    
    # User-Agent para las peticiones - usa USER_AGENT del .env
    USER_AGENT = os.getenv(
        "USER_AGENT", 
        "VulnLabScanner/1.0"
    )
    
    # Número máximo de reintentos
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    
    # Modo debug/verbose - usa DEBUG del .env
    VERBOSE = os.getenv("DEBUG", "False").lower() == "true"
    
    @classmethod
    def display(cls):
        """Muestra la configuración actual (sin mostrar credenciales)."""
        from app.utils.logger import info
        info(f"Rate limit: {cls.RATE_LIMIT}s")
        info(f"HTTP timeout: {cls.HTTP_TIMEOUT}s")
        info(f"Reports dir: {cls.REPORTS_DIR}")
        info(f"Report format: {cls.REPORT_FORMAT}")
        info(f"User agent: {cls.USER_AGENT}")
