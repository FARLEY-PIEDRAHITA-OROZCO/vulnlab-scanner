# VulnLab Scanner

Herramienta profesional de escaneo de vulnerabilidades web basada en OWASP Top 10 (2021), diseñada para automatizar pruebas de seguridad de manera modular, fácil de instalar y usar.

## Estado Actual del Proyecto

**Versión**: 1.5.0 (Fase 7 completada)
**Cobertura OWASP Top 10 (2021)**: 10/10 (100%)
**Pruebas**: 154 passed (100% total)
**Licencia**: MIT (Open Source)
**Estado**: Listo para producción y publicación en PyPI

[![CI](https://github.com/FARLEY-PIEDRAHITA-OROZCO/vulnlab-scanner/actions/workflows/ci.yml/badge.svg)](https://github.com/FARLEY-PIEDRAHITA-OROZCO/vulnlab-scanner/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/vulnlab-scanner.svg)](https://pypi.org/project/vulnlab-scanner/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/pycqa/bandit)

## 🚀 Características Implementadas ✅

### Escáneres OWASP (10/10)
- ✅ **A01 - Broken Access Control**: IDOR, escalación de privilegios, Forceful Browsing
- ✅ **A02 - Cryptographic Failures**: HTTPS faltante, cookies sin Secure, credenciales en URL
- ✅ **A03 - SQL Injection**: Error-based, Boolean-based
- ✅ **A04 - Insecure Design**: Rate limiting, CSRF, validación de entrada, flujos inseguros
- ✅ **A05 - Security Misconfiguration**: Validación de HTTP Security Headers
- ✅ **A06 - Vulnerable Components**: Detección de librerías desactualizadas (jQuery, Bootstrap)
- ✅ **A07 - Auth Failures**: Credenciales débiles, fuerza bruta suave, gestión de sesiones
- ✅ **A09 - Security Logging**: Headers de logging, manejo de errores, monitoreo, audit logs
- ✅ **A10 - SSRF**: Parámetros de URL, IPs internas, esquemas peligrosos
- ✅ **XSS Scanner**: Reflected, Stored, DOM-based (extra, no es categoría Axx)

### Mejoras Técnicas
- ✅ **Multithreading**: Escaneo paralelo con `concurrent.futures`
- ✅ **Progress Bars**: Barras de progreso con `tqdm`
- ✅ **Chart.js Reports**: Gráficos de severidad en reportes HTML
- ✅ **Autenticación**: Soporte para login automático en sitios protegidos
- ✅ **Configuración centralizada**: Clase `Config` en `app/config.py` con variables de entorno
- ✅ **Modo DRY-RUN**: Simulación sin ataques reales
- ✅ **Rate Limiting**: Control de velocidad para no saturar servidores
- ✅ **Aviso Legal**: Validación de permisos antes de escanear
- ✅ **Arquitectura Modular**: Fácil extensión con nuevos escáneres
- ✅ **Reportes**: Generación en JSON y HTML con resúmenes y gráficos

## Roadmap de Desarrollo (Fases 1-6)

### ✅ Fase 1: Análisis de Requisitos (Completada)
- Documentación de requisitos (`DOCS/REQUISITOS.md`, `DOCS/ALCANCE.md`)

### ✅ Fase 2: Diseño de Arquitectura (Completada)
- Arquitectura técnica (`DOCS/ARQUITECTURA.md`, `DOCS/ESTANDARES_CODIGO.md`)

### ✅ Fase 3: Desarrollo MVP (Completada)
- Escáneres básicos: XSS, SQLi, Headers
- Gestión de sesiones y reportes

### ✅ Fase 4: Nuevos Escáneres OWASP (Completada)
- ✅ **A01 - Broken Access Control** (11 pruebas)
- ✅ **A02 - Cryptographic Failures** (10 pruebas)
- ✅ **A06 - Vulnerable Components** (8 pruebas)
- ✅ **A07 - Auth Failures** (10 pruebas)
- ✅ **A10 - SSRF** (9 pruebas)

### ✅ Fase 5: Mejoras Técnicas (Completada)
- ✅ Barras de progreso (tqdm)
- ✅ Multithreading (`concurrent.futures`)
- ✅ Gráficos Chart.js en reportes
- ✅ Configuración centralizada (`Config` class)

### ✅ Fase 6: Empaquetado y Distribución (95% completada)
- ✅ Empaquetado con `setup.py` y `pyproject.toml`
- ✅ Configuración de CI/CD (GitHub Actions)
- ✅ Manifest y `.env.example` documentados
- ✅ Archivos profesionales: `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CODEOWNERS`
- ✅ Configuración de desarrollo: `.pre-commit-config.yaml`, `tox.ini`, `Makefile`
- ✅ Plantillas GitHub: issues, PR, Dependabot
- 🔄 Publicar en PyPI (`pip install vulnlab-scanner`) - *pendiente configurar `PYPI_API_TOKEN`*

## Requisitos

- Python 3.8+
- pip
- Dependencias: `requests`, `colorama`, `python-dotenv`, `jinja2`, `tqdm`

## Instalación

### Opción 1: Instalación desde PyPI (recomendada)
```bash
pip install vulnlab-scanner
```

### Opción 2: Instalación desde código fuente (Desarrollo)
```bash
# 1. Clonar el repositorio
git clone https://github.com/FARLEY-PIEDRAHITA-OROZCO/vulnlab-scanner.git
cd vulnlab-scanner

# 2. Crear entorno virtual (recomendado)
python -m venv .venv

# 3. Activar entorno virtual
# Windows:
.\.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Instalar en modo editable (para desarrollo)
pip install -e .
```

## Configuración

Edita el archivo `.env` para personalizar la configuración (puedes copiar de `.env.example`):

```env
# Configuración General
DEBUG=False
VERBOSE=False

# Configuración de HTTP
RATE_LIMIT=0.5
DEFAULT_TIMEOUT=10
USER_AGENT=VulnLabScanner/1.4.3
MAX_RETRIES=3

# Configuración de Autenticación
DEFAULT_LOGIN_PATHS=/login,/signin,/auth,/login.php
DEFAULT_BRUTE_FORCE_ATTEMPTS=3
DEFAULT_BRUTE_FORCE_PASSWORDS=123456,password,admin123,qwerty,letmein

# Configuración de Access Control
DEFAULT_ADMIN_PATHS=/admin,/administrator,/admin/users,/dashboard/admin

# Directorios
REPORTS_DIR=reports
```

## Uso

### Escaneo básico
```bash
python -m app.main -u http://ejemplo.com --all
```

### Opciones disponibles
```
Uso: python -m app.main [OPCIONES]

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
  -a, --all              Ejecutar todos los escáneres

Autenticación:
  --login-url URL        URL de la página de login
  --username USER        Usuario para autenticación
  --password PASS        Contraseña para autenticación
  --login-username-field NAME   Campo usuario (default: username)
  --login-password-field NAME   Campo password (default: password)

Reportes:
  --report-format FMT    Formato: json, html, ambos (default: ambos)
  --output-dir DIR       Directorio de salida (default: ./reports)

Opciones adicionales:
  --dry-run              Simular sin ataques reales
  --rate-limit SEC       Segundos entre peticiones (default: 0.5)
  --disclaimer           Mostrar aviso legal y salir
  --no-disclaimer        Omitir aviso legal (no recomendado)
  -v, --verbose          Modo verbose
```

### Ejemplos

#### Escaneo completo con autenticación:
```bash
python -m app.main -u http://juiceshop:3000 --all \
  --login-url http://juiceshop:3000/#/login \
  --username admin@juice-sh.op \
  --password admin123
```

#### Solo verificar headers:
```bash
python -m app.main -u https://www.google.com --headers
```

#### Probar XSS en modo simulación:
```bash
python -m app.main -u "http://test.com/search?q=test" --xss --dry-run
```

## Estructura del Proyecto

```
vulnlab-scanner/
├── app/
│   ├── __init__.py            # Versión 1.4.2
│   ├── main.py               # Punto de entrada principal
│   ├── cli.py                # Argumentos CLI
│   ├── config.py             # Configuración centralizada (Clase Config)
│   ├── core/
│   │   ├── http.py           # Cliente HTTP con rate limiting
│   │   └── session.py       # Gestión de sesiones y login
│   ├── scanner/
│   │   ├── base.py           # Clase base abstracta BaseScanner
│   │   ├── xss.py           # Escáner XSS
│   │   ├── sqli.py          # Escáner SQL Injection
│   │   ├── headers.py       # Validador de HTTP Security Headers
│   │   ├── access_control.py # Escáner A01 (Broken Access Control)
│   │   ├── auth.py          # Escáner A07 (Auth Failures)
│   │   ├── components.py    # Escáner A06 (Vulnerable Components)
│   │   ├── crypto.py       # Escáner A02 (Cryptographic Failures)
│   │   └── ssrf.py         # Escáner A10 (SSRF)
│   └── utils/
│       ├── logger.py         # Salida coloreada
│       ├── helpers.py        # Funciones auxiliares
│       ├── renderer.py       # Formateo de resultados
│       ├── reporter.py       # Generación de reportes JSON/HTML
│       ├── payloads.py       # Payloads centralizados
│       └── disclaimer.py     # Aviso legal
├── tests/                    # Pruebas unitarias (114 pruebas)
├── docs/                     # Documentación completa
├── reports/                  # Reportes generados (no incluido en paquete)
├── .env.example              # Ejemplo de configuración
├── requirements.txt          # Dependencias de producción
├── requirements-dev.txt      # Dependencias de desarrollo
├── setup.py                 # Configuración de empaquetado
├── pyproject.toml           # Configuración moderna de build
├── MANIFEST.in              # Control de archivos incluidos
├── Makefile                 # Tareas comunes (test, lint, format)
├── tox.ini                  # Configuración de pruebas multi-entorno
├── .pre-commit-config.yaml  # Hooks de pre-commit
├── .editorconfig            # Configuración de editor
├── SECURITY.md              # Política de seguridad
├── CODE_OF_CONDUCT.md       # Código de conducta
├── CODEOWNERS               # Propietarios del código
├── CHANGELOG.md             # Registro de cambios
├── CONTRIBUTING.md          # Guía de contribución
├── README.md                # Este archivo
└── LICENSE                  # Licencia MIT
```

## Aviso Legal

Esta herramienta está diseñada exclusivamente para **propósitos de seguridad ética**.

Al usar VulnLab Scanner, declaras que:
1. Solo escanearás sistemas para los cuales tienes autorización explícita
2. No usarás la herramienta para actividades ilegales
3. Eres responsable del uso que le des a los resultados

Para ver el aviso legal completo:
```bash
python -m app.main --disclaimer
```

## Documentación

La documentación completa está en el directorio `docs/`:
- `docs/REQUISITOS.md` - Requisitos del sistema
- `docs/ALCANCE.md` - Alcance del proyecto
- `docs/ARQUITECTURA.md` - Arquitectura técnica
- `docs/ESTANDARES_CODIGO.md` - Estándares de código
- `docs/GUIA_USUARIO.md` - Guía de usuario
- `docs/ROADMAP.md` - Roadmap de desarrollo
- `docs/PROGRESO.md` - Estado actual de desarrollo
- `docs/PROGRESO_ACTUAL.md` - Progreso actual detallado

## Pruebas

Para ejecutar las pruebas unitarias:
```bash
pytest tests/ -v
```

**Cobertura actual**: 154 pruebas (154 passed, 0 skipped)

## Contribuciones

Las contribuciones son bienvenidas. Por favor lee:
- `CONTRIBUTING.md` antes de contribuir
- `docs/ESTANDARES_CODIGO.md` para estándares de código
- Seguir convenciones de commits: `tipo(ámbito): descripción en español`
- Ejecutar pruebas antes de cada commit: `make test` o `pytest tests/ -v`

## Licencia

MIT License - Open Source

## Contacto

- **Proyecto**: https://github.com/FARLEY-PIEDRAHITA-OROZCO/vulnlab-scanner
- **Issues**: https://github.com/FARLEY-PIEDRAHITA-OROZCO/vulnlab-scanner/issues
- **Seguridad**: security@vulnlab.com

## Agradecimientos

Agradecemos a todos los contribuidores y a la comunidad OWASP por las referencias y metodologías.
