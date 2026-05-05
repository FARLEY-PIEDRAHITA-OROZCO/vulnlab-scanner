# Changelog - VulnLab Scanner

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto sigue el [Semantic Versioning](https://semver.org/lang/es/).

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
