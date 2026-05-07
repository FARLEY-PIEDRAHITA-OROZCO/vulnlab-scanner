"""Módulo para detección de Security Logging and Monitoring Failures (A09 - OWASP Top 10).

Este módulo implementa detección de:
- Ausencia de headers de logging de seguridad
- Falta de monitorización de eventos críticos
- Ausencia de audit logs para acciones sensibles
- Manejo inadecuado de errores de seguridad
"""

import re
from urllib.parse import urljoin, urlparse

from app.scanner.base import BaseScanner
from app.utils.logger import info, success, warning
from app.utils.payloads import SECURITY_LOGGING_PAYLOADS


class SecurityLoggingScanner(BaseScanner):
    """Escáner de Security Logging and Monitoring Failures (A09).

    Detecta fallos en el registro y monitoreo de eventos
    de seguridad que podrían impedir la detección de ataques.
    """

    def __init__(self, target_url: str, session, dry_run: bool = False):
        """Inicializa el escáner de Security Logging.

        Args:
            target_url: URL de la aplicación a escanear.
            session: Sesión HTTP para realizar peticiones.
            dry_run: Si es True, solo simula sin atacar.
        """
        super().__init__(target_url, session, dry_run)
        self.payloads = self.get_payloads()
        self.security_headers = [
            "X-Request-ID",
            "X-Correlation-ID",
            "X-Forwarded-For",
            "X-Real-IP",
            "Server",
            "X-Powered-By",
        ]

    def get_payloads(self) -> list:
        """Retorna la lista de payloads para Security Logging.

        Returns:
            Lista de payloads de tipo security logging.
        """
        return SECURITY_LOGGING_PAYLOADS

    def _check_security_headers(self, url: str) -> bool:
        """Verifica la presencia de headers de seguridad relacionados con logging.

        Args:
            url: URL para verificar headers.

        Returns:
            True si se detecta falta de headers, False en caso contrario.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Verificaría headers de logging en {url}")
            return False

        info(f"Verificando headers de logging en: {url}")

        try:
            response = self.session.get(url)
            headers = response.headers

            missing_headers = []
            for header in self.security_headers:
                if header not in headers:
                    missing_headers.append(header)

            if len(missing_headers) >= 4:  # Si faltan muchos headers de logging
                self.add_result(
                    vuln_name="Missing Security Logging Headers",
                    severity="MEDIUM",
                    description=f"Faltan headers de logging de seguridad: {', '.join(missing_headers[:3])}...",
                    evidence=f"Headers faltantes: {len(missing_headers)} de {len(self.security_headers)}",
                )
                return True

        except Exception as e:
            warning(f"Error al verificar headers: {str(e)}")

        return False

    def _check_error_handling(self, url: str) -> bool:
        """Verifica si los errores exponen información sensible.

        Args:
            url: URL para probar manejo de errores.

        Returns:
            True si se detecta mal manejo de errores, False en caso contrario.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Probaría manejo de errores en {url}")
            return False

        info(f"Verificando manejo de errores en: {url}")

        # Provocar un error (parámetro inválido)
        test_url = f"{url}?id=invalid_test_12345"

        try:
            response = self.session.get(test_url)

            # Buscar indicadores de error en la respuesta
            error_patterns = [
                r"(error|exception|traceback|stack trace)",
                r"(sql|syntax|query) error",
                r"(warning|notice|debug)",
            ]

            content_lower = response.text.lower()
            for pattern in error_patterns:
                if re.search(pattern, content_lower):
                    self.add_result(
                        vuln_name="Insecure Error Handling",
                        severity="LOW",
                        description="Manejo inseguro de errores: información sensible expuesta",
                        evidence=f"Patrón detectado: {pattern} en respuesta de error",
                    )
                    return True

        except Exception as e:
            warning(f"Error al probar manejo de errores: {str(e)}")

        return False

    def _check_monitoring_endpoints(self, url: str) -> bool:
        """Verifica si existen endpoints de monitoreo/health check.

        Args:
            url: URL base para verificar.

        Returns:
            True si no se detectan endpoints de monitoreo, False en caso contrario.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Verificaría endpoints de monitoreo en {url}")
            return False

        info("Verificando endpoints de monitoreo...")

        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        monitoring_paths = [
            "/health",
            "/healthz",
            "/metrics",
            "/status",
            "/monitoring",
            "/alerts",
        ]

        found_monitoring = False
        for path in monitoring_paths[:3]:  # Limitar pruebas
            test_url = urljoin(base_url, path)
            try:
                response = self.session.get(test_url)
                if response.status_code == 200:
                    found_monitoring = True
                    break
            except Exception:
                continue

        if not found_monitoring:
            self.add_result(
                vuln_name="Missing Monitoring Endpoints",
                severity="LOW",
                description="No se detectaron endpoints de monitoreo/health check",
                evidence=f"Probados: {', '.join(monitoring_paths[:3])}",
            )
            return True

        return False

    def _check_audit_logs(self, url: str) -> bool:
        """Verifica indicadores de audit logging para acciones críticas.

        Args:
            url: URL para verificar.

        Returns:
            True si se detecta falta de audit logs, False en caso contrario.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Analizaría audit logging en {url}")
            return False

        info("Verificando indicadores de audit logging...")

        # Verificar si hay referencias a logging en la página principal
        try:
            response = self.session.get(url)
            content_lower = response.text.lower()

            audit_indicators = ["audit", "log", "track", "monitor", "alert", "security event", "incident", "siem"]

            found_indicators = [ind for ind in audit_indicators if ind in content_lower]

            if len(found_indicators) < 2:
                self.add_result(
                    vuln_name="Missing Audit Log Indications",
                    severity="MEDIUM",
                    description="No se detectaron indicadores de audit logging",
                    evidence=f"Indicadores encontrados: {len(found_indicators)} de {len(audit_indicators)}",
                )
                return True

        except Exception as e:
            warning(f"Error al verificar audit logs: {str(e)}")

        return False

    def scan(self) -> list:
        """Ejecuta el escaneo de Security Logging and Monitoring Failures.

        Returns:
            Lista de diccionarios con resultados del escaneo.
        """
        self.display_scan_start()
        self.clear_results()

        info("Iniciando detección de Security Logging Failures (A09)")

        # 1. Verificar headers de logging
        info("Paso 1: Verificando headers de logging...")
        self._check_security_headers(self.target_url)

        # 2. Verificar manejo de errores
        info("Paso 2: Verificando manejo de errores...")
        self._check_error_handling(self.target_url)

        # 3. Verificar endpoints de monitoreo
        info("Paso 3: Verificando endpoints de monitoreo...")
        self._check_monitoring_endpoints(self.target_url)

        # 4. Verificar audit logging
        info("Paso 4: Verificando audit logging...")
        self._check_audit_logs(self.target_url)

        success(f"Escaneo A09 completado. Vulnerabilidades encontradas: {len(self.results)}")
        return self.get_results()
