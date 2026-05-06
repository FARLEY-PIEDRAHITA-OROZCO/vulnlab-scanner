# Arquitectura de VulnLab Scanner v1.4.2

## 1. Visión General

La arquitectura está diseñada bajo el patrón modular, donde cada tipo de vulnerabilidad OWASP es un módulo independiente que hereda de una clase base común. Esto permite fácil mantenimiento y extensibilidad.

**Versión**: 1.4.2  
**Arquitectura**: Modular con herencia de clase base  
**Estado**: Estable, listo para producción

## 2. Estructura de Directorios (Actualizada)

```
vulnlab-scanner/
├── app/
│   ├── __init__.py            # Versión 1.4.2
│   ├── main.py               # Punto de entrada principal (orquestador)
│   ├── cli.py                # Manejo de argumentos CLI (argparse)
│   ├── config.py             # Configuración centralizada (Clase Config)
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── http.py           # Cliente HTTP con rate limiting y reintentos
│   │   └── session.py       # Gestión de sesiones y autenticación
│   │
│   ├── scanner/
│   │   ├── __init__.py
│   │   ├── base.py           # Clase base abstracta (BaseScanner)
│   │   ├── xss.py           # XSS Scanner (Reflected, Stored, DOM)
│   │   ├── sqli.py          # SQL Injection Scanner (Error, Boolean)
│   │   ├── headers.py       # HTTP Security Headers Validator
│   │   ├── access_control.py # A01: Broken Access Control
│   │   ├── auth.py          # A07: Authentication Failures
│   │   ├── components.py    # A06: Vulnerable Components
│   │   ├── crypto.py       # A02: Cryptographic Failures
│   │   └── ssrf.py         # A10: Server-Side Request Forgery
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py         # Salida coloreada (colorama)
│       ├── helpers.py        # Funciones auxiliares
│       ├── renderer.py       # Formateo de resultados en consola
│       ├── reporter.py       # Generación de reportes (JSON/HTML)
│       ├── payloads.py       # Payloads centralizados
│       └── disclaimer.py     # Aviso legal y validación de permisos
│
├── tests/                    # Pruebas unitarias (114 total)
│   ├── __init__.py
│   ├── test_xss.py
│   ├── test_sqli.py
│   ├── test_headers.py
│   ├── test_access_control.py
│   ├── test_auth.py
│   ├── test_components.py
│   ├── test_crypto.py
│   ├── test_ssrf.py
│   └── test_config.py
│
├── docs/                     # Documentación completa en español
│   ├── REQUISITOS.md
│   ├── ALCANCE.md
│   ├── ARQUITECTURA.md     # Este archivo
│   ├── ESTANDARES_CODIGO.md
│   ├── GUIA_USUARIO.md
│   ├── ROADMAP.md
│   ├── PROGRESO.md
│   └── PROGRESO_ACTUAL.md
│
├── reports/                  # Reportes generados (no incluido en paquete)
│
├── .github/                 # GitHub config (CI/CD, templates)
│   ├── workflows/
│   │   ├── ci.yml          # CI: tests en Python 3.8-3.11
│   │   └── publish.yml    # CD: publicación en PyPI
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── security_report.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── dependabot.yml
│   └── FUNDING.yml
│
├── .env.example              # Ejemplo de configuración
├── requirements.txt          # Dependencias de producción
├── requirements-dev.txt      # Dependencias de desarrollo
├── setup.py                 # Empaquetado tradicional
├── pyproject.toml           # Configuración moderna de build
├── MANIFEST.in              # Control de archivos incluidos
├── Makefile                 # Tareas comunes (test, lint, format)
├── tox.ini                  # Pruebas multi-entorno
├── .pre-commit-config.yaml  # Hooks de pre-commit
├── .editorconfig            # Configuración de editor
├── .gitignore               # Archivos ignorados por Git
├── SECURITY.md              # Política de seguridad
├── CODE_OF_CONDUCT.md       # Código de conducta
├── CODEOWNERS               # Propietarios del código
├── CHANGELOG.md             # Registro de cambios
├── CONTRIBUTING.md          # Guía de contribución
├── README.md                # Documentación principal
└── LICENSE                  # Licencia MIT
```

## 3. Clases Principales

### 3.1 BaseScanner (app/scanner/base.py)
Clase base abstracta que define la interfaz común para todos los escáneres.

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseScanner(ABC):
    """Clase base abstracta para todos los escáneres de vulnerabilidades."""
    
    def __init__(self, target_url: str, session, dry_run: bool = False):
        self.name = self.__class__.__name__
        self.target_url = target_url
        self.session = session
        self.dry_run = dry_run
        self.results = []
    
    @abstractmethod
    def scan(self) -> List[Dict[str, Any]]:
        """Ejecuta el escaneo de vulnerabilidades."""
        pass
    
    @abstractmethod
    def get_payloads(self) -> List[str]:
        """Retorna la lista de payloads para este escáner."""
        pass
    
    def add_result(self, vuln_name: str, severity: str, 
                  description: str, evidence: str) -> None:
        """Añade un resultado del escaneo."""
        self.results.append({
            "vulnerability": vuln_name,
            "severity": severity,
            "description": description,
            "evidence": evidence
        })
```

### 3.2 Config (app/config.py)
Clase centralizada que maneja todas las configuraciones.

```python
import os
from dotenv import load_dotenv

load_dotenv()

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

## 4. Flujo de Ejecución

### 4.1 Punto de Entrada (main.py)
1. Parsea argumentos CLI (cli.py)
2. Muestra aviso legal (disclaimer.py)
3. Crea instancia de Config
4. Inicializa gestión de sesiones (session.py)
5. Si se requiere, realiza login automático
6. Ejecuta escáneres seleccionados (multithreading opcional)
7. Genera reportes (reporter.py)

### 4.2 Ejecución de Escáneres
```python
# Ejemplo de ejecución de un escáner
scanner = XSSScanner(target_url, session, dry_run)
results = scanner.scan()
```

### 4.3 Multithreading
Uso de `concurrent.futures.ThreadPoolExecutor` para ejecutar múltiples escáneres en paralelo:
```python
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(scanner.scan) for scanner in scanners]
    results = [f.result() for f in as_completed(futures)]
```

## 5. Módulos de Escáneres (8 OWASP + XSS)

| Escáner | Clase | Archivo | OWASP | Pruebas |
|----------|-------|--------|-------|---------|
| XSS | XSSScanner | xss.py | Extra | 10 |
| SQLi | SQLiScanner | sqli.py | A03 | 12 |
| Headers | HeadersScanner | headers.py | A05 | 8 |
| Access Control | AccessControlScanner | access_control.py | A01 | 11 |
| Auth Failures | AuthScanner | auth.py | A07 | 10 |
| Vulnerable Components | ComponentsScanner | components.py | A06 | 8 |
| Cryptographic Failures | CryptoScanner | crypto.py | A02 | 10 |
| SSRF | SSRFScanner | ssrf.py | A10 | 9 |

**Total**: 8 escáneres OWASP + XSS = 68 pruebas de escáneres + 46 de integración = 114 total

## 6. Comunicación HTTP

### 6.1 HTTPClient (app/core/http.py)
Cliente HTTP con:
- Rate limiting configurable
- Reintentos automáticos
- Manejo de errores
- User-Agent personalizado

### 6.2 ScannerSession (app/core/session.py)
Gestión de sesiones con:
- Soporte para login automático
- Mantenimiento de cookies
- Manejo de redirecciones

## 7. Generación de Reportes

### 7.1 JSON Reports (reporter.py)
- Estructura: scan_info, results, summary
- Formato: UTF-8, indent=2
- Ubicación: Config.REPORTS_DIR

### 7.2 HTML Reports (reporter.py)
- Gráficos Chart.js de severidad
- Resumen ejecutivo
- Detalles de cada vulnerabilidad
- Recomendaciones de corrección

## 8. Pruebas y Calidad

### 8.1 Pruebas Unitarias
- **Total**: 114 pruebas
- **Pasando**: 109
- **Omitidas**: 5
- **Fallando**: 0

### 8.2 Herramientas de Calidad
- **flake8**: Linting (max-line-length=127)
- **black**: Formateo automático de código
- **isort**: Ordenamiento de imports
- **bandit**: Análisis de seguridad estático
- **pytest**: Framework de pruebas
- **pytest-cov**: Cobertura de código

### 8.3 CI/CD (GitHub Actions)
- **ci.yml**: Ejecuta pruebas en Python 3.8, 3.9, 3.10, 3.11
- **publish.yml**: Publica en PyPI al crear un Release

## 9. Extensibilidad

### 9.1 Crear un Nuevo Escáner
1. Heredar de `BaseScanner`
2. Implementar `scan()` y `get_payloads()`
3. Añadir payloads en `payloads.py`
4. Integrar en `main.py` y `cli.py`
5. Crear pruebas en `tests/test_nombre.py`

### 9.2 Ejemplo de Extensión
```python
from app.scanner.base import BaseScanner

class NewScanner(BaseScanner):
    def scan(self):
        # Implementar lógica de escaneo
        pass
    
    def get_payloads(self):
        return ["payload1", "payload2"]
```

## 10. Seguridad y Ética

### 10.1 Aviso Legal
- Obligatorio antes de cada escaneo
- Validación de permisos
- Modo dry-run para simulación

### 10.2 Restricciones
- Solo para propósitos éticos
- Requiere autorización explícita
- No se permite uso malicioso

---

**Versión del documento**: 1.4.2  
**Fecha de actualización**: 2026-05-06  
**Responsable**: @FARLEY-PIEDRAHITA-OROZCO  
**Estado**: ✅ Completo y actualizado con arquitectura real
