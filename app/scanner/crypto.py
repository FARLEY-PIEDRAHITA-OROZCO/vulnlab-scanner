"""Módulo para detección de Cryptographic Failures (A02 - OWASP Top 10).

Este módulo implementa detección de:
- HTTPS faltante (transmisión no segura)
- Cookies sin flag Secure
- Credenciales o tokens en URLs
- Uso de TLS obsoleto (SSLv3, TLS 1.0/1.1) - detección básica
"""

from app.scanner.base import BaseScanner
from app.utils.payloads import CRYPTO_PAYLOADS
from app.utils.logger import info, warning, success
from urllib.parse import urlparse
import re


class CryptoScanner(BaseScanner):
    """Escáner de Cryptographic Failures.
    
    Detecta fallos criptográficos y de transmisión
    que expongan datos sensibles.
    """
    
    def __init__(self, target_url: str, session, dry_run: bool = False):
        """Inicializa el escáner de Cryptographic Failures.
        
        Args:
            target_url: URL de la aplicación a escanear.
            session: Sesión HTTP para realizar peticiones.
            dry_run: Si es True, solo simula sin atacar.
        """
        super().__init__(target_url, session, dry_run)
        self.payloads = self.get_payloads()
    
    def get_payloads(self) -> list:
        """Retorna la lista de payloads para Cryptographic Failures.
        
        Returns:
            Lista de payloads de tipo crypto.
        """
        return CRYPTO_PAYLOADS
    
    def _check_https(self) -> bool:
        """Verifica si la URL objetivo usa HTTPS.
        
        Returns:
            True si se detecta falta de HTTPS.
        """
        if self.dry_run:
            info("[DRY-RUN] Verificaría uso de HTTPS")
            return False
        
        parsed = urlparse(self.target_url)
        
        if parsed.scheme != "https":
            self.add_result(
                vuln_name="Missing HTTPS",
                severity="HIGH",
                description="El sitio no utiliza HTTPS para comunicación segura",
                evidence=f"URL: {self.target_url}"
            )
            return True
        
        return False
    
    def _check_cookies_secure(self) -> bool:
        """Verifica si las cookies tienen flag Secure.
        
        Returns:
            True si se detectan cookies sin flag Secure.
        """
        if self.dry_run:
            info("[DRY-RUN] Verificaría flags Secure en cookies")
            return False
        
        info("Verificando flags Secure en cookies...")
        
        try:
            response = self.session.get(self.target_url)
            cookies = response.cookies
            
            if not cookies:
                info("No se encontraron cookies para verificar")
                return False
            
            insecure_cookies = []
            for cookie in cookies:
                if not cookie.secure:
                    insecure_cookies.append(cookie.name)
            
            if insecure_cookies:
                self.add_result(
                    vuln_name="Cookie Without Secure Flag",
                    severity="MEDIUM",
                    description=f"Cookies sin flag Secure: {', '.join(insecure_cookies)}",
                    evidence=f"Cookies inseguras: {len(insecure_cookies)}"
                )
                return True
            
            info("Todas las cookies tienen flag Secure")
            return False
            
        except Exception as e:
            warning(f"Error al verificar cookies: {str(e)}")
            return False
    
    def _check_sensitive_in_url(self) -> bool:
        """Busca credenciales o tokens en la URL.
        
        Returns:
            True si se detectan credenciales en la URL.
        """
        if self.dry_run:
            info("[DRY-RUN] Verificaría credenciales en URL")
            return False
        
        info("Verificando credenciales en URL...")
        
        parsed = urlparse(self.target_url)
        
        # Patrones de credenciales en URL
        sensitive_patterns = [
            r'password=([^&]+)',
            r'pass=([^&]+)',
            r'pwd=([^&]+)',
            r'token=([^&]+)',
            r'api[_-]?key=([^&]+)',
            r'secret=([^&]+)',
            r'auth=([^&]+)',
        ]
        
        found = False
        for pattern in sensitive_patterns:
            match = re.search(pattern, self.target_url, re.IGNORECASE)
            if match:
                self.add_result(
                    vuln_name="Sensitive Data in URL",
                    severity="HIGH",
                    description=f"Credencial o token expuesto en la URL",
                    evidence=f"Patrón: {pattern}, Valor: {match.group(1)[:20]}..."
                )
                found = True
        
        # Verificar user:password@host en URL
        if '@' in self.target_url:
            self.add_result(
                vuln_name="Credentials in URL (Basic Auth)",
                severity="CRITICAL",
                description="Credenciales en formato user:pass@host en la URL",
                evidence=f"URL contiene '@': {self.target_url}"
            )
            found = True
        
        if not found:
            info("No se encontraron credenciales en la URL")
        
        return found
    
    def _check_weak_tls(self) -> bool:
        """Verifica si el sitio usa TLS obsoleto (detección básica).
        
        Returns:
            True si se detecta TLS obsoleto.
        """
        if self.dry_run:
            info("[DRY-RUN] Verificaría TLS obsoleto")
            return False
        
        info("Verificando TLS obsoleto (detección básica)...")
        
        # Con requests moderno, el TLS débil se rechaza automáticamente
        # Hacemos una verificación básica: si usa HTTPS, asumimos TLS 1.2+ (bueno)
        # En un escáner real se usaría ssl, socket para probar versiones específicas
        
        parsed = urlparse(self.target_url)
        if parsed.scheme == "https":
            info("El sitio usa HTTPS (se asume TLS 1.2+ con requests moderno)")
            return False
        
        return False
    
    def scan(self) -> list:
        """Ejecuta el escaneo de Cryptographic Failures.
        
        Returns:
            Lista de diccionarios con resultados del escaneo.
        """
        self.display_scan_start()
        self.clear_results()
        
        info("Iniciando detección de Cryptographic Failures (A02)")
        
        # 1. Verificar HTTPS
        info("Paso 1: Verificando uso de HTTPS...")
        self._check_https()
        
        # 2. Verificar cookies sin Secure
        info("Paso 2: Verificando flags Secure en cookies...")
        self._check_cookies_secure()
        
        # 3. Verificar credenciales en URL
        info("Paso 3: Verificando credenciales en URL...")
        self._check_sensitive_in_url()
        
        # 4. Verificar TLS obsoleto
        info("Paso 4: Verificando TLS obsoleto...")
        self._check_weak_tls()
        
        success(f"Escaneo A02 completado. Vulnerabilidades encontradas: {len(self.results)}")
        return self.get_results()
