"""Módulo para detección de Insecure Design (A04 - OWASP Top 10).

Este módulo implementa detección de:
- Falta de rate limiting en endpoints críticos
- Ausencia de validación de entrada en flujos críticos
- Falta de tokens CSRF en operaciones state-changing
- Patrones de diseño inseguro (IDOR, flujos sin validación)
"""

import re
from urllib.parse import urljoin, urlparse

from app.config import Config
from app.scanner.base import BaseScanner
from app.utils.logger import info, success, warning
from app.utils.payloads import INSECURE_DESIGN_PAYLOADS


class InsecureDesignScanner(BaseScanner):
    """Escáner de Insecure Design (A04).

    Detecta fallos de diseño que pueden llevar a vulnerabilidades
    incluso con implementación perfecta. Se enfoca en patrones
    arquitectónicos inseguros.
    """

    def __init__(self, target_url: str, session, dry_run: bool = False):
        """Inicializa el escáner de Insecure Design.

        Args:
            target_url: URL de la aplicación a escanear.
            session: Sesión HTTP para realizar peticiones.
            dry_run: Si es True, solo simula sin atacar.
        """
        super().__init__(target_url, session, dry_run)
        self.payloads = self.get_payloads()
        self.csrf_token_patterns = Config.CSRF_TOKEN_PATTERNS

    def get_payloads(self) -> list:
        """Retorna la lista de payloads para Insecure Design.

        Returns:
            Lista de payloads de tipo insecure design.
        """
        return INSECURE_DESIGN_PAYLOADS

    def _check_rate_limiting(self, url: str) -> bool:
        """Verifica si un endpoint tiene rate limiting.

        Args:
            url: URL del endpoint a probar.

        Returns:
            True si se detecta falta de rate limiting, False en caso contrario.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Probaría rate limiting en {url}")
            return False

        info(f"Verificando rate limiting en: {url}")

        # Probar múltiples peticiones rápidas
        try:
            responses = []
            for _ in range(10):  # Enviar 10 peticiones rápidas
                response = self.session.get(url)
                responses.append(response.status_code)

            # Si todas son 200, probablemente no hay rate limiting
            if responses.count(200) == 10:
                self.add_result(
                    vuln_name="Missing Rate Limiting",
                    severity="MEDIUM",
                    description=f"Endpoint sin rate limiting detectado: {url}",
                    evidence="10 peticiones enviadas, todas retornaron 200",
                )
                return True

        except Exception as e:
            warning(f"Error al probar rate limiting: {str(e)}")

        return False

    def _check_csrf_protection(self, url: str) -> bool:
        """Verifica si los formularios tienen protección CSRF.

        Args:
            url: URL para verificar formularios.

        Returns:
            True si se detecta falta de protección CSRF, False en caso contrario.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Verificaría CSRF en formularios de {url}")
            return False

        info(f"Verificando protección CSRF en: {url}")

        try:
            response = self.session.get(url)
            content = response.text.lower()

            # Buscar formularios (patrón más robusto)
            form_pattern = r"<form[^>]*>.*?</form>"
            forms = re.findall(form_pattern, content, re.DOTALL | re.IGNORECASE)

            for form in forms:
                form_lower = form.lower()
                has_csrf = False

                # Verificar patrones de CSRF token
                for pattern in self.csrf_token_patterns:
                    if pattern.lower() in form_lower:
                        has_csrf = True
                        break

                # Verificar método POST (más crítico)
                method_match = re.search(r'method\s*=\s*["\']?post["\']?', form, re.IGNORECASE)

                if not has_csrf and method_match:
                    self.add_result(
                        vuln_name="Missing CSRF Protection",
                        severity="HIGH",
                        description="Formulario POST sin protección CSRF detectado",
                        evidence="URL: %s - Formulario sin token CSRF" % url,
                    )
                    return True

        except Exception as e:
            warning(f"Error al verificar CSRF: {str(e)}")

        return False

    def _check_input_validation(self, url: str) -> bool:
        """Verifica validación de entrada en parámetros.

        Args:
            url: URL para probar validación.

        Returns:
            True si se detecta falta de validación, False en caso contrario.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Probaría validación de entrada en {url}")
            return False

        info(f"Verificando validación de entrada en: {url}")

        # Payloads de prueba
        test_payloads = [
            ("<script>", "XSS-like input"),
            ("'", "SQL-like input"),
            ("../../etc/passwd", "Path traversal"),
            ("${7*7}", "Template injection"),
        ]

        parsed = urlparse(url)
        test_url = f"{parsed.scheme}://{parsed.netloc}/search?q={{payload}}"

        for payload, desc in test_payloads[:2]:  # Limitar pruebas
            try:
                test_url_final = test_url.replace("{payload}", payload)
                response = self.session.get(test_url_final)

                # Si el payload se refleja sin codificar
                if payload in response.text:
                    self.add_result(
                        vuln_name="Missing Input Validation",
                        severity="MEDIUM",
                        description=f"Falta validación de entrada: {desc}",
                        evidence=f"Payload '{payload}' se refleja en respuesta",
                    )
                    return True

            except Exception as e:
                warning(f"Error al probar validación: {str(e)}")

        return False

    def _check_insecure_flows(self, url: str) -> bool:
        """Verifica flujos de diseño inseguros.

        Args:
            url: URL base para verificar.

        Returns:
            True si se detectan flujos inseguros, False en caso contrario.
        """
        if self.dry_run:
            info(f"[DRY-RUN] Analizaría flujos de diseño en {url}")
            return False

        info("Verificando flujos de diseño inseguros...")

        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        # Verificar saltos de flujo (ej: ir a checkout sin cart)
        insecure_flows = [
            "/checkout",
            "/payment",
            "/admin",
            "/profile/edit",
        ]

        for flow in insecure_flows[:2]:  # Limitar pruebas
            test_url = base_url + flow
            try:
                response = self.session.get(test_url, allow_redirects=False)

                # Si permite acceso directo sin redirección
                if response.status_code == 200:
                    if "login" not in response.url.lower():
                        self.add_result(
                            vuln_name="Insecure Design Flow",
                            severity="MEDIUM",
                            description=f"Acceso directo a flujo sin validación: {flow}",
                            evidence=f"URL: {test_url} - Acceso permitido sin validación de flujo",
                        )
                        return True

            except Exception as e:
                warning(f"Error al verificar flujo: {str(e)}")

        return False

    def scan(self) -> list:
        """Ejecuta el escaneo de Insecure Design.

        Returns:
            Lista de diccionarios con resultados del escaneo.
        """
        self.display_scan_start()
        self.clear_results()

        info("Iniciando detección de Insecure Design (A04)")

        # 1. Verificar rate limiting en endpoints comunes
        info("Paso 1: Verificando rate limiting...")
        rate_limit_endpoints = [
            self.target_url,
            urljoin(self.target_url, "/login"),
            urljoin(self.target_url, "/api/"),
        ]

        for endpoint in self.progress_iter(rate_limit_endpoints, "Rate limiting"):
            self._check_rate_limiting(endpoint)

        # 2. Verificar protección CSRF
        info("Paso 2: Verificando protección CSRF...")
        self._check_csrf_protection(self.target_url)

        # 3. Verificar validación de entrada
        info("Paso 3: Verificando validación de entrada...")
        self._check_input_validation(self.target_url)

        # 4. Verificar flujos de diseño inseguros
        info("Paso 4: Verificando flujos de diseño...")
        self._check_insecure_flows(self.target_url)

        success(f"Escaneo A04 completado. Vulnerabilidades encontradas: {len(self.results)}")
        return self.get_results()
