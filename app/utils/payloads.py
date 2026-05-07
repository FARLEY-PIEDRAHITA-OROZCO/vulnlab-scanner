"""Payloas centralizados para todos los escáneres de vulnerabilidades.

Todos los vectores de ataque están organizados por categoría
para evitar hardcodear payloads en los módulos de escaneo.
"""

# Payloads para XSS (Cross-Site Scripting)
XSS_PAYLOADS = [
    # Reflected XSS
    {"type": "reflected", "value": "<script>alert('XSS')</script>"},
    {"type": "reflected", "value": "<img src=x onerror=alert('XSS')>"},
    {"type": "reflected", "value": "<svg/onload=alert('XSS')>"},
    {"type": "reflected", "value": "javascript:alert('XSS')"},
    {"type": "reflected", "value": "<body onload=alert('XSS')>"},
    # Stored XSS
    {"type": "stored", "value": "<script>alert('Stored XSS')</script>"},
    {"type": "stored", "value": "<img src=x onerror=alert('Stored XSS')>"},
    # DOM-based XSS
    {"type": "dom", "value": "#<script>alert('DOM XSS')</script>"},
    {"type": "dom", "value": "javascript:alert(document.cookie)"},
]

# Payloads para SQL Injection
SQLI_PAYLOADS = [
    # Error-based
    {"type": "error_based", "value": "' OR '1'='1"},
    {"type": "error_based", "value": "' OR 1=1--"},
    {"type": "error_based", "value": '" OR "1"="1'},
    {"type": "error_based", "value": "admin' --"},
    {"type": "error_based", "value": "admin' #"},
    # Boolean-based
    {"type": "boolean_based", "value": "' AND 1=1--"},
    {"type": "boolean_based", "value": "' AND 1=2--"},
    {"type": "boolean_based", "value": '" AND "1"="1'},
    # Time-based (futuro)
    {"type": "time_based", "value": "'; WAITFOR DELAY '00:00:05'--"},
]

# Headers de seguridad a verificar
HEADERS_CHECKS = [
    {"header": "Strict-Transport-Security", "recommendation": "max-age=31536000; includeSubDomains", "severity": "MEDIUM"},
    {"header": "X-Content-Type-Options", "recommendation": "nosniff", "severity": "LOW"},
    {"header": "X-Frame-Options", "recommendation": "DENY o SAMEORIGIN", "severity": "MEDIUM"},
    {"header": "Content-Security-Policy", "recommendation": "default-src 'self'", "severity": "HIGH"},
    {"header": "X-XSS-Protection", "recommendation": "1; mode=block", "severity": "LOW"},
    {"header": "Referrer-Policy", "recommendation": "strict-origin-when-cross-origin", "severity": "LOW"},
]

# Payloads para futuros escáneres
AUTH_PAYLOADS = [
    {"type": "weak_password", "value": "password123"},
    {"type": "weak_password", "value": "123456"},
    {"type": "default_creds", "value": "admin:admin"},
]

COMPONENTS_PAYLOADS = [
    {"type": "outdated_js", "description": "jQuery 1.x, Angular 1.x, etc."},
    {"type": "vulnerable_cdn", "description": "Bootstrap, React, etc. outdated"},
]

ACCESS_CONTROL_PAYLOADS = [
    {"type": "idor", "description": "Cambio de ID en URL (ej: /user/1 -> /user/2)"},
    {"type": "privilege_escalation", "description": "Acceso a rutas admin sin permisos"},
    {"type": "forceful_browsing", "description": "Saltos de flujo (ej: ir a /checkout sin pasar por /cart)"},
]

ACCESS_CONTROL_PAYLOADS = [
    {"type": "idor", "description": "Cambio de IDs en URL"},
    {"type": "privilege_escalation", "description": "Modificar rol en parámetros"},
]

# Payloads para A02 - Cryptographic Failures
CRYPTO_PAYLOADS = [
    {"type": "https_missing", "description": "El sitio no usa HTTPS"},
    {"type": "cookie_secure_missing", "description": "Cookies sin flag Secure"},
    {"type": "sensitive_in_url", "description": "Credenciales o tokens en la URL"},
    {"type": "weak_tls", "description": "Uso de TLS obsoleto (SSLv3, TLS 1.0/1.1)"},
]

# Payloads para A10 - SSRF (Server-Side Request Forgery)
SSRF_PAYLOADS = [
    {"type": "url_param", "param": "url", "test_value": "http://169.254.169.254/latest/meta-data/"},
    {"type": "url_param", "param": "redirect", "test_value": "http://localhost/"},
    {"type": "url_param", "param": "path", "test_value": "file:///etc/passwd"},
    {"type": "url_param", "param": "next", "test_value": "http://127.0.0.1/"},
    {"type": "dangerous_scheme", "scheme": "file://", "description": "Acceso a sistema de archivos"},
    {"type": "dangerous_scheme", "scheme": "dict://", "description": "Protocolo dict peligroso"},
]

# Payloads para A04 - Insecure Design
INSECURE_DESIGN_PAYLOADS = [
    {"type": "rate_limiting", "description": "Falta de rate limiting en endpoints"},
    {"type": "csrf_missing", "description": "Ausencia de tokens CSRF en formularios POST"},
    {"type": "input_validation", "description": "Falta validación de entrada en parámetros"},
    {"type": "insecure_flow", "description": "Flujos de diseño inseguros (ej: saltos de flujo)"},
    {"type": "idor_pattern", "description": "Patrones IDOR en diseño de APIs"},
    {"type": "missing_authorization", "description": "Falta verificación de autorización en flujos críticos"},
]

# Payloads para A09 - Security Logging and Monitoring Failures
SECURITY_LOGGING_PAYLOADS = [
    {"type": "missing_security_headers", "description": "Falta headers de logging (X-Request-ID, etc.)"},
    {"type": "insecure_error_handling", "description": "Errores exponen información sensible"},
    {"type": "missing_monitoring", "description": "Ausencia de endpoints de monitoreo (/health, /metrics)"},
    {"type": "missing_audit_logs", "description": "No hay indicadores de audit logging"},
    {"type": "no_siem_integration", "description": "Falta integración con SIEM"},
]
