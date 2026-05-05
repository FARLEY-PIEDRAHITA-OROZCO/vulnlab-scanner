"""Módulo para validación de HTTP Security Headers.

Verifica la presencia y configuración correcta de headers
de seguridad basados en las mejores prácticas de OWASP.

Basado en: OWASP Top 10 - A05: Security Misconfiguration
"""

from app.scanner.base import BaseScanner
from app.utils.payloads import HEADERS_CHECKS
from app.utils.logger import info, warning, success


class HeadersScanner(BaseScanner):
    """Escáner de configuración de HTTP Security Headers.
    
    Verifica que los headers de seguridad estén presentes
    y correctamente configurados para proteger la aplicación.
    """
    
    def __init__(self, target_url: str, session, dry_run: bool = False):
        """Inicializa el escáner de headers.
        
        Args:
            target_url: URL de la aplicación a escanear.
            session: Sesión HTTP para realizar peticiones.
            dry_run: Si es True, solo simula sin atacar.
        """
        super().__init__(target_url, session, dry_run)
        self.checks = self.get_payloads()
    
    def get_payloads(self) -> list:
        """Retorna la lista de verificaciones de headers.
        
        Returns:
            Lista de diccionarios con headers a verificar.
        """
        return HEADERS_CHECKS
    
    def scan(self) -> list:
        """Ejecuta la revisión de headers de seguridad.
        
        Returns:
            Lista de resultados de la revisión.
        """
        self.display_scan_start()
        self.clear_results()
        
        try:
            response = self.session.get(self.target_url)
            headers = dict(response.headers)
            
            checks = self.get_payloads()
            
            for check in self.progress_iter(checks, "Verificando headers"):
                header_name = check["header"]
                expected = check.get("expected")
                severity = check.get("severity", "MEDIUM")
                
                if header_name not in headers:
                    self.add_result(
                        f"Missing Header: {header_name}",
                        severity,
                        f"El encabezado {header_name} no está presente",
                        "Header faltante"
                    )
                elif expected and expected not in headers[header_name]:
                    self.add_result(
                        f"Weak Header: {header_name}",
                        severity,
                        f"El encabezado {header_name} tiene un valor débil",
                        f"Valor actual: {headers[header_name]}"
                    )
                else:
                        self.info(f"✓ {header_name} presente y correcto")
            
        except Exception as e:
            self.info(f"Error al obtener headers: {str(e)}")
        
        return self.get_results()
        
        try:
            info(f"Obteniendo headers de: {self.target_url}")
            response = self.session.get(self.target_url)
            headers = response.headers
            
            info(f"Verificando {len(self.checks)} headers de seguridad")
            
            for check in self.checks:
                header_name = check["header"]
                recommendation = check["recommendation"]
                severity = check["severity"]
                
                # Verificar si el header está presente
                header_found = None
                for actual_header in headers:
                    if actual_header.lower() == header_name.lower():
                        header_found = actual_header
                        break
                
                if not header_found:
                    self.add_result(
                        vuln_name=f"Missing Security Header: {header_name}",
                        severity=severity,
                        description=f"El header de seguridad '{header_name}' no está presente",
                        evidence=f"Recomendación: {recommendation}"
                    )
                else:
                    value = headers[header_found]
                    info(f"Header '{header_found}' presente: {value}")
                    
                    # Aquí se podrían agregar validaciones más específicas del valor
                    # Por ahora solo registramos que está presente
                    
        except Exception as e:
            warning(f"Error al obtener headers: {str(e)}")
        
        success(f"Validación de headers completada. Problemas encontrados: {len(self.results)}")
        return self.get_results()
