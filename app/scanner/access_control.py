"""Módulo para detección de Broken Access Control (A01 - OWASP Top 10).

Este módulo implementa detección de:
- IDOR (Insecure Direct Object References)
- Privilege Escalation (escalación de privilegios)
- Forceful Browsing (saltos de autenticación)
"""

from app.scanner.base import BaseScanner
from app.utils.payloads import ACCESS_CONTROL_PAYLOADS
from app.utils.logger import info, warning, success
from urllib.parse import urlparse, urlunparse, parse_qs
import re


class AccessControlScanner(BaseScanner):
    """Escáner de Broken Access Control.
    
    Detecta fallos en el control de acceso que permitan
    a usuarios acceder a recursos no autorizados mediante
    manipulación de URLs, IDs o saltos de flujo.
    """
    
    def __init__(self, target_url: str, session, dry_run: bool = False):
        """Inicializa el escáner de Access Control.
        
        Args:
            target_url: URL de la aplicación a escanear.
            session: Sesión HTTP para realizar peticiones.
            dry_run: Si es True, solo simula sin atacar.
        """
        super().__init__(target_url, session, dry_run)
        self.payloads = self.get_payloads()
        self.tested_urls = []
    
    def get_payloads(self) -> list:
        """Retorna la lista de payloads para Access Control.
        
        Returns:
            Lista de payloads de tipo access control.
        """
        return ACCESS_CONTROL_PAYLOADS
    
    def _extract_ids_from_url(self, url: str) -> list:
        """Extrae posibles IDs numéricos de una URL.
        
        Args:
            url: URL a analizar.
            
        Returns:
            Lista de tuplas (posición, valor_original, valor_prueba).
        """
        results = []
        parsed = urlparse(url)
        
        # Buscar IDs en el path (/user/123/profile)
        path_ids = re.findall(r'/(\d+)(?=/|$)', parsed.path)
        for id_val in path_ids:
            new_id = str(int(id_val) + 1)  # Probar ID siguiente
            results.append(("path", id_val, new_id))
        
        # Buscar IDs en parámetros (?id=123)
        params = parse_qs(parsed.query)
        for param, values in params.items():
            for val in values:
                if val.isdigit():
                    new_val = str(int(val) + 1)
                    results.append(("param", val, new_val))
        
        return results
    
    def _inject_id(self, url: str, original_val: str, test_val: str, id_type: str) -> str:
        """Inyeta un ID de prueba en la URL.
        
        Args:
            url: URL original.
            original_val: Valor original del ID.
            test_val: Valor a probar.
            id_type: 'path' o 'param'.
            
        Returns:
            URL con el ID modificado.
        """
        parsed = urlparse(url)
        
        if id_type == "path":
            new_path = re.sub(rf'/{original_val}(?=/|$)', f'/{test_val}', parsed.path)
            test_url = urlunparse((
                parsed.scheme, parsed.netloc, new_path,
                parsed.params, parsed.query, parsed.fragment
            ))
        else:  # param
            params = parse_qs(parsed.query)
            params[original_val] = test_val
            new_query = '&'.join([f'{k}={v}' for k, v in params.items()])
            test_url = urlunparse((
                parsed.scheme, parsed.netloc, parsed.path,
                parsed.params, new_query, parsed.fragment
            ))
        
        return test_url
    
    def _test_idor(self, url: str, id_type: str, original_val: str, test_val: str) -> bool:
        """Prueba IDOR modificando IDs en la URL.
        
        Args:
            url: URL objetivo.
            id_type: 'path' o 'param'.
            original_val: Valor original del ID.
            test_val: Valor a probar.
            
        Returns:
            True si se detecta IDOR, False en caso contrario.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Probaría IDOR con ID: {original_val} -> {test_val}")
            return False
        
        test_url = self._inject_id(url, original_val, test_val, id_type)
        
        try:
            response = self.session.get(test_url)
            
            # Si la respuesta es exitosa (200) y similar a la original
            # podría indicar acceso no autorizado
            if response.status_code == 200:
                # Verificar que no sea una página de login
                if "login" not in response.url.lower():
                    self.add_result(
                        vuln_name="IDOR (Insecure Direct Object Reference)",
                        severity="HIGH",
                        description=f"Posible IDOR detectado al cambiar ID de {original_val} a {test_val}",
                        evidence=f"URL probada: {test_url} - Status: 200"
                    )
                    return True
                    
        except requests.exceptions.RequestException as e:
            warning(f"Error al probar IDOR: {str(e)}")
        
        return False
    
    def _test_privilege_escalation(self, url: str) -> bool:
        """Prueba escalación de privilegios verificando acceso a rutas administrativas.
        
        Args:
            url: URL base objetivo.
            
        Returns:
            True si se detecta escalación, False en caso contrario.
        """
        from app.config import Config
        admin_paths = Config.DEFAULT_ADMIN_PATHS
        
        if self.dry_run:
            info(f"[DRY-RUN] Probaría rutas administrativas en {url}")
            return False
        
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        for path in self.progress_iter(admin_paths, "Probando rutas administrativas"):
            test_url = base_url + path
            try:
                response = self.session.get(test_url)
                
                # Si accede sin redirección a login
                if response.status_code == 200:
                    if "login" not in response.url.lower():
                        self.add_result(
                            vuln_name="Privilege Escalation",
                            severity="CRITICAL",
                            description=f"Acceso no autorizado a ruta administrativa: {path}",
                            evidence=f"URL: {test_url} - Status: {response.status_code}"
                        )
                        return True
                    
            except requests.exceptions.RequestException as e:
                warning(f"Error al probar escalación: {str(e)}")
        
        return False
    
    def scan(self) -> list:
        """Ejecuta el escaneo de Broken Access Control.
        
        Returns:
            Lista de diccionarios con resultados del escaneo.
        """
        self.display_scan_start()
        self.clear_results()
        
        info("Iniciando detección de Broken Access Control (A01)")
        
        # 1. Probar IDOR (cambio de IDs)
        info("Paso 1: Verificando IDOR...")
        ids = self._extract_ids_from_url(self.target_url)
        
        if ids:
            info(f"Encontrados {len(ids)} IDs para probar IDOR")
            for id_type, original_val, test_val in self.progress_iter(ids[:5], "Probando IDOR"):  # Limitar a 5 pruebas
                self._test_idor(self.target_url, id_type, original_val, test_val)
        else:
            info("No se encontraron IDs numéricos para probar IDOR")
        
        # 2. Probar escalación de privilegios
        info("Paso 2: Verificando escalación de privilegios...")
        self._test_privilege_escalation(self.target_url)
        
        success(f"Escaneo A01 completado. Vulnerabilidades encontradas: {len(self.results)}")
        return self.get_results()
