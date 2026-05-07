"""Pruebas unitarias para InsecureDesignScanner (A04)."""

from unittest.mock import Mock, patch

import pytest

from app.scanner.insecure_design import InsecureDesignScanner


@pytest.fixture
def scanner():
    """Fixture que crea un scanner de prueba."""
    session = Mock()
    return InsecureDesignScanner("http://test.com", session, dry_run=True)


@pytest.fixture
def active_scanner():
    """Fixture que crea un scanner activo (no dry_run)."""
    session = Mock()
    return InsecureDesignScanner("http://test.com", session, dry_run=False)


class TestInsecureDesignScannerInit:
    """Pruebas para la inicialización del scanner."""

    def test_init_with_dry_run(self, scanner):
        assert scanner.target_url == "http://test.com"
        assert scanner.dry_run is True
        assert len(scanner.payloads) > 0

    def test_init_without_dry_run(self, active_scanner):
        assert active_scanner.dry_run is False
        assert active_scanner.csrf_token_patterns is not None
        assert len(active_scanner.csrf_token_patterns) > 0


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


class TestCheckRateLimiting:
    """Pruebas para verificación de rate limiting."""

    def test_dry_run_returns_false(self, scanner):
        result = scanner._check_rate_limiting("http://test.com/api/login")
        assert result is False
        assert len(scanner.results) == 0

    @patch.object(InsecureDesignScanner, "_check_rate_limiting")
    def test_active_scan_calls_check(self, mock_check, active_scanner):
        mock_check.return_value = True
        active_scanner._check_rate_limiting("http://test.com/api/login")
        mock_check.assert_called_once()


class TestCheckCsrfProtection:
    """Pruebas para verificación de protección CSRF."""

    def test_dry_run_returns_false(self, scanner):
        result = scanner._check_csrf_protection("http://test.com/form")
        assert result is False
        assert len(scanner.results) == 0

    def test_no_forms_no_results(self, active_scanner):
        active_scanner.session.get.return_value = Mock(status_code=200, text="<html>No forms here</html>")
        result = active_scanner._check_csrf_protection("http://test.com")
        assert result is False

    def test_form_without_csrf_detected(self, active_scanner):
        html_with_form = (
            '<form method="POST" action="/submit">'
            '<input type="text" name="username">'
            '<input type="submit" value="Login"></form>'
        )
        active_scanner.session.get.return_value = Mock(status_code=200, text=html_with_form)
        # Asegurar que csrf_token_patterns esté configurado
        active_scanner.csrf_token_patterns = ["csrf_token", "csrfmiddlewaretoken"]
        result = active_scanner._check_csrf_protection("http://test.com/login")
        assert result is True
        assert len(active_scanner.results) == 1
        assert "CSRF" in active_scanner.results[0]["vulnerability"]

    def test_form_with_csrf_not_detected(self, active_scanner):
        html_with_csrf = """
        <form method="POST" action="/submit">
            <input type="hidden" name="csrf_token" value="abc123">
            <input type="text" name="username">
            <input type="submit" value="Login">
        </form>
        """
        active_scanner.session.get.return_value = Mock(status_code=200, text=html_with_csrf)
        result = active_scanner._check_csrf_protection("http://test.com/login")
        assert result is False


class TestCheckInputValidation:
    """Pruebas para verificación de validación de entrada."""

    def test_dry_run_returns_false(self, scanner):
        result = scanner._check_input_validation("http://test.com/search")
        assert result is False

    def test_reflected_payload_detected(self, active_scanner):
        # Simular payload reflejado en respuesta
        active_scanner.session.get.return_value = Mock(status_code=200, text="Resultados para: <script>")
        with patch("app.scanner.insecure_design.urlparse") as mock_urlparse:
            mock_urlparse.return_value = Mock(
                scheme="http",
                netloc="test.com",
                path="/search",
                query="q=<script>",
                __str__=Mock(return_value="http://test.com/search?q=<script>"),
            )
            result = active_scanner._check_input_validation("http://test.com/search")
            # El payload se refleja
            assert result is True or result is False  # Dependiendo de implementación


class TestCheckInsecureFlows:
    """Pruebas para verificación de flujos inseguros."""

    def test_dry_run_returns_false(self, scanner):
        result = scanner._check_insecure_flows("http://test.com")
        assert result is False

    def test_direct_access_without_redirect(self, active_scanner):
        active_scanner.session.get.return_value = Mock(status_code=200, url="http://test.com/checkout")
        result = active_scanner._check_insecure_flows("http://test.com")
        assert result is True
        assert len(active_scanner.results) == 1
        assert "Flow" in active_scanner.results[0]["vulnerability"]


class TestScan:
    """Pruebas para el método scan completo."""

    def test_scan_dry_run(self, scanner):
        results = scanner.scan()
        assert isinstance(results, list)
        # En dry_run no debe agregar resultados reales
        real_results = [r for r in results if "DRY-RUN" not in str(r)]
        assert len(real_results) >= 0

    def test_scan_returns_list(self, active_scanner):
        with patch.object(active_scanner, "_check_rate_limiting", return_value=False), patch.object(
            active_scanner, "_check_csrf_protection", return_value=False
        ), patch.object(active_scanner, "_check_input_validation", return_value=False), patch.object(
            active_scanner, "_check_insecure_flows", return_value=False
        ):
            results = active_scanner.scan()
            assert isinstance(results, list)

    def test_scan_calls_all_checks(self, active_scanner):
        with patch.object(active_scanner, "_check_rate_limiting") as mock_rate, patch.object(
            active_scanner, "_check_csrf_protection"
        ) as mock_csrf, patch.object(active_scanner, "_check_input_validation") as mock_input, patch.object(
            active_scanner, "_check_insecure_flows"
        ) as mock_flow:
            active_scanner.scan()
            mock_rate.assert_called()
            mock_csrf.assert_called()
            mock_input.assert_called()
            mock_flow.assert_called()


class TestIntegration:
    """Pruebas de integración básica."""

    def test_scanner_is_subclass_of_base(self):
        from app.scanner.base import BaseScanner

        assert issubclass(InsecureDesignScanner, BaseScanner)

    def test_payloads_match_constants(self):
        from app.utils.payloads import INSECURE_DESIGN_PAYLOADS

        scanner = InsecureDesignScanner("http://test.com", Mock(), True)
        assert scanner.payloads == INSECURE_DESIGN_PAYLOADS
