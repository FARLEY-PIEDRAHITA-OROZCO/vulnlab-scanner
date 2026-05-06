"""Configuración centralizada para VulnLab Scanner."""

import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    """Clase de configuración centralizada.
    
    Los valores se leen de variables de entorno con valores por defecto.
    """
    
    # Configuración General
    DEBUG = os.getenv("DEBUG", "False") == "True"
    VERBOSE = os.getenv("VERBOSE", "False") == "True"
    
    # Configuración de HTTP
    RATE_LIMIT = float(os.getenv("RATE_LIMIT", "0.5"))  # Segundos entre peticiones
    HTTP_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
    USER_AGENT = os.getenv("USER_AGENT", "VulnLabScanner/1.4.2")
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    
    # Configuración de Autenticación
    DEFAULT_LOGIN_PATHS = os.getenv(
        "DEFAULT_LOGIN_PATHS", 
        "/login,/signin,/auth,/login.php"
    ).split(",")
    
    # Configuración de Access Control
    DEFAULT_ADMIN_PATHS = os.getenv(
        "DEFAULT_ADMIN_PATHS",
        "/admin,/administrator,/admin/users,/dashboard/admin"
    ).split(",")
    
    # Configuración de Escáneres
    DEFAULT_BRUTE_FORCE_ATTEMPTS = int(os.getenv("DEFAULT_BRUTE_FORCE_ATTEMPTS", "3"))
    DEFAULT_BRUTE_FORCE_PASSWORDS = os.getenv(
        "DEFAULT_BRUTE_FORCE_PASSWORDS",
        "123456,password,admin123,qwerty,letmein"
    ).split(",")
    
    # Directorios
    REPORTS_DIR = os.getenv("REPORTS_DIR", "reports")
