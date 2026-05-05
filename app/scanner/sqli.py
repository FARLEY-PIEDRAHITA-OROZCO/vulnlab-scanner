"""Módulo para detección de vulnerabilidades SQL Injection.

Este módulo implementa detección de:
- Error-based SQL Injection
- Boolean-based Blind SQL Injection

Basado en: OWASP Top 10 - A03: Injection
"""

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from app.scanner.base import BaseScanner
from app.utils.payloads import SQLI_PAYLOADS
from app.utils.logger import info, warning, success


class SQLiScanner(BaseScanner):
    """Escáner de vulnerabilidades SQL Injection.
    
    Detecta inyecciones SQL mediante la inyección de payloads
    y análisis de respuestas del servidor para detectar errores
    o diferencias en el comportamiento.
    """
    
    def __init__(self, target_url: str, session, dry_run: bool = False):
        """Inicializa el escáner SQLi.
        
        Args:
            target_url: URL de la aplicación a escanear.
            session: Sesión HTTP para realizar peticiones.
            dry_run: Si es True, solo simula sin atacar.
        """
        super().__init__(target_url, session, dry_run)
        self.payloads = self.get_payloads()
        self.error_indicators = [
            "sql syntax", "mysql error", "postgresql error",
            "oracle error", "sqlite error", "database error",
            "you have an error in your sql syntax"
        ]
    
    def get_payloads(self) -> list:
        """Retorna la lista de payloads para SQL Injection.
        
        Returns:
            Lista de payloads de tipo SQLi.
        """
        return SQLI_PAYLOADS
    
    def _inject_payload(self, url: str, param: str, payload: str) -> str:
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
    
    def _check_error_based(self, url: str, param: str, payload: dict) -> bool:
        """Verifica si un payload causa errores SQL visibles.
        
        Args:
            url: URL objetivo.
            param: Parámetro a probar.
            payload: Diccionario con el payload a inyectar.
            
        Returns:
            True si se detecta SQLi, False en caso contrario.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Probaría SQLi en '{param}' con: {payload['value']}")
            return False
        
        test_url = self._inject_payload(url, param, payload["value"])
        
        try:
            response = self.session.get(test_url)
            response_text = response.text.lower()
            
            # Buscar indicadores de error SQL en la respuesta
            for indicator in self.error_indicators:
                if indicator in response_text:
                    self.add_result(
                        vuln_name="Error-based SQL Injection",
                        severity="CRITICAL",
                        description=f"Se detectó SQL Injection basado en errores en '{param}'",
                        evidence=f"Payload: {payload['value']}, Indicador: {indicator}"
                    )
                    return True
                    
        except Exception as e:
            warning(f"Error al probar SQLi en {param}: {str(e)}")
        
        return False
    
    def _check_boolean_based(self, url: str, param: str, payload: dict) -> bool:
        """Verifica diferencias en respuestas para detectar SQLi ciego.
        
        Args:
            url: URL objetivo.
            param: Parámetro a probar.
            payload: Diccionario con el payload a inyectar.
            
        Returns:
            True si se detecta SQLi, False en caso contrario.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Probaría SQLi booleano en '{param}'")
            return False
        
        # Obtener respuesta base (sin payload)
        try:
            response_base = self.session.get(url)
            base_length = len(response_base.text)
            
            # Probar payload que debería ser verdadero (1=1)
            if "1=1" in payload["value"]:
                test_url = self._inject_payload(url, param, payload["value"])
                response_true = self.session.get(test_url)
                
                # Probar payload que debería ser falso (1=2)
                false_payload = payload["value"].replace("1=1", "1=2")
                test_url_false = self._inject_payload(url, param, false_payload)
                response_false = self.session.get(test_url_false)
                
                # Comparar longitudes de respuesta
                if abs(len(response_true.text) - len(response_false.text)) > 50:
                    self.add_result(
                        vuln_name="Boolean-based Blind SQL Injection",
                        severity="HIGH",
                        description=f"Se detectó SQL Injection ciego basado en booleanos en '{param}'",
                        evidence=f"Diferencia de respuesta detectada"
                    )
                    return True
                    
        except Exception as e:
            warning(f"Error al probar SQLi booleano en {param}: {str(e)}")
        
        return False
    
    def scan(self) -> list:
        """Ejecuta el escaneo de vulnerabilidades SQL Injection.
        
        Returns:
            Lista de diccionarios con resultados del escaneo.
        """
        self.display_scan_start()
        self.clear_results()
        
        parsed = urlparse(self.target_url)
        params = parse_qs(parsed.query)
        
        if not params:
            info("No hay parámetros en la URL para probar SQL Injection")
        else:
            info(f"Encontrados {len(params)} parámetros para probar")
            
            for param in params:
                info(f"Probando parámetro: {param}")
                
                for payload in self.payloads:
                    if payload["type"] == "error_based":
                        self._check_error_based(self.target_url, param, payload)
                    elif payload["type"] == "boolean_based":
                        self._check_boolean_based(self.target_url, param, payload)
        
        success(f"Escaneo SQLi completado. Vulnerabilidades encontradas: {len(self.results)}")
        return self.get_results()
