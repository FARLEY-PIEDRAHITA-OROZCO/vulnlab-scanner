# Guía de Usuario - VulnLab Scanner v1.5.0

## Introducción

VulnLab Scanner es una herramienta profesional para escaneo automatizado de vulnerabilidades web basada en OWASP Top 10 (2021). Diseñada para pruebas de seguridad éticas, cuenta con una arquitectura modular, configuración flexible y reportes detallados.

**Versión actual**: 1.5.0
**Cobertura OWASP**: 10/10 (100%) + XSS extra
**Licencia**: MIT (Open Source)

## Instalación

### Requisitos previos
- Python 3.8 o superior instalado
- pip (gestor de paquetes de Python)
- Git (para instalación desde código fuente)

### Opción 1: Instalación desde PyPI (Recomendada)
```bash
pip install vulnlab-scanner
```

### Opción 2: Instalación para Desarrollo
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

### Verificación de instalación
```bash
python -c "import app; print(f'VulnLab Scanner v{app.__version__}')"
# Debería mostrar: VulnLab Scanner v1.4.2
```

## Configuración

### Archivo `.env`

Crea un archivo `.env` en la raíz del proyecto (puedes copiar de `.env.example`):

```env
# Configuración General
DEBUG=False
VERBOSE=False

# Configuración de HTTP
RATE_LIMIT=0.5
DEFAULT_TIMEOUT=10
USER_AGENT=VulnLabScanner/1.4.2
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

### Variables de entorno explicadas

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DEBUG` | Modo debug con información detallada | `False` |
| `VERBOSE` | Salida verbose en consola | `False` |
| `RATE_LIMIT` | Segundos entre peticiones (rate limiting) | `0.5` |
| `DEFAULT_TIMEOUT` | Tiempo máximo de espera en requests (segundos) | `10` |
| `USER_AGENT` | Identidad del scanner en requests HTTP | `VulnLabScanner/1.4.2` |
| `MAX_RETRIES` | Número máximo de reintentos en requests | `3` |
| `DEFAULT_LOGIN_PATHS` | Rutas comunes de login (separadas por coma) | `/login,/signin,...` |
| `DEFAULT_BRUTE_FORCE_ATTEMPTS` | Intentos máximos para fuerza bruta | `3` |
| `DEFAULT_BRUTE_FORCE_PASSWORDS` | Contraseñas comunes para pruebas | `123456,password,...` |
| `DEFAULT_ADMIN_PATHS` | Rutas administrativas a probar | `/admin,/administrator,...` |
| `REPORTS_DIR` | Directorio de salida para reportes | `reports` |

## Uso Básico

### Escaneo simple
```bash
python -m app.main -u http://ejemplo.com --all
```

### Opciones disponibles

#### Argumentos principales
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
  -a, --all              Ejecutar todos los escáneres disponibles
```

#### Autenticación (para sitios que requieren login)
```bash
python -m app.main -u http://ejemplo.com --all \
  --login-url http://ejemplo.com/login \
  --username mi_usuario \
  --password mi_password
```

#### Opciones de autenticación
```
  --login-url URL        URL de la página de login
  --username USER        Usuario para autenticación
  --password PASS        Contraseña para autenticación
  --login-username-field NAME   Campo usuario (default: username)
  --login-password-field NAME   Campo password (default: password)
```

#### Reportes
```
  --report-format FMT    Formato: json, html, ambos (default: ambos)
  --output-dir DIR       Directorio de salida (default: ./reports)
```

#### Opciones adicionales
```
  --dry-run              Simular sin ataques reales (no envía ataques)
  --rate-limit SEC       Segundos entre peticiones (default: 0.5)
  --disclaimer           Mostrar aviso legal y salir
  --no-disclaimer        Omitir aviso legal (no recomendado)
  -v, --verbose         Modo verbose (más detalles)
```

## Ejemplos de Uso

### Ejemplo 1: Escaneo completo con autenticación
```bash
python -m app.main -u http://juiceshop:3000 --all \
  --login-url http://juiceshop:3000/#/login \
  --username admin@juice-sh.op \
  --password admin123
```

### Ejemplo 2: Solo verificar headers de seguridad
```bash
python -m app.main -u https://www.google.com --headers
```

### Ejemplo 3: Probar XSS en modo simulación (dry-run)
```bash
python -m app.main -u "http://test.com/search?q=test" --xss --dry-run
```

### Ejemplo 4: Escaneo de múltiples vulnerabilidades con salida verbose
```bash
python -m app.main -u http://example.com -x -s -H -v
```

### Ejemplo 5: Generar solo reporte JSON en directorio personalizado
```bash
python -m app.main -u http://example.com --all \
  --report-format json \
  --output-dir ./mis_reportes
```

## Escáneres Disponibles

### A01 - Broken Access Control
Detecta problemas como:
- IDOR (Insecure Direct Object References)
- Escalación de privilegios
- Forceful Browsing (saltos de autenticación)

**Uso**: `--access-control` o `-A`

### A02 - Cryptographic Failures
Detecta:
- HTTPS faltante
- Cookies sin flags Secure
- Credenciales en URLs

**Uso**: `--crypto` o `-K`

### A03 - SQL Injection
Detecta inyección SQL:
- Error-based
- Boolean-based

**Uso**: `--sqli` o `-s`

### A05 - Security Misconfiguration
Valida HTTP Security Headers:
- Strict-Transport-Security
- X-Content-Type-Options
- X-Frame-Options
- Content-Security-Policy
- X-XSS-Protection

**Uso**: `--headers` o `-H`

### A06 - Vulnerable Components
Detecta librerías desactualizadas:
- jQuery
- Bootstrap
- Otros componentes con vulnerabilidades conocidas

**Uso**: `--vuln-components` o `-C`

### A07 - Auth Failures
Detecta problemas de autenticación:
- Credenciales débiles
- Fuerza bruta suave
- Gestión de sesiones inseguras

**Uso**: `--auth` o `-U`

### A10 - SSRF (Server-Side Request Forgery)
Detecta vulnerabilidades SSRF:
- Parámetros de URL (`?url=`, `?redirect=`)
- IPs internas y esquemas peligrosos

**Uso**: `--ssrf` o `-R`

### XSS Scanner (Extra)
Detecta Cross-Site Scripting:
- Reflected XSS
- Stored XSS
- DOM-based XSS

**Uso**: `--xss` o `-x`

## Reportes

### Formato JSON
Contiene toda la información del escaneo en formato JSON:
```json
{
  "scan_info": {
    "target_url": "http://example.com",
    "timestamp": "2026-05-06T16:30:00",
    "scanner_version": "1.4.2",
    "options": {...}
  },
  "results": [...],
  "summary": {
    "total_vulnerabilities": 5,
    "critical": 0,
    "high": 2,
    "medium": 2,
    "low": 1
  }
}
```

### Formato HTML
Reporte visual con:
- Resumen ejecutivo
- Gráficos Chart.js de severidad
- Detalles de cada vulnerabilidad
- Recomendaciones de corrección

### Ubicación de reportes
Por defecto en el directorio `reports/` (configurable vía `REPORTS_DIR` en `.env`)

## Modo DRY-RUN

El modo dry-run permite simular el escaneo sin enviar ataques reales:
```bash
python -m app.main -u http://example.com --all --dry-run
```

**Útil para**:
- Verificar configuración antes de escanear
- Pruebas en entornos de producción (sin riesgo)
- Entender qué haría el escáner

## Aviso Legal y Ética

### Aviso Legal Integrado
Al usar VulnLab Scanner, declaras que:
1. Solo escanearás sistemas para los cuales tienes autorización explícita
2. No usarás la herramienta para actividades ilegales
3. Eres responsable del uso que le des a los resultados

### Ver aviso legal completo
```bash
python -m app.main --disclaimer
```

### Recomendaciones éticas
- ✅ Obtener autorización por escrito antes de escanear
- ✅ Usar en entornos de prueba/staging, no producción
- ✅ Notificar al propietario sobre vulnerabilidades encontradas
- ❌ No usar para atacar sistemas ajenos
- ❌ No realizar ataques de denegación de servicio (DoS)

## Solución de Problemas

### Error: "No se puede conectar al host"
- Verifica que la URL sea correcta y accesible
- Revisa tu conexión a internet
- Aumenta `DEFAULT_TIMEOUT` en `.env`

### Error: "HTTP 403 Forbidden"
- El sitio puede tener protección WAF
- Intenta con `--rate-limit 1.0` (más lento)
- Verifica si requiere autenticación

### Los reportes no se generan
- Verifica permisos de escritura en `REPORTS_DIR`
- Revisa que el directorio exista o se pueda crear
- Ejecuta con `-v` para ver detalles

### Problemas con autenticación
- Verifica que `--login-url` sea correcta
- Revisa los nombres de campos (`--login-username-field`, `--login-password-field`)
- Usa `--dry-run` para probar sin atacar

## Soporte y Contacto

- **Repositorio**: https://github.com/FARLEY-PIEDRAHITA-OROZCO/vulnlab-scanner
- **Issues**: https://github.com/FARLEY-PIEDRAHITA-OROZCO/vulnlab-scanner/issues
- **Seguridad**: security@vulnlab.com
- **Documentación**: Directorio `docs/` del proyecto

## Referencias

- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Python requests documentation](https://docs.python-requests.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)

---

**Última actualización**: 2026-05-06 (v1.4.2)
**Autor**: VulnLab Team
**Licencia**: MIT (Open Source)
