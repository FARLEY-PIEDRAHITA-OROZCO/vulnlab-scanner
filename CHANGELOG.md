# Changelog - VulnLab Scanner

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto sigue el [Semantic Versioning](https://semver.org/lang/es/).

## [1.4.0] - 2026-05-05

### Agregado
- Escáner A10 - SSRF (Server-Side Request Forgery)
- 9 pruebas unitarias para SSRFScanner (`tests/test_ssrf.py`)
- Argumento CLI `-R` / `--ssrf` para escanear A10
- Integración de SSRFScanner en `main.py` y `cli.py`
- Payloads SSRF_PAYLOADS en `app/utils/payloads.py`
- Actualización de cobertura OWASP: 7/10 (70%) + XSS extra
- 114 pruebas pasando (100%)

### Cambiado
- README.md actualizado con A10, cobertura 7/10, 114 pruebas
- CLI: `--all` incluye ahora escáner A10
- DOCS/PROGRESO.md sincronizado con 7/10 OWASP
- DOCS/ROADMAP.md actualizado con A02 y A10 completados
- CHANGELOG.md sincronizado con últimas versiones

## [1.3.0] - 2026-05-05

### Agregado
- Escáner A02 - Cryptographic Failures (Missing HTTPS, Cookies without Secure, Sensitive Data in URL)
- 10 pruebas unitarias para CryptoScanner (`tests/test_crypto.py`)
- Argumento CLI `-K` / `--crypto` para escanear A02
- Integración de CryptoScanner en `main.py` y `cli.py`
  - Actualización de cobertura OWASP: 7/10 (70%) + XSS extra
  - 114 pruebas pasando (100%)

### Cambiado
- README.md actualizado con A02, cobertura 6/10, 105 pruebas
- CLI actualizado: `--all` incluye ahora escáner A02

## [1.4.0] - 2026-05-05

### Agregado
- Escáner A10 - SSRF (Server-Side Request Forgery)
- 9 pruebas unitarias para SSRFScanner (`tests/test_ssrf.py`)
- Argumento CLI `-R` / `--ssrf` para escanear A10
- Integración de SSRFScanner en `main.py` y `cli.py`
- Payloads SSRF_PAYLOADS en `app/utils/payloads.py`
- Actualización de cobertura OWASP: 7/10 (70%) + XSS extra
- 114 pruebas pasando (100%)

### Cambiado
- README.md actualizado con A10, cobertura 7/10, 114 pruebas
- CLI: `--all` incluye ahora escáner A10
- DOCS/PROGRESO.md sincronizado con 7/10 OWASP

## [1.2.0] - 2026-05-05

### Agregado
- Escáner A01 - Broken Access Control (IDOR, Privilege Escalation)
- Escáner A07 - Authentication Failures (Weak Creds, Brute Force)
- Escáner A06 - Vulnerable Components (jQuery, Bootstrap detection)
- Multithreading con `concurrent.futures` en main.py
- Barras de progreso con `tqdm` en todos los escáneres
- Gráficos Chart.js en reportes HTML
- Preparación para PyPI (`setup.py`, `pyproject.toml`, `MANIFEST.in`)
- GitHub Actions CI/CD (`.github/workflows/ci.yml`, `publish.yml`)
- Comando `vulnlab-scan` disponible tras instalación
- Configuración centralizada con clase `Config` en `app/config.py`
- Variables de entorno para rutas de login, credenciales y rutas admin
- Archivo `.env.example` documentado
- 95 pruebas pasando (100%)

### Corregido
- Logger simplificado (eliminadas importaciones obsoletas)
- Excepción desnuda corregida en `auth.py`
- Import obsoleto en `http.py` (requests.packages.urllib3 → urllib3)
- Código muerto eliminado en `xss.py`
- `.env` añadido a `.gitignore`
- Importación de `Config` corregida (ahora es clase en lugar de variables sueltas)
- Mocks de pruebas corregidos en `test_auth.py`
- `MANIFEST.in` excluye correctamente directorio `reports/`

### Cambiado
- README.md actualizado a v1.2.0 con Fase 5.3 y cobertura OWASP corregida
- Estructura de proyecto actualizada (nuevos escáneres A01, A06, A07)
- Enlaces de badges corregidos al usuario correcto de GitHub
- Documentación sincronizada con estado real del proyecto

## [1.0.0] - 2026-05-05

### Agregado
- Arquitectura modular completa con clase base `BaseScanner`
- Soporte para escaneo de XSS (Reflected, Stored, DOM-based)
- Soporte para escaneo de SQL Injection (Error-based, Boolean-based)
- Validación de HTTP Security Headers
- Gestión de sesiones con autenticación automática
- Generación de reportes en formato JSON y HTML
- Modo DRY-RUN para simulación sin ataques reales
- Rate limiting configurable para no saturar servidores
- Aviso legal obligatorio antes de escanear
- Soporte para entornos no interactivos (`--accept-disclaimer`)
- 40 pruebas unitarias y de integración (100% pasando)
- Documentación completa en español (DOCS/, README.md, GUIA_USUARIO.md)
- Configuración centralizada vía archivo `.env`
- Payloads centralizados en `utils/payloads.py`
- Cliente HTTP con reintentos y manejo de errores
- Script de instalación automática (`install.py`)

### Características de la Arquitectura
- Módulos independientes para cada tipo de vulnerabilidad
- Estándares de código PEP8 con docstrings en español
- Interfaz CLI con argparse
- Salida coloreada en consola (colorama)
- Soporte para múltiples formatos de reporte

### Seguridad
- Validación de permisos antes de cada escaneo
- Opción de simulación sin ataques reales
- Aviso legal claro sobre uso ético

## [0.1.0] - 2026-04-05 (Prototipo Inicial)

### Agregado
- Estructura básica del proyecto
- Escáner XSS básico (solo reflejado)
- Validación básica de headers
- Reportería JSON simple
- Interfaz CLI inicial
