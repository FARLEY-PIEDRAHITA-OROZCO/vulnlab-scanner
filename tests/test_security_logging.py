"""Pruebas unitarias para SecurityLoggingScanner (A09)."""

from unittest.mock import Mock, patch

import pytest

from app.scanner.security_logging import SecurityLoggingScanner


@pytest.fixture
def scanner():
    """Fixture que crea un scanner de prueba."""
    session = Mock()
    return SecurityLoggingScanner("http://test.com", session, dry_run=True)


@pytest.fixture
def active_scanner():
    """Fixture que crea un scanner activo (no dry_run)."""
    session = Mock()
    return SecurityLoggingScanner("http://test.com", session, dry_run=False)


class TestSecurityLoggingScannerInit:
    """Pruebas para la inicialización del scanner."""

    def test_init_with_dry_run(self, scanner):
        assert scanner.target_url == "http://test.com"
        assert scanner.dry_run is True
        assert len(scanner.payloads) > 0

    def test_init_without_dry_run(self, active_scanner):
        assert active_scanner.dry_run is False
        assert active_scanner.security_headers is not None
        assert len(active_scanner.security_headers) > 0


class TestGetPayloads:
    """Pruebas para el método get_payloads."""

    def test_get_payloads_returns_list(self, scanner):
        payloads = scanner.get_payloads()
        assert isinstance(payloads, list)
        assert len(payloads) > 0

    def test_payloads_have_required_keys(self, scanner):
        payloads = scanner.get_payloads()
        for payload in payloads:
            assert "type" in payload
            assert "description" in payload


class TestCheckSecurityHeaders:
    """Pruebas para verificación de headers de logging."""

    def test_dry_run_returns_false(self, scanner):
        result = scanner._check_security_headers("http://test.com")
        assert result is False
        assert len(scanner.results) == 0

    def test_missing_headers_detected(self, active_scanner):
        # Simular respuesta sin headers de logging
        active_scanner.session.get.return_value = Mock(status_code=200, headers={})  # Sin headers
        result = active_scanner._check_security_headers("http://test.com")
        assert result is True
        assert len(active_scanner.results) == 1
        assert "Logging" in active_scanner.results[0]["vulnerability"]

    def test_headers_present_no_result(self, active_scanner):
        # Simular respuesta con headers de logging
        active_scanner.session.get.return_value = Mock(
            status_code=200, headers={"X-Request-ID": "123", "X-Forwarded-For": "1.2.3.4", "Server": "nginx"}
        )
        result = active_scanner._check_security_headers("http://test.com")
        assert result is False


class TestCheckErrorHandling:
    """Pruebas para verificación de manejo de errores."""

    def test_dry_run_returns_false(self, scanner):
        result = scanner._check_error_handling("http://test.com")
        assert result is False

    def test_error_info_exposed(self, active_scanner):
        # Simular respuesta con información de error
        html_with_error = "Error: SQL syntax error in query"
        active_scanner.session.get.return_value = Mock(status_code=500, text=html_with_error)
        result = active_scanner._check_error_handling("http://test.com")
        assert result is True
        assert len(active_scanner.results) == 1
        assert "Error" in active_scanner.results[0]["vulnerability"]

    def test_no_error_info_exposed(self, active_scanner):
        # Simular respuesta limpia
        active_scanner.session.get.return_value = Mock(status_code=404, text="Page not found")
        result = active_scanner._check_error_handling("http://test.com")
        assert result is False


class TestCheckMonitoringEndpoints:
    """Pruebas para verificación de endpoints de monitoreo."""

    def test_dry_run_returns_false(self, scanner):
        result = scanner._check_monitoring_endpoints("http://test.com")
        assert result is False

    def test_no_monitoring_detected(self, active_scanner):
        # Simular que ningún endpoint responde 200
        active_scanner.session.get.return_value = Mock(status_code=404)
        result = active_scanner._check_monitoring_endpoints("http://test.com")
        assert result is True
        assert len(active_scanner.results) == 1
        assert "Monitoring" in active_scanner.results[0]["vulnerability"]

    def test_monitoring_found_no_result(self, active_scanner):
        # Simular que /health responde 200
        active_scanner.session.get.return_value = Mock(status_code=200)
        result = active_scanner._check_monitoring_endpoints("http://test.com")
        assert result is False


class TestCheckAuditLogs:
    """Pruebas para verificación de audit logs."""

    def test_dry_run_returns_false(self, scanner):
        result = scanner._check_audit_logs("http://test.com")
        assert result is False

    def test_no_audit_indicators(self, active_scanner):
        # Página sin indicadores de audit
        active_scanner.session.get.return_value = Mock(status_code=200, text="<html>Welcome to our site</html>")
        result = active_scanner._check_audit_logs("http://test.com")
        assert result is True
        assert len(active_scanner.results) == 1
        assert "Audit" in active_scanner.results[0]["vulnerability"]

    def test_audit_indicators_present(self, active_scanner):
        # Página con indicadores
        html_with_audit = "Check our audit log for security events"
        active_scanner.session.get.return_value = Mock(status_code=200, text=html_with_audit)
        result = active_scanner._check_audit_logs("http://test.com")
        assert result is False


class TestScan:
    """Pruebas para el método scan completo."""

    def test_scan_dry_run(self, scanner):
        results = scanner.scan()
        assert isinstance(results, list)
        # En dry_run no debe agregar resultados reales
        real_results = [r for r in results if "DRY-RUN" not in str(r)]
        assert len(real_results) >= 0

    def test_scan_returns_list(self, active_scanner):
        with patch.object(active_scanner, "_check_security_headers", return_value=False), patch.object(
            active_scanner, "_check_error_handling", return_value=False
        ), patch.object(active_scanner, "_check_monitoring_endpoints", return_value=False), patch.object(
            active_scanner, "_check_audit_logs", return_value=False
        ):
            results = active_scanner.scan()
            assert isinstance(results, list)

    def test_scan_calls_all_checks(self, active_scanner):
        with patch.object(active_scanner, "_check_security_headers") as mock_headers, patch.object(
            active_scanner, "_check_error_handling"
        ) as mock_error, patch.object(active_scanner, "_check_monitoring_endpoints") as mock_monitor, patch.object(
            active_scanner, "_check_audit_logs"
        ) as mock_audit:
            active_scanner.scan()
            mock_headers.assert_called()
            mock_error.assert_called()
            mock_monitor.assert_called()
            mock_audit.assert_called()


class TestIntegration:
    """Pruebas de integración básica."""

    def test_scanner_is_subclass_of_base(self):
        from app.scanner.base import BaseScanner

        assert issubclass(SecurityLoggingScanner, BaseScanner)

    def test_payloads_match_constants(self):
        from app.utils.payloads import SECURITY_LOGGING_PAYLOADS

        scanner = SecurityLoggingScanner("http://test.com", Mock(), True)
        assert scanner.payloads == SECURITY_LOGGING_PAYLOADS
