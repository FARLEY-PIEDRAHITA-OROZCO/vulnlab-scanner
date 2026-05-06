# VulnLab Scanner

Herramienta profesional de escaneo de vulnerabilidades web basada en OWASP Top 10, diseñada para automatizar pruebas de seguridad de manera modular, fácil de instalar y usar.

## Estado Actual del Proyecto

**Versión**: 1.2.0 (Fase 6 en progreso)  
**Cobertura OWASP Top 10 (2021)**: 5/10 (50%) + XSS extra  
**Pruebas**: 95 pasando (100%)  
**Licencia**: MIT (Open Source)

[![CI](https://github.com/FARLEY-PIEDRAHITA-OROZCO/vulnlab-scanner/actions/workflows/ci.yml/badge.svg)](https://github.com/FARLEY-PIEDRAHITA-OROZCO/vulnlab-scanner/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/vulnlab-scanner.svg)](https://pypi.org/project/vulnlab-scanner/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🚀 Características Implementadas ✅

### Escáneres OWASP
- ✅ **A01 - Broken Access Control**: IDOR, escalación de privilegios, Forceful Browsing
- ✅ **A03 - SQL Injection**: Error-based, Boolean-based
- ✅ **A05 - Security Misconfiguration**: Validación de HTTP Security Headers
- ✅ **A06 - Vulnerable Components**: Detección de librerías desactualizadas (jQuery, Bootstrap)
- ✅ **A07 - Auth Failures**: Credenciales débiles, fuerza bruta suave, gestión de sesiones
- ✅ **XSS Scanner**: Reflected, Stored, DOM-based (extra, no es categoría Axx)

### Mejoras Técnicas
- ✅ **Multithreading**: Escaneo paralelo con `concurrent.futures`
- ✅ **Progress Bars**: Barras de progreso con `tqdm`
- ✅ **Chart.js Reports**: Gráficos de severidad en reportes HTML
- ✅ **Autenticación**: Soporte para login automático en sitios protegidos
- ✅ **Configuración**: Valores configurables vía `.env` (login paths, credenciales, rutas admin)
- ✅ **Modo DRY-RUN**: Simulación sin ataques reales
- ✅ **Rate Limiting**: Control de velocidad para no saturar servidores
- ✅ **Aviso Legal**: Validación de permisos antes de escanear
- ✅ **Arquitectura Modular**: Fácil extensión con nuevos escáneres

## Roadmap de Desarrollo (Fases 4-6)

### Fase 4: Nuevos Escáneres OWASP (Completada)
- ✅ **A01 - Broken Access Control**: IDOR, escalación de privilegios
- ✅ **A07 - Auth Failures**: Fuerza bruta suave, sesiones débiles
- ✅ **A06 - Vulnerable Components**: Detección de librerías (SCA)

### Fase 5: Mejoras Técnicas (60% completada)
- ✅ Barras de progreso (tqdm)
- ✅ Multithreading para escaneo paralelo
- ✅ Mejorar reportes (gráficos Chart.js)
- ✅ Valores configurables en `app/config.py`
- 🔄 Interfaz web básica (FastAPI/Flask)

### Fase 6: Empaquetado y Distribución (80% completada)
- ✅ Empaquetado con `setup.py` y `pyproject.toml`
- ✅ Configuración de CI/CD con GitHub Actions (`.github/workflows/`)
- ✅ Manifest y `.env.example` documentados
- 🔄 Publicar en PyPI (`pip install vulnlab-scanner`) - *pendiente configurar `PYPI_API_TOKEN`*
- 🔄 Generar comunidad inicial

### Próximos Escáneres OWASP (para llegar a 8/10)
- 🔄 **A02 - Cryptographic Failures**: Detectar HTTPS faltante, TLS obsoleto, cookies sin Secure
- 🔄 **A10 - SSRF**: Probar parámetros de URL (`?url=`, `?redirect=`)
- 🔄 **A08 - Software Integrity Failures** (opcional, complejo)

**Objetivo actual**: Llegar a **8/10 en funcionalidad profesional** (actualmente 5/10 OWASP + XSS)

## Requisitos

- Python 3.8+
- pip

## Instalación

### Opción 1: Instalación desde PyPI (cuando esté publicado)
```bash
pip install vulnlab-scanner
```

### Opción 2: Instalación Manual (Desarrollo)
```bash
# 1. Clonar el repositorio
git clone https://github.com/FARLEY-PIEDRAHITA-OROZCO/vulnlab-scanner.git
cd vulnlab-scanner

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno virtual
# Windows:
.\.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

### Opción 3: Script Automático
```bash
python install.py
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
USER_AGENT=VulnLabScanner/1.2.0
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
  -u, --url URL          URL del sitio a escanear (obligatorio)
  -x, --xss              Escanear vulnerabilidades XSS
  -s, --sqli             Escanear vulnerabilidades SQL Injection
  -H, --headers          Validar HTTP Security Headers
  -a, --all              Ejecutar todos los escáneres

Autenticación:
  --login-url URL        URL de la página de login
  --username USER        Usuario para autenticación
  --password PASS        Contraseña para autenticación
  --login-username-field NAME   Campo usuario (default: username)
  --login-password-field NAME   Campo password (default: password)

Reportes:
  --report-format FMT    Formato: json, html, ambos (default: ambos)
  --report-output DIR    Directorio de salida (default: ./reports)

Opciones adicionales:
  --dry-run              Simular sin ataques reales
  --rate-limit SEC       Segundos entre peticiones (default: 0.5)
  --disclaimer           Mostrar aviso legal y salir
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
│   ├── main.py                 # Punto de entrada
│   ├── cli.py                  # Argumentos CLI
│   ├── config.py               # Configuración centralizada (Clase Config)
│   ├── core/
│   │   ├── http.py             # Cliente HTTP
│   │   └── session.py          # Gestión de sesiones
│   ├── scanner/
│   │   ├── base.py             # Clase base abstracta
│   │   ├── xss.py              # Escáner XSS
│   │   ├── sqli.py             # Escáner SQLi
│   │   ├── headers.py          # Validador de headers
│   │   ├── access_control.py   # Escáner A01 (Access Control)
│   │   ├── auth.py             # Escáner A07 (Auth Failures)
│   │   └── components.py       # Escáner A06 (Vulnerable Components)
│   └── utils/
│       ├── logger.py           # Salida coloreada
│       ├── helpers.py          # Funciones auxiliares
│       ├── renderer.py         # Formateo de resultados
│       ├── reporter.py         # Generación de reportes
│       ├── payloads.py         # Payloads centralizados
│       └── disclaimer.py       # Aviso legal
├── tests/                      # Pruebas unitarias (95 pruebas)
├── reports/                    # Reportes generados (no incluido en paquete)
├── .env.example                # Ejemplo de configuración
├── requirements.txt
├── setup.py
├── pyproject.toml
├── MANIFEST.in
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
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

La documentación completa está en el directorio `DOCS/` (si existe):
- `DOCS/REQUISITOS.md` - Requisitos del sistema
- `DOCS/ALCANCE.md` - Alcance del proyecto
- `DOCS/ARQUITECTURA.md` - Arquitectura técnica
- `DOCS/ESTANDARES_CODIGO.md` - Estándares de código
- `DOCS/GUIA_USUARIO.md` - Guía de usuario
- `DOCS/ROADMAP.md` - Futuras mejoras
- `DOCS/PROGRESO.md` - Estado actual de desarrollo

## Pruebas

Para ejecutar las pruebas unitarias:
```bash
pytest tests/ -v
```

**Cobertura actual**: 95 pruebas (100% pasando)

## Contribuciones

Las contribuciones son bienvenidas. Por favor lee:
- `DOCS/ESTANDARES_CODIGO.md` antes de contribuir
- Seguir convenciones de commits: `tipo(ámbito): descripción en español`
- Ejecutar pruebas antes de cada commit

## Licencia

MIT License - Open Source

## Estado de Desarrollo

| Fase | Descripción | Estado |
|------|----------------|--------|
| Fase 1 | Análisis de Requisitos | ✅ Completada |
| Fase 2 | Diseño de Arquitectura | ✅ Completada |
| Fase 3 | Desarrollo (MVP) | ✅ Completada |
| Fase 4 | Nuevos Escáneres OWASP | ✅ Completada |
| Fase 5 | Mejoras Técnicas | 🔄 En progreso (60%) |
| Fase 6 | Empaquetado y Distribución | 🔄 En progreso (80%) |

**Siguiente hito**: Publicar en PyPI y luego implementar A02 (Cryptographic Failures)
