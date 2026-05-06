# VulnLab Scanner

Herramienta profesional de escaneo de vulnerabilidades web basada en OWASP Top 10, diseñada para automatizar pruebas de seguridad de manera modular, fácil de instalar y usar.

## Estado Actual del Proyecto

**Versión**: 1.2.0 (Fase 5.3 Completada)  
**Cobertura OWASP**: 6/10 (60%)  
**Pruebas**: 95 pasando (100%)  
**Licencia**: MIT (Open Source)

[![CI](https://github.com/anomalyco/vulnlab-scanner/actions/workflows/ci.yml/badge.svg)](https://github.com/anomalyco/vulnlab-scanner/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/vulnlab-scanner.svg)](https://pypi.org/project/vulnlab-scanner/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🚀 Características Implementadas ✅

- ✅ **XSS Scanner**: Detección de Cross-Site Scripting (Reflected, Stored, DOM-based)
- ✅ **SQLi Scanner**: Detección de SQL Injection (Error-based, Boolean-based)
- ✅ **Headers Checker**: Validación de HTTP Security Headers
- ✅ **Broken Access Control (A01)**: IDOR, escalación de privilegios, Forceful Browsing
- ✅ **Auth Failures (A07)**: Credenciales débiles, fuerza bruta suave, gestión sesiones
- ✅ **Vulnerable Components (A06)**: Detección tecnologías desactualizadas (jQuery, Bootstrap)
- ✅ **Multithreading**: Escaneo paralelo con `concurrent.futures`
- ✅ **Progress Bars**: Barras de progreso con `tqdm`
- ✅ **Chart.js Reports**: Gráficos de severidad en reportes HTML
- ✅ **Autenticación**: Soporte para login automático en sitios protegidos
- ✅ **Reportes**: Generación de reportes en JSON y HTML
- ✅ **Modo DRY-RUN**: Simulación sin ataques reales
- ✅ **Rate Limiting**: Control de velocidad para no saturar servidores
- ✅ **Aviso Legal**: Validación de permisos antes de escanear
- ✅ **Arquitectura Modular**: Fácil extensión con nuevos escáneres

## Roadmap de Desarrollo (Fases 4-6)

### Fase 4: Nuevos Escáneres OWASP (Completada)
- ✅ **A01 - Broken Access Control**: IDOR, escalación de privilegios
- ✅ **A07 - Auth Failures**: Fuerza bruta suave, sesiones débiles
- ✅ **A06 - Vulnerable Components**: Detección de librerías (SCA)

### Fase 5: Mejoras Técnicas (Completada - 60%)
- ✅ Barras de progreso (tqdm)
- ✅ Multithreading para escaneo paralelo
- ✅ Mejorar reportes (gráficos Chart.js)
- 🔄 Interfaz web básica (FastAPI/Flask)

### Fase 6: Empaquetado y Distribución (Pendiente)
- 🔄 Publicar en PyPI (`pip install vulnlab-scanner`)
- 🔄 Configurar CI/CD con GitHub Actions
- 🔄 Generar comunidad inicial

**Objetivo**: Llegar a **8/10 en funcionalidad profesional** (actualmente 6/10)

## Requisitos

- Python 3.8+
- pip

## Instalación

### Opción 1: Instalación Manual
```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/vulnlab-scanner.git
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

### Opción 2: Script Automático
```bash
python install.py
```

## Configuración

Edita el archivo `.env` para personalizar la configuración:

```env
# Tiempo máximo de espera en requests (segundos)
DEFAULT_TIMEOUT=10

# Identidad del scanner
USER_AGENT=VulnLabScanner/1.0

# Modo debug
DEBUG=False

# Segundos entre peticiones (rate limiting)
RATE_LIMIT=0.5

# Directorio de salida de reportes
REPORTS_DIR=./reports

# Formato de reporte por defecto: json, html, ambos
REPORT_FORMAT=ambos
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
│   ├── config.py               # Configuración centralizada
│   ├── core/
│   │   ├── http.py             # Cliente HTTP
│   │   └── session.py          # Gestión de sesiones
│   ├── scanner/
│   │   ├── base.py             # Clase base abstracta
│   │   ├── xss.py              # Escáner XSS
│   │   ├── sqli.py             # Escáner SQLi
│   │   └── headers.py          # Validador de headers
│   └── utils/
│       ├── logger.py           # Salida coloreada
│       ├── helpers.py          # Funciones auxiliares
│       ├── renderer.py         # Formateo de resultados
│       ├── reporter.py         # Generación de reportes
│       ├── payloads.py         # Payloads centralizados
│       └── disclaimer.py       # Aviso legal
├── tests/                      # Pruebas unitarias (43 pruebas)
├── reports/                    # Reportes generados
├── DOCS/                       # Documentación del proyecto
├── .env                        # Variables de entorno
├── requirements.txt
├── README.md
└── DISCLAIMER.md              # Aviso legal completo
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

La documentación completa está en el directorio `DOCS/`:
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

**Cobertura actual**: 43 pruebas (100% pasando)

## Contribuciones

Las contribuciones son bienvenidas. Por favor lee:
- `DOCS/ESTANDARES_CODIGO.md` antes de contribuir
- Seguir convenciones de commits: `tipo(ámbito): descripción`
- Ejecutar pruebas antes de cada commit

## Licencia

MIT License - Open Source

## Estado de Desarrollo

| Fase | Descripción | Estado |
|------|----------------|--------|
| Fase 1 | Análisis de Requisitos | ✅ Completada |
| Fase 2 | Diseño de Arquitectura | ✅ Completada |
| Fase 3 | Desarrollo (MVP) | ✅ Completada |
| Fase 4 | Nuevos Escáneres OWASP | 🔄 En progreso |
| Fase 5 | Mejoras Técnicas | ❌ Pendiente |
| Fase 6 | Empaquetado y Distribución | ❌ Pendiente |

**Siguiente hito**: Implementar A01 - Broken Access Control
