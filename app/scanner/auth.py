"""Módulo para detección de Authentication Failures (A07 - OWASP Top 10).

Este módulo implementa detección de:
- Weak Passwords / Default Credentials
- Brute Force (suave, sin bloqueo)
- Session Management Issues (sesiones débiles)
"""

from app.scanner.base import BaseScanner
from app.utils.payloads import AUTH_PAYLOADS
from app.utils.logger import info, warning, success
from urllib.parse import urlparse
import re
import time


class AuthScanner(BaseScanner):
    """Escáner de fallos de autenticación.
    
    Detecta vulnerabilidades en mecanismos de autenticación
    que permitan accesos no autorizados.
    """
    
    def __init__(self, target_url: str, session, dry_run: bool = False):
        """Inicializa el escáner de Auth Failures.
        
        Args:
            target_url: URL de la aplicación a escanear.
            session: Sesión HTTP para realizar peticiones.
            dry_run: Si es True, solo simula sin atacar.
        """
        super().__init__(target_url, session, dry_run)
        self.payloads = self.get_payloads()
        self.login_paths = ["/login", "/signin", "/auth", "/login.php"]
    
    def get_payloads(self) -> list:
        """Retorna la lista de payloads para Auth Failures.
        
        Returns:
            Lista de payloads de tipo auth.
        """
        return AUTH_PAYLOADS
    
    def _test_weak_passwords(self, login_url: str) -> bool:
        """Prueba credenciales débiles o por defecto.
        
        Args:
            login_url: URL del formulario de login.
            
        Returns:
            True si se detecta acceso con credenciales débiles.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Probaría credenciales débiles en {login_url}")
            return False
        
        info(f"Probando credenciales débiles en: {login_url}")
        
        # Obtener página de login para CSRF tokens si existen
        try:
            login_page = self.session.get(login_url)
            
            # Payloads de credenciales por defecto
            weak_creds = [
                ("admin", "admin"),
                ("admin", "password"),
                ("test", "test"),
                ("user", "user"),
                ("administrator", "administrator")
            ]
            
            for username, password in weak_creds:
                login_data = {
                    "username": username,
                    "password": password
                }
                
                response = self.session.post(login_url, data=login_data)
                
                # Verificar si el login fue exitoso
                if response.status_code == 200 or response.status_code == 302:
                    if "login" not in response.url.lower():
                        self.add_result(
                            vuln_name="Weak/Default Credentials",
                            severity="CRITICAL",
                            description=f"Acceso con credenciales por defecto: {username}/{password}",
                            evidence=f"URL: {login_url} - Status: {response.status_code}"
                        )
                        return True
            
            info("No se encontraron credenciales por defecto")
            return False
            
        except Exception as e:
            warning(f"Error al probar credenciales débiles: {str(e)}")
            return False
    
    def _test_brute_force(self, login_url: str) -> bool:
        """Prueba fuerza bruta suave (3 intentos).
        
        Args:
            login_url: URL del formulario de login.
            
        Returns:
            True si se detecta falta de protección contra fuerza bruta.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Probaría fuerza bruta suave en {login_url}")
            return False
        
        info(f"Probando protección contra fuerza bruta en: {login_url}")
        
        try:
            # Hacer 3 intentos con credenciales incorrectas
            failed_attempts = 0
            
            for i in range(3):
                login_data = {
                    "username": f"test_user_{i}",
                    "password": "wrong_password"
                }
                
                response = self.session.post(login_url, data=login_data)
                
                # Si no hay captcha, bloqueo, o delay significativo
                if response.status_code == 200:
                    if "login" in response.url.lower() or "incorrect" in response.text.lower():
                        failed_attempts += 1
                        continue
            
            # Si todos los intentos fallaron normalmente (sin bloqueo)
            # podría indicar falta de protección
            if failed_attempts == 3:
                info("No se detectó protección contra fuerza bruta (3 intentos permitidos)")
                # No reportamos como vulnerabilidad automáticamente
                # ya que requiere análisis manual
                return False
            
            return False
            
        except Exception as e:
            warning(f"Error al probar fuerza bruta: {str(e)}")
            return False
    
    def _test_session_management(self, login_url: str) -> bool:
        """Verifica problemas en gestión de sesiones.
        
        Args:
            login_url: URL del formulario de login.
            
        Returns:
            True si se detectan problemas de sesión.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Probaría gestión de sesiones en {login_url}")
            return False
        
        info(f"Verificando gestión de sesiones en: {login_url}")
        
        try:
            # Login con credenciales de prueba
            login_data = {"username": "test", "password": "test123"}
            response = self.session.post(login_url, data=login_data)
            
            # Verificar headers de sesión
            cookies = response.cookies
            
            if cookies:
                # Verificar flags de cookies
                for cookie in cookies:
                    name = cookie.name.lower()
                    value = cookie.value
                    
                    # Verificar HttpOnly
                    if not cookie.has_nonstandard_attr('HttpOnly'):
                        self.add_result(
                            vuln_name="Session Cookie without HttpOnly",
                            severity="MEDIUM",
                            description=f"Cookie '{name}' no tiene flag HttpOnly",
                            evidence=f"Cookie: {name}={value}"
                        )
                    
                    # Verificar Secure
                    if not cookie.secure:
                        self.add_result(
                            vuln_name="Session Cookie without Secure",
                            severity="MEDIUM",
                            description=f"Cookie '{name}' no tiene flag Secure",
                            evidence=f"Cookie: {name}={value}"
                        )
            
            return len(self.results) > 0
            
        except Exception as e:
            warning(f"Error al verificar sesiones: {str(e)}")
            return False
    
    def scan(self) -> list:
        """Ejecuta el escaneo de Authentication Failures.
        
        Returns:
            Lista de diccionarios con resultados del escaneo.
        """
        self.display_scan_start()
        self.clear_results()
        
        info("Iniciando detección de Authentication Failures (A07)")
        
        # Determinar URL de login
        parsed = urlparse(self.target_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        login_url = None
        for path in self.login_paths:
            test_url = base_url + path
            try:
                response = self.session.get(test_url)
                if response.status_code == 200:
                    login_url = test_url
                    info(f"URL de login encontrada: {login_url}")
                    break
            except:
                continue
        
        if not login_url:
            # Usar la URL objetivo como login
            login_url = self.target_url
            info(f"Usando URL objetivo como login: {login_url}")
        
        # 1. Probar credenciales débiles
        info("Paso 1: Verificando credenciales débiles...")
        self._test_weak_passwords(login_url)
        
        # 2. Probar fuerza bruta suave
        info("Paso 2: Verificando protección contra fuerza bruta...")
        self._test_brute_force(login_url)
        
        # 3. Verificar gestión de sesiones
        info("Paso 3: Verificando gestión de sesiones...")
        self._test_session_management(login_url)
        
        success(f"Escaneo A07 completado. Vulnerabilidades encontradas: {len(self.results)}")
        return self.get_results()
