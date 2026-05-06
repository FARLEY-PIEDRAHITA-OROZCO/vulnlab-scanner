# Interfaces y Contratos - VulnLab Scanner v1.4.2

## 1. Interfaz de Línea de Comandos (CLI)

### 1.1 Argumentos Principales
```bash
python -m app.main [OPCIONES]

Argumentos principales:
  -u, --url URL          URL del sitio a escanear (obligatorio si no usa --disclaimer)
  -x, --xss              Escanear vulnerabilidades XSS
  -s, --sqli             Escanear vulnerabilidades SQL Injection
  -H, --headers          Validar HTTP Security Headers
  -A, --access-control   Escanear Broken Access Control (A01)
  -U, --auth             Escanear Authentication Failures (A07)
  -C, --vuln-components Escanear Vulnerable Components (A06)
  -K, --crypto           Escanear Cryptographic Failures (A02)
  -R, --ssrf             Escanear SSRF (A10)
  -a, --all              Ejecutar todos los escáneres disponibles
```

### 1.2 Opciones de Autenticación
```
Autenticación:
  --login-url URL        URL de la página de login
  --username USER        Usuario para autenticación
  --password PASS        Contraseña para autenticación
  --login-username-field NAME   Campo usuario (default: username)
  --login-password-field NAME   Campo password (default: password)
```

### 1.3 Opciones de Reporte
```
Reportes:
  --report-format FMT    Formato: json, html, ambos (default: ambos)
  --output-dir DIR       Directorio de salida (default: ./reports)
```

### 1.4 Opciones Adicionales
```
Opciones adicionales:
  --dry-run              Simular sin ataques reales
  --rate-limit SEC       Segundos entre peticiones (default: 0.5)
  --disclaimer           Mostrar aviso legal y salir
  --no-disclaimer        Omitir aviso legal (no recomendado)
  -v, --verbose         Modo verbose (más detalles)
  -h, --help             Mostrar ayuda
```

## 2. Interfaz de Escáneres (BaseScanner)

Todos los módulos en `app/scanner/` deben implementar esta interfaz:

### 2.1 Métodos Obligatorios

#### `scan() -> list`
Ejecuta el escaneo y retorna resultados.
```python
def scan(self) -> List[Dict[str, Any]]:
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
            "timestamp": "2026-05-06T15:30:00"
        }
    """
    pass
```

#### `get_payloads() -> list`
Retorna payloads desde `utils/payloads.py`.
```python
def get_payloads(self) -> List[str]:
    """Obtiene payloads para este escáner."""
    pass
```

### 2.2 Métodos Heredados de BaseScanner

#### `add_result(vuln_name, severity, description, evidence)`
Añade un resultado del escaneo.
```python
def add_result(self, vuln_name: str, severity: str, 
              description: str, evidence: str) -> None:
    """Añade un resultado del escaneo a la lista de resultados."""
    self.results.append({
        "vulnerability": vuln_name,
        "severity": severity,
        "description": description,
        "evidence": evidence
    })
```

## 3. Interfaz de Reportes

### 3.1 Estructura de Reporte JSON
```json
{
  "scan_info": {
    "target_url": "http://example.com",
    "start_time": "2026-05-06T15:00:00",
    "end_time": "2026-05-06T15:05:00",
    "scanner_version": "1.4.2",
    "options": {
      "xss": true,
      "sqli": false,
      "headers": true,
      "all": false
    }
  },
  "results": [
    {
      "scanner": "XSSScanner",
      "vulnerability": "Reflected XSS",
      "severity": "HIGH",
      "url": "http://example.com/search?q=test",
      "description": "Vulnerabilidad detectada...",
      "evidence": "<script>alert(1)</script>",
      "timestamp": "2026-05-06T15:02:00"
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

### 3.2 Estructura de Reporte HTML
- **Header**: Título, fecha, objetivo
- **Summary**: Resumen con gráfico Chart.js
- **Results**: Detalles de cada vulnerabilidad
  - Vulnerabilidad
  - Severidad (con color: CRITICAL=rojo, HIGH=naranja, etc.)
  - Descripción
  - Evidencia
  - Recomendación

### 3.3 Funciones de `reporter.py`
```python
def save_json_report(data: dict, output_dir: str = None) -> str:
    """Guarda el reporte en formato JSON.
    
    Args:
        data: Diccionario con los datos del reporte.
        output_dir: Directorio de salida (usa Config.REPORTS_DIR por defecto).
        
    Returns:
        Ruta del archivo guardado.
    """

def save_html_report(data: dict, output_dir: str = None) -> str:
    """Guarda el reporte en formato HTML básico.
    
    Args:
        data: Diccionario con los datos del reporte.
        output_dir: Directorio de salida (usa Config.REPORTS_DIR por defecto).
        
    Returns:
        Ruta del archivo guardado.
    """

def generate_summary(results: list) -> dict:
    """Genera un resumen estadístico de los resultados.
    
    Args:
        results: Lista de resultados del escaneo.
        
    Returns:
        Diccionario con el resumen.
    """
```

## 4. Interfaz de Payloads

### 4.1 Estructura en `utils/payloads.py`
```python
# XSS Payloads
XSS_PAYLOADS = [
    {"type": "reflected", "value": "<script>alert('XSS')</script>"},
    {"type": "reflected", "value": "<img src=x onerror=alert('XSS')>"},
    # ... más payloads
]

# SQL Injection Payloads
SQLI_PAYLOADS = [
    {"type": "error_based", "value": "' OR '1'='1"},
    {"type": "boolean_based", "value": "' AND 1=1--"},
    # ... más payloads
]

# HTTP Headers to Check
HEADERS_CHECKS = [
    {"header": "Strict-Transport-Security", "recommendation": "Max-age=31536000"},
    {"header": "X-Content-Type-Options", "recommendation": "nosniff"},
    # ... más headers
]

# Access Control Payloads
ACCESS_CONTROL_PAYLOADS = [
    {"type": "idor", "param": "id", "test_value": "2"},
    # ... más payloads
]

# Authentication Payloads
AUTH_PAYLOADS = [
    {"type": "weak_creds", "username": "admin", "password": "admin123"},
    # ... más payloads
]

# Vulnerable Components (technologies to detect)
VULNERABLE_COMPONENTS = [
    {"name": "jQuery", "version_pattern": r"jquery[/-](\d+\.\d+\.\d+)", "vulnerable_below": "3.6.0"},
    # ... más componentes
]

# Cryptographic Failures Payloads
CRYPTO_PAYLOADS = [
    {"type": "missing_https", "check": "url_scheme"},
    # ... más payloads
]

# SSRF Payloads
SSRF_PAYLOADS = [
    {"type": "internal_ip", "value": "http://127.0.0.1/admin"},
    # ... más payloads
]
```

## 5. Interfaz de Autenticación (Session)

### 5.1 Métodos de `core/session.py`
```python
class ScannerSession:
    """Gestión de sesiones con soporte de autenticación."""
    
    def __init__(self, rate_limit: float = None):
        """Inicializa la sesión del escáner.
        
        Args:
            rate_limit: Tiempo entre peticiones (usa Config si es None).
        """
    
    def login(self, login_url: str, username: str, password: str,
              user_field: str = "username", pass_field: str = "password") -> bool:
        """Realiza login automático y mantiene la sesión.
        
        Args:
            login_url: URL de la página de login.
            username: Nombre de usuario.
            password: Contraseña.
            user_field: Nombre del campo de usuario en el formulario.
            pass_field: Nombre del campo de contraseña en el formulario.
            
        Returns:
            True si el login fue exitoso, False en caso contrario.
        """
    
    def get(self, url: str, params: dict = None, **kwargs) -> requests.Response:
        """Realiza petición GET manteniendo la sesión.
        
        Args:
            url: URL objetivo.
            params: Parámetros de consulta.
            **kwargs: Argumentos adicionales.
            
        Returns:
            Objeto Response de requests.
        """
    
    def post(self, url: str, data: dict = None, **kwargs) -> requests.Response:
        """Realiza petición POST manteniendo la sesión.
        
        Args:
            url: URL objetivo.
            data: Datos del formulario.
            **kwargs: Argumentos adicionales.
            
        Returns:
            Objeto Response de requests.
        """
```

## 6. Código de Colores (Logger)

| Nivel | Color | Función | Uso |
|-------|-------|---------|-----|
| INFO | Azul | `info(msg)` | Información general |
| SUCCESS | Verde | `success(msg)` | Operación exitosa |
| WARNING | Amarillo | `warning(msg)` | Advertencia |
| ERROR | Rojo | `error(msg)` | Error crítico |
| VULN | Magenta | `vulnerability(msg)` | Vulnerabilidad detectada |

### 6.1 Funciones en `utils/logger.py`
```python
def info(msg: str) -> None:
    """Imprime mensaje informativo en azul."""
    
def success(msg: str) -> None:
    """Imprime mensaje de éxito en verde."""
    
def warning(msg: str) -> None:
    """Imprime advertencia en amarillo."""
    
def error(msg: str) -> None:
    """Imprime error en rojo."""
    
def vulnerability(msg: str) -> None:
    """Imprime vulnerabilidad detectada en magenta."""
```

## 7. Interfaz de Configuración (Config)

### 7.1 Clase Config en `config.py`
```python
class Config:
    """Configuración centralizada del escáner."""
    
    # HTTP
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", 10))
    RATE_LIMIT = float(os.getenv("RATE_LIMIT", 0.5))
    USER_AGENT = os.getenv("USER_AGENT", "VulnLabScanner/1.4.2")
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
    
    # Auth
    DEFAULT_LOGIN_PATHS = os.getenv("DEFAULT_LOGIN_PATHS", "/login,/signin").split(",")
    DEFAULT_BRUTE_FORCE_ATTEMPTS = int(os.getenv("DEFAULT_BRUTE_FORCE_ATTEMPTS", 3))
    DEFAULT_BRUTE_FORCE_PASSWORDS = os.getenv("DEFAULT_BRUTE_FORCE_PASSWORDS", "123456,password").split(",")
    
    # Access Control
    DEFAULT_ADMIN_PATHS = os.getenv("DEFAULT_ADMIN_PATHS", "/admin,/administrator").split(",")
    
    # Directories
    REPORTS_DIR = os.getenv("REPORTS_DIR", "reports")
```

## 8. Contratos de Pruebas

### 8.1 Estructura de Archivos de Prueba
```
tests/
├── __init__.py
├── test_xss.py
├── test_sqli.py
├── test_headers.py
├── test_access_control.py
├── test_auth.py
├── test_components.py
├── test_crypto.py
├── test_ssrf.py
└── test_config.py
```

### 8.2 Formato de Pruebas
```python
import unittest
from unittest.mock import Mock, patch
import pytest

class TestMiScanner(unittest.TestCase):
    """Pruebas para MiScanner."""
    
    def setUp(self):
        """Configuración antes de cada prueba."""
        self.session = Mock()
        self.scanner = MiScanner("http://example.com", self.session)
    
    def test_initialization(self):
        """Prueba que el escáner se inicializa correctamente."""
        self.assertEqual(self.scanner.target_url, "http://example.com")
        self.assertEqual(self.scanner.name, "MiScanner")
    
    @patch('app.scanner.mi_scanner.requests.get')
    def test_scan_sin_vulnerabilidades(self, mock_get):
        """Prueba escaneo sin detectar vulnerabilidades."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "sin vulnerabilidades"
        mock_get.return_value = mock_response
        
        results = self.scanner.scan()
        self.assertEqual(len(results), 0)
```

---

**Versión del documento**: 1.4.2  
**Fecha de actualización**: 2026-05-06  
**Responsable**: @FARLEY-PIEDRAHITA-OROZCO  
**Estado**: ✅ Completo y actualizado con interfaces actuales
