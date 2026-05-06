"""Módulo para detección de SSRF (A10 - OWASP Top 10).

Este módulo implementa detección de:
- SSRF via parámetros de URL (url, redirect, path, next, file)
- Intentos de acceso a IPs internas (localhost, 127.0.0.1, 192.168.x.x)
- Uso de esquemas peligrosos (file://, dict://, gopher://)
"""

from app.scanner.base import BaseScanner
from app.utils.payloads import SSRF_PAYLOADS
from app.utils.logger import info, warning, success
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import re


class SSRFScanner(BaseScanner):
    """Escáner de SSRF (Server-Side Request Forgery).
    
    Detecta vulnerabilidades que permitan al atacante
    hacer que el servidor realice peticiones a destinos arbitrarios.
    """
    
    def __init__(self, target_url: str, session, dry_run: bool = False):
        """Inicializa el escáner de SSRF.
        
        Args:
            target_url: URL de la aplicación a escanear.
            session: Sesión HTTP para realizar peticiones.
            dry_run: Si es True, solo simula sin atacar.
        """
        super().__init__(target_url, session, dry_run)
        self.payloads = self.get_payloads()
        self.internal_ips = [
            "127.0.0.1",
            "localhost",
            "169.254.169.254",  # AWS metadata
            "192.168.0.1",
            "10.0.0.1",
            "0.0.0.0",
        ]
        self.dangerous_schemes = ["file://", "dict://", "gopher://", "ftp://"]
    
    def get_payloads(self) -> list:
        """Retorna la lista de payloads para SSRF.
        
        Returns:
            Lista de payloads de tipo SSRF.
        """
        return SSRF_PAYLOADS
    
    def _get_url_params(self, url: str) -> dict:
        """Extrae los parámetros de la URL.
        
        Args:
            url: URL a analizar.
            
        Returns:
            Diccionario de parámetros.
        """
        parsed = urlparse(url)
        return parse_qs(parsed.query)
    
    def _inject_param(self, url: str, param: str, value: str) -> str:
        """Inyeta un valor en un parámetro de la URL.
        
        Args:
            url: URL original.
            param: Parámetro a inyectar.
            value: Valor a probar.
            
        Returns:
            URL modificada.
        """
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        params[param] = [value]
        
        new_query = urlencode(params, doseq=True)
        test_url = urlunparse((
            parsed.scheme, parsed.netloc, parsed.path,
            parsed.params, new_query, parsed.fragment
        ))
        return test_url
    
    def _test_ssrf_param(self, param: str, test_value: str) -> bool:
        """Prueba SSRF inyectando una URL en un parámetro.
        
        Args:
            param: Parámetro a probar.
            test_value: Valor a inyectar (URL interna).
            
        Returns:
            True si se detecta posible SSRF.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Probaría SSRF con param '{param}' = '{test_value}'")
            return False
        
        test_url = self._inject_param(self.target_url, param, test_value)
        
        try:
            info(f"Probando SSRF: {param}={test_value}")
            response = self.session.get(test_url)
            
            # Verificar si la respuesta contiene indicadores de SSRF
            # Esto es complejo, aquí hacemos detección básica
            if response.status_code == 200:
                # Si el contenido cambia significativamente, podría ser SSRF
                # En un escáner real se usaría un servidor controlado
                content = response.text.lower()
                
                # Buscar indicadores de que el servidor accedió a la URL
                indicators = [
                    "root:", "daemon:", "[boot loader]", "index of",
                    "localhost", "127.0.0.1", "internal", "metadata"
                ]
                
                for indicator in indicators:
                    if indicator in content:
                        self.add_result(
                            vuln_name="SSRF via Parameter",
                            severity="HIGH",
                            description=f"Posible SSRF detectado inyectando '{test_value}' en parámetro '{param}'",
                            evidence=f"URL: {test_url} - Indicador: {indicator}"
                        )
                        return True
            
            return False
            
        except Exception as e:
            warning(f"Error al probar SSRF: {str(e)}")
            return False
    
    def _test_ssrf_common_params(self) -> bool:
        """Prueba parámetros comunes que podrían ser vulnerables a SSRF.
        
        Returns:
            True si se detecta SSRF.
        """
        common_params = [
            "url", "redirect", "path", "next", "file", "document",
            "img", "image", "src", "link", "host", "port", "ip"
        ]
        
        if self.dry_run:
            info("[DRY-RUN] Probaría parámetros comunes para SSRF")
            return False
        
        found = False
        for param in self.progress_iter(common_params, "Probando parámetros SSRF"):
            # Probar con localhost
            if self._test_ssrf_param(param, "http://localhost/"):
                found = True
            
            # Probar con IP interna
            if self._test_ssrf_param(param, "http://169.254.169.254/latest/meta-data/"):
                found = True
        
        return found
    
    def _test_dangerous_schemes(self) -> bool:
        """Prueba esquemas peligrosos como file://, dict://, etc.
        
        Returns:
            True si se detecta uso de esquemas peligrosos.
        """
        if self.dry_run:
            info("[DRY-RUN] Probaría esquemas peligrosos (file://, dict://, ...)")
            return False
        
        found = False
        for scheme in self.dangerous_schemes:
            test_value = scheme + "localhost/"
            
            # Buscar parámetros en la URL actual
            params = self._get_url_params(self.target_url)
            
            if params:
                # Hay parámetros, probar inyectar en el primero
                first_param = list(params.keys())[0]
                test_url = self._inject_param(self.target_url, first_param, test_value)
            else:
                # No hay parámetros, omitir
                continue
            
            try:
                info(f"Probando esquema peligroso: {scheme}")
                response = self.session.get(test_url)
                
                # Si no da error, podría ser vulnerable
                if response.status_code == 200:
                    self.add_result(
                        vuln_name="Dangerous Scheme in URL",
                        severity="MEDIUM",
                        description=f"Posible uso de esquema peligroso: {scheme}",
                        evidence=f"URL probada: {test_url}"
                    )
                    found = True
                    
            except Exception as e:
                # Es normal que falle con esquemas como file://
                pass
        
        return found
    
    def scan(self) -> list:
        """Ejecuta el escaneo de SSRF.
        
        Returns:
            Lista de diccionarios con resultados del escaneo.
        """
        self.display_scan_start()
        self.clear_results()
        
        info("Iniciando detección de SSRF (A10)")
        
        # 1. Probar parámetros comunes
        info("Paso 1: Probando parámetros comunes para SSRF...")
        self._test_ssrf_common_params()
        
        # 2. Probar esquemas peligrosos
        info("Paso 2: Probando esquemas peligrosos...")
        self._test_dangerous_schemes()
        
        success(f"Escaneo A10 completado. Vulnerabilidades encontradas: {len(self.results)}")
        return self.get_results()
