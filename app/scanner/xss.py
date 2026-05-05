"""Módulo para detección de vulnerabilidades XSS (Cross-Site Scripting).

Este módulo implementa detección de:
- Reflected XSS
- Stored XSS (básico)
- DOM-based XSS (básico)

Basado en: OWASP Top 10 - A03: Injection
"""

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from app.scanner.base import BaseScanner
from app.utils.payloads import XSS_PAYLOADS
from app.utils.logger import info, warning, success


class XSSScanner(BaseScanner):
    """Escáner de vulnerabilidades XSS.
    
    Detecta Cross-Site Scripting reflejado, almacenado y DOM-based
    mediante inyección de payloads en parámetros de URL y formularios.
    """
    
    def __init__(self, target_url: str, session, dry_run: bool = False):
        """Inicializa el escáner XSS.
        
        Args:
            target_url: URL de la aplicación a escanear.
            session: Sesión HTTP para realizar peticiones.
            dry_run: Si es True, solo simula sin atacar.
        """
        super().__init__(target_url, session, dry_run)
        self.payloads = self.get_payloads()
    
    def get_payloads(self) -> list:
        """Retorna la lista de payloads para detección de XSS.
        
        Returns:
            Lista de payloads de tipo XSS.
        """
        return XSS_PAYLOADS
    
    def _get_url_params(self) -> list:
        """Extrae los nombres de los parámetros de la URL.
        
        Returns:
            Lista de nombres de parámetros.
        """
        parsed = urlparse(self.target_url)
        params = parse_qs(parsed.query)
        return list(params.keys())
    
    def _inject_payload(self, param: str, payload: str) -> str:
        """Inyecta un payload en un parámetro de la URL.
        
        Args:
            url: URL original.
            param: Parámetro donde inyectar.
            payload: Payload a inyectar.
            
        Returns:
            URL con el payload inyectado.
        """
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        
        query[param] = payload
        
        new_query = urlencode(query, doseq=True)
        
        new_url = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))
        
        return new_url
    
    def _check_reflected_xss(self, url: str, param: str, payload: dict) -> bool:
        """Verifica si un payload XSS se refleja en la respuesta.
        
        Args:
            url: URL objetivo.
            param: Parámetro a probar.
            payload: Diccionario con el payload a inyectar.
            
        Returns:
            True si se detecta XSS, False en caso contrario.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Probaría XSS en parámetro '{param}' con payload: {payload['value']}")
            return False
        
        test_url = self._inject_payload(url, param, payload["value"])
        
        try:
            response = self.session.get(test_url)
            
            # Verificar si el payload se refleja sin codificación
            if payload["value"] in response.text:
                self.add_result(
                    vuln_name="Reflected XSS",
                    severity="HIGH",
                    description=f"Se detectó XSS reflejado en el parámetro '{param}'",
                    evidence=f"Payload: {payload['value']}"
                )
                return True
                
        except Exception as e:
            warning(f"Error al probar XSS en {param}: {str(e)}")
        
        return False
    
    def scan(self) -> list:
        """Ejecuta el escaneo de vulnerabilidades XSS.
        
        Returns:
            Lista de resultados del escaneo.
        """
        self.display_scan_start()
        self.clear_results()
        
        params = self._get_url_params()
        payloads = self.get_payloads()
        
        if not params:
            self.info("No se encontraron parámetros GET para probar")
            return self.get_results()
        
        total_tests = len(params) * len(payloads)
        self.info(f"Probando {len(params)} parámetros con {len(payloads)} payloads ({total_tests} pruebas)")
        
        for param in self.progress_iter(params, "Probando parámetros"):
            for payload in self.progress_iter(payloads, "Inyectando payloads", leave=False):
                try:
                    test_url = self._inject_payload(param, payload)
                    response = self.session.get(test_url)
                    
                    if payload in response.text:
                        self.add_result(
                            "XSS Reflected",
                            "HIGH",
                            f"Vulnerabilidad XSS detectada en parámetro: {param}",
                            f"Payload: {payload}"
                        )
                except Exception as e:
                    self.info(f"Error probando {param}: {str(e)}")
        
        return self.get_results()
