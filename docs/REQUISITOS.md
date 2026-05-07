# Requisitos de VulnLab Scanner v1.4.3

## 1. Introducción

VulnLab Scanner es una herramienta de escaneo de vulnerabilidades web diseñada para automatizar pruebas basadas en el estándar OWASP Top 10 (2021). Enfocada en uso profesional, permite detectar fallos de seguridad comunes de manera modular, fácil de instalar, configurar y usar.

**Versión actual**: 1.4.3
**Cobertura OWASP**: 8/10 (80%) + XSS extra
**Estado**: Listo para producción y publicación en PyPI

## 2. Requisitos Funcionales

### 2.1 Escaneo de Vulnerabilidades OWASP
- **RF-01**: La herramienta debe detectar vulnerabilidades XSS (Cross-Site Scripting) - Reflected, Stored, DOM-based ✅
- **RF-02**: La herramienta debe detectar inyecciones SQL (SQL Injection) - Error-based, Boolean-based ✅
- **RF-03**: La herramienta debe validar configuraciones de seguridad en headers HTTP ✅
- **RF-04**: La herramienta debe detectar Broken Access Control (A01) - IDOR, Privilege Escalation ✅
- **RF-05**: La herramienta debe detectar Authentication Failures (A07) - Weak Creds, Brute Force ✅
- **RF-06**: La herramienta debe detectar Vulnerable Components (A06) - jQuery, Bootstrap ✅
- **RF-07**: La herramienta debe detectar Cryptographic Failures (A02) - HTTPS, Cookies, URLs ✅
- **RF-08**: La herramienta debe detectar SSRF (A10) - Params, Internal IPs ✅
- **RF-09**: La herramienta debe detectar SQL Injection ampliado (A03) ✅

### 2.2 Autenticación
- **RF-10**: La herramienta debe soportar escaneo de sitios que requieran inicio de sesión ✅
- **RF-11**: Debe permitir configurar credenciales (usuario/contraseña) para login automático ✅
- **RF-12**: Debe mantener la sesión activa durante todo el escaneo ✅
- **RF-13**: Debe soportar campos de login personalizados (username field, password field) ✅

### 2.3 Reportes
- **RF-14**: Generar reportes en formato JSON (estructurado para procesamiento) ✅
- **RF-15**: Generar reportes en formato HTML (visual para revisión en navegador) ✅
- **RF-16**: Los reportes deben incluir: vulnerabilidad detectada, URL, severidad, recomendación ✅
- **RF-17**: Reportes HTML deben incluir gráficos Chart.js de severidad ✅
- **RF-18**: Debe permitir seleccionar directorio de salida para reportes ✅

### 2.4 Interfaz de Usuario
- **RF-19**: La herramienta se ejecutará exclusivamente por línea de comandos (CLI) ✅
- **RF-20**: Debe soportar flags para seleccionar tipo de escaneo (--xss, --sqli, etc.) ✅
- **RF-21**: Debe validar que la URL objetivo use http:// o https:// ✅
- **RF-22**: Debe mostrar barras de progreso (tqdm) durante el escaneo ✅
- **RF-23**: Debe soportar modo verbose (-v) para más detalles ✅

### 2.5 Seguridad Legal
- **RF-24**: Mostrar aviso legal antes de cada escaneo ✅
- **RF-25**: Requerir confirmación explícita de que el usuario tiene permisos para escanear ✅
- **RF-26**: Debe permitir modo dry-run (simulación sin ataques reales) ✅

### 2.6 Arquitectura Modular
- **RF-27**: Cada tipo de vulnerabilidad debe ser un módulo independiente ✅
- **RF-28**: Debe existir una clase base común para todos los escáneres (BaseScanner) ✅
- **RF-29**: Debe soportar multithreading para escaneo paralelo ✅
- **RF-30**: Configuración centralizada vía archivo .env y clase Config ✅

## 3. Requisitos No Funcionales

### 3.1 Usabilidad
- **RNF-01**: Instalación mediante un solo comando (pip install) o máximo 3 pasos ✅
- **RNF-02**: Configuración inicial mediante archivo .env o flags CLI ✅
- **RNF-03**: Mensajes de salida en español, claros y coloridos (colorama) ✅
- **RNF-04**: Documentación completa en español ✅

### 3.2 Modularidad y Calidad
- **RNF-05**: Cada escáner debe ser un módulo independiente ✅
- **RNF-06**: Código documentado con docstrings en español ✅
- **RNF-07**: Uso de type hints en funciones principales ✅
- **RNF-08**: Cumplimiento de estándares PEP 8 ✅
- **RNF-09**: Pruebas unitarias con cobertura del 100% en módulos implementados ✅
- **RNF-10**: Uso de pre-commit hooks para linting y formateo ✅

### 3.3 Rendimiento y Seguridad
- **RNF-11**: Implementar rate limiting para no saturar el servidor objetivo ✅
- **RNF-12**: Opción de ejecución en modo "dry-run" (solo simular, no atacar) ✅
- **RNF-13**: Cliente HTTP con reintentos y manejo de errores ✅
- **RNF-14**: Validación de permisos antes de cada escaneo ✅
- **RNF-15**: No almacenar credenciales en texto plano ✅

### 3.4 Empaquetado y Distribución
- **RNF-16**: Empaquetado compatible con PyPI (setup.py, pyproject.toml) ✅
- **RNF-17**: CI/CD configurado con GitHub Actions ✅
- **RNF-18**: Manifest.in para control de archivos incluidos ✅
- **RNF-19**: Documentación de variables en .env.example ✅
- **RNF-20**: Licencia MIT (Open Source) ✅

## 4. Restricciones

- **R-01**: Solo compatible con Python 3.8+
- **R-02**: Dependencias mínimas (requests, colorama, python-dotenv, jinja2, tqdm)
- **R-03**: No se incluye interfaz gráfica (GUI) en esta versión
- **R-04**: No se soporta escaneo distribuido/múltiples targets simultáneos
- **R-05**: No se incluye explotación automática (solo detección)
- **R-06**: Límite de 5 intentos de fuerza bruta suave por defecto

## 5. Supuestos

- **S-01**: El usuario tiene permisos legales para escanear el objetivo
- **S-02**: El sitio objetivo es accesible vía HTTP/HTTPS
- **S-03**: Python 3.8+ está instalado en el sistema
- **S-04**: El usuario tiene conocimientos básicos de línea de comandos
- **S-05**: El entorno de ejecución tiene acceso a internet (para instalación de dependencias)

## 6. Criterios de Aceptación

### 6.1 Funcionalidad
- ✅ El escáner detecta correctamente vulnerabilidades en entornos de prueba (ej: OWASP Juice Shop)
- ✅ Los reportes generados son legibles y contienen información útil
- ✅ La instalación no requiere más de 3 comandos
- ✅ El código cumple con estándares PEP 8 y está documentado

### 6.2 Calidad
- ✅ 114 pruebas unitarias pasando (109 passed, 5 skipped)
- ✅ Cobertura de pruebas del 100% en módulos implementados
- ✅ Falsos positivos < 5%
- ✅ Tiempo de escaneo razonable (< 5 min para escaneo completo)

### 6.3 Profesionalismo
- ✅ Documentación completa en español
- ✅ Archivos profesionales: SECURITY.md, CODE_OF_CONDUCT.md, etc.
- ✅ CI/CD operativo con GitHub Actions
- ✅ Preparado para publicación en PyPI

## 7. Métricas de Éxito

| Métrica | Objetivo | Estado Actual |
|---------|----------|--------------|
| Cobertura OWASP | 8/10 (80%) | ✅ 8/10 + XSS |
| Pruebas unitarias | >100 | ✅ 114 total |
| Pruebas pasando | 100% | ✅ 109 passed |
| Falsos positivos | <5% | ✅ <5% |
| Tiempo instalación | <3 comandos | ✅ 1 comando (pip) |
| Documentación | Completa | ✅ En español |

---

**Versión del documento**: 1.4.2
**Fecha de actualización**: 2026-05-06
**Responsable**: @FARLEY-PIEDRAHITA-OROZCO
**Estado**: ✅ Completo y actualizado a v1.4.3
