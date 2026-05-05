# Alcance de VulnLab Scanner

## 1. En Alcance (In-Scope)

### Fase Actual (MVP - Producto Mínimo Viable)
- Escaneo de XSS (Reflected, Stored, DOM-based)
- Escaneo de SQL Injection (Error-based, Boolean-based)
- Validación de HTTP Security Headers
- Gestión de sesiones con login automático (usuario/contraseña)
- Generación de reportes JSON y HTML
- Interfaz CLI con flags de configuración
- Aviso legal obligatorio antes de escanear

### Futuro (Post-MVP)
- Escaneo de Broken Access Control
- Escaneo de Authentication Failures
- Escaneo de Vulnerable Components
- Modo interactivo (opcional)

## 2. Fuera de Alcance (Out-of-Scope)

- **No** se incluye escaneo de redes (solo aplicaciones web)
- **No** se incluye fuzzing de directorios/archivos
- **No** se incluye ataques de fuerza bruta
- **No** se desarrollará interfaz gráfica (GUI)
- **No** se soporta escaneo distribuido/múltiples targets simultáneos
- **No** se incluye explotación automática (solo detección)

## 3. Supuestos
- El usuario tiene permisos legales para escanear el objetivo
- El sitio objetivo es accesible vía HTTP/HTTPS
- Python 3.8+ está instalado en el sistema
- El usuario tiene conocimientos básicos de línea de comandos

## 4. Criterios de Aceptación
- El escáner detecta correctamente vulnerabilidades en entornos de prueba (ej: OWASP Juice Shop)
- Los reportes generados son legibles y contienen información útil
- La instalación no requiere más de 3 comandos
- El código cumple con estándares PEP8 y está documentado
