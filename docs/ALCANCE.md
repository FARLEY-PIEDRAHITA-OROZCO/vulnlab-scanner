# Alcance de VulnLab Scanner

## 1. En Alcance (In-Scope)

### Fase Actual (Fase 5.3 - Completada)
- ✅ Escaneo de XSS (Reflected, Stored, DOM-based)
- ✅ Escaneo de SQL Injection (Error-based, Boolean-based)
- ✅ Validación de HTTP Security Headers
- ✅ Gestión de sesiones con login automático
- ✅ **Escaneo de Broken Access Control (A01)** - Completado
  - Detección IDOR (Insecure Direct Object References)
  - Detección escalación privilegios
  - Detección Forceful Browsing
- ✅ **Escaneo de Authentication Failures (A07)** - Completado
  - Detección credenciales débiles/por defecto
  - Detección fuerza bruta suave
  - Verificación gestión sesiones (HttpOnly, Secure)
- ✅ **Escaneo de Vulnerable Components (A06)** - Completado
  - Detección tecnologías desactualizadas (jQuery, Bootstrap, etc.)
  - Detección CDNs vulnerables
  - Verificación headers (X-Powered-By, Server)
- ✅ **Multithreading** con concurrent.futures
- ✅ **Progress Bars** con tqdm
- ✅ **Chart.js Reports** en HTML

### Futuro (Post-Fase 4)
- Escaneo de Cryptographic Failures (A02)
- Escaneo de Injection (A03) - ampliar SQLi
- Escaneo de Security Misconfiguration (A05)
- Escaneo de Identification/Authentication Failures (A07) - ampliar
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
