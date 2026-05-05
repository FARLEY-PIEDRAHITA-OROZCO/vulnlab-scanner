# Interfaces y Contratos - VulnLab Scanner

## 1. Interfaz de Línea de Comandos (CLI)

### 1.1 Argumentos Principales
```bash
python -m app.main [OPCIONES]

Opciones:
  -u, --url URL          URL objetivo (obligatorio)
  -x, --xss              Ejecutar escaneo XSS
  -s, --sqli             Ejecutar escaneo SQL Injection
  -H, --headers          Validar HTTP Headers
  -a, --all              Ejecutar todos los escáneres disponibles
  
Opciones de autenticación:
  --login-url URL        URL de la página de login
  --username USER        Usuario para autenticación
  --password PASS        Contraseña para autenticación
  --login-username-field NAME   Nombre del campo usuario (default: username)
  --login-password-field NAME   Nombre del campo password (default: password)
  
Opciones de reporte:
  --report-format FMT    Formato de reporte: json, html, ambos (default: ambos)
  --report-output DIR    Directorio de salida (default: ./reports)
  
Opciones adicionales:
  --dry-run              Solo simular, no enviar ataques reales
  --rate-limit SEC       Segundos entre peticiones (default: 0.5)
  --disclaimer           Mostrar aviso legal y salir
  -v, --verbose          Modo verbose (más detalles)
  -h, --help             Mostrar ayuda
```

## 2. Interfaz de Escáneres (BaseScanner)

Todos los módulos en `app/scanner/` deben implementar esta interfaz:

### 2.1 Métodos Obligatorios

#### `scan() -> list`
Ejecuta el escaneo y retorna resultados.
```python
def scan(self) -> list:
    """Ejecuta el escaneo de vulnerabilidades.
    
    Returns:
        Lista de diccionarios con formato:
        {
            "scanner": "XSSScanner",
            "vulnerability": "Reflected XSS",
            "severity": "HIGH",
            "url": "http://example.com/search?q=test",
            "description": "Se encontró XSS reflejado en el parámetro q",
            "evidence": "<script>alert(1)</script>",
            "timestamp": "2026-05-05T15:30:00"
        }
    """
    pass
```

#### `get_payloads() -> list`
Retorna payloads desde `utils/payloads.py`.
```python
def get_payloads(self) -> list:
    """Obtiene payloads para este escáner."""
    pass
```

## 3. Interfaz de Reportes

### 3.1 Estructura de Reporte JSON
```json
{
    "scan_info": {
        "target_url": "http://example.com",
        "start_time": "2026-05-05T15:00:00",
        "end_time": "2026-05-05T15:05:00",
        "scanners_used": ["XSSScanner", "SQLiScanner"]
    },
    "results": [
        {
            "scanner": "XSSScanner",
            "vulnerability": "Reflected XSS",
            "severity": "HIGH",
            "url": "http://example.com/search?q=test",
            "description": "Vulnerabilidad detectada...",
            "evidence": "<script>alert(1)</script>",
            "timestamp": "2026-05-05T15:02:00"
        }
    ],
    "summary": {
        "total_vulnerabilities": 3,
        "critical": 0,
        "high": 2,
        "medium": 1,
        "low": 0
    }
}
```

## 4. Interfaz de Payloads

### 4.1 Estructura en `utils/payloads.py`
```python
XSS_PAYLOADS = [
    {"type": "reflected", "value": "<script>alert('XSS')</script>"},
    {"type": "reflected", "value": "<img src=x onerror=alert('XSS')>"},
]

SQLI_PAYLOADS = [
    {"type": "error_based", "value": "' OR '1'='1"},
    {"type": "boolean_based", "value": "' AND 1=1--"},
]

HEADERS_CHECKS = [
    {"header": "Strict-Transport-Security", "recommendation": "Max-age=31536000"},
    {"header": "X-Content-Type-Options", "recommendation": "nosniff"},
]
```

## 5. Interfaz de Autenticación (Session)

### 5.1 Métodos de `core/session.py`
```python
class ScannerSession:
    def __init__(self, rate_limit: float = 0.5):
        """Inicializa sesión con rate limiting."""
        
    def login(self, login_url: str, username: str, password: str, 
              user_field: str = "username", pass_field: str = "password") -> bool:
        """Realiza login y mantiene sesión activa.
        
        Returns:
            True si el login fue exitoso, False en caso contrario.
        """
        
    def get(self, url: str, params: dict = None) -> requests.Response:
        """Realiza petición GET con rate limiting."""
        
    def post(self, url: str, data: dict = None) -> requests.Response:
        """Realiza petición POST con rate limiting."""
```

## 6. Código de Colores (Logger)

| Nivel | Color | Función | Uso |
|-------|-------|---------|-----|
| INFO | Azul | `info(msg)` | Información general |
| SUCCESS | Verde | `success(msg)` | Operación exitosa |
| WARNING | Amarillo | `warning(msg)` | Advertencia |
| ERROR | Rojo | `error(msg)` | Error crítico |
| VULN | Magenta | `vulnerability(msg)` | Vulnerabilidad detectada |
