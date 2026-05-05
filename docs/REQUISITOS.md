# Requisitos de VulnLab Scanner

## 1. Introducción
VulnLab Scanner es una herramienta de escaneo de vulnerabilidades web diseñada para automatizar pruebas basadas en el estándar OWASP Top 10. Enfocada en uso profesional, permite detectar fallos de seguridad comunes de manera modular, fácil de instalar, configurar y usar.

## 2. Requisitos Funcionales

### 2.1 Escaneo de Vulnerabilidades OWASP
- **RF-01**: La herramienta debe detectar vulnerabilidades XSS (Cross-Site Scripting)
- **RF-02**: La herramienta debe detectar inyecciones SQL (SQL Injection)
- **RF-03**: La herramienta debe validar configuraciones de seguridad en headers HTTP
- **RF-04**: La herramienta debe detectar fallos de control de acceso (futuro)
- **RF-05**: La herramienta debe detectar fallos de autenticación (futuro)

### 2.2 Autenticación
- **RF-06**: La herramienta debe soportar escaneo de sitios que requieran inicio de sesión
- **RF-07**: Debe permitir configurar credenciales (usuario/contraseña) para login automático
- **RF-08**: Debe mantener la sesión activa durante todo el escaneo

### 2.3 Reportes
- **RF-09**: Generar reportes en formato JSON (estructurado para procesamiento)
- **RF-10**: Generar reportes en formato HTML (visual para revisión en navegador)
- **RF-11**: Los reportes deben incluir: vulnerabilidad detectada, URL, severidad, recomendación

### 2.4 Interfaz de Usuario
- **RF-12**: La herramienta se ejecutará exclusivamente por línea de comandos (CLI)
- **RF-13**: Debe soportar flags para seleccionar tipo de escaneo (--xss, --sqli, --headers, --all)
- **RF-14**: Debe validar que la URL objetivo use http:// o https://

### 2.5 Seguridad Legal
- **RF-15**: Mostrar aviso legal antes de cada escaneo
- **RF-16**: Requerir confirmación explícita de que el usuario tiene permisos para escanear

## 3. Requisitos No Funcionales

### 3.1 Usabilidad
- **RNF-01**: Instalación mediante un solo comando (pip install o script)
- **RNF-02**: Configuración inicial mediante archivo .env o flags CLI
- **RNF-03**: Mensajes de salida en español, claros y coloridos

### 3.2 Modularidad
- **RNF-04**: Cada tipo de vulnerabilidad debe ser un módulo independiente
- **RNF-05**: Código documentado con docstrings en español
- **RNF-06**: Uso de una clase base común para todos los escáneres

### 3.3 Rendimiento
- **RNF-07**: Implementar rate limiting para no saturar el servidor objetivo
- **RNF-08**: Opción de ejecución en modo "dry-run" (solo simular, no atacar)

## 4. Restricciones
- Solo compatible con Python 3.8+
- Dependencias mínimas (requests, colorama, python-dotenv)
- No se incluye interfaz gráfica (GUI) en esta versión
