# Guía de Usuario - VulnLab Scanner

## Introducción
VulnLab Scanner es una herramienta profesional para escaneo automatizado de vulnerabilidades web basada en OWASP Top 10.

## Instalación

### Requisitos previos
- Python 3.8 o superior instalado
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio** (si aplica) o descargar el código fuente

2. **Crear entorno virtual** (recomendado):
```bash
python -m venv .venv
```

3. **Activar entorno virtual**:
   - **Windows**: `.\.venv\Scripts\activate`
   - **Linux/Mac**: `source .venv/bin/activate`

4. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

5. **Configurar variables de entorno** (opcional):
Editar el archivo `.env` según tus necesidades.

## Configuración

### Archivo `.env`
Puedes configurar los siguientes parámetros en el archivo `.env`:

```env
# Tiempo máximo de espera en requests (segundos)
DEFAULT_TIMEOUT=10

# Identidad del scanner
USER_AGENT=VulnLabScanner/1.4.2

# Modo debug
DEBUG=False

# Segundos entre peticiones (rate limiting)
RATE_LIMIT=0.5

# Directorio de salida de reportes
REPORTS_DIR=./reports

# Formato de reporte por defecto: json, html, ambos
REPORT_FORMAT=ambos
```

## Uso Básico

### Escaneo simple
```bash
python -m app.main -u http://ejemplo.com --all
```

### Opciones disponibles

#### Argumentos principales
- `-u, --url`: URL del sitio a escanear (obligatorio)
- `-x, --xss`: Escanear vulnerabilidades XSS
- `-s, --sqli`: Escanear vulnerabilidades SQL Injection
- `-H, --headers`: Validar HTTP Security Headers
- `-a, --all`: Ejecutar todos los escáneres disponibles

#### Autenticación (para sitios que requieren login)
```bash
python -m app.main -u http://ejemplo.com --all \
  --login-url http://ejemplo.com/login \
  --username mi_usuario \
  --password mi_password
```

Opciones adicionales de autenticación:
- `--login-username-field`: Nombre del campo usuario (default: username)
- `--login-password-field`: Nombre del campo contraseña (default: password)

#### Reportes
```bash
# Solo JSON
python -m app.main -u http://ejemplo.com --all --report-format json

# Solo HTML
python -m app.main -u http://ejemplo.com --all --report-format html

# Ambos (por defecto)
python -m app.main -u http://ejemplo.com --all --report-format ambos

# Cambiar directorio de salida
python -m app.main -u http://ejemplo.com --all --report-output ./mis_reportes
```

#### Opciones adicionales
- `--dry-run`: Simular escaneo sin enviar ataques reales
- `--rate-limit`: Segundos entre peticiones (default: 0.5)
- `--disclaimer`: Mostrar aviso legal y salir
- `-v, --verbose`: Modo verbose (más detalles)

## Ejemplos de Uso

### Ejemplo 1: Escaneo completo con autenticación
```bash
python -m app.main -u http://juiceshop:3000 --all \
  --login-url http://juiceshop:3000/#/login \
  --username admin@juice-sh.op \
  --password admin123 \
  --report-format ambos
```

### Ejemplo 2: Solo verificar headers de seguridad
```bash
python -m app.main -u https://www.google.com --headers
```

### Ejemplo 3: Probar XSS en modo simulación
```bash
python -m app.main -u http://test.com/search?q=test --xss --dry-run
```

## Interpretación de Resultados

### Salida en consola
La herramienta usa colores para identificar:
- **Verde**: Operación exitosa
- **Rojo**: Error
- **Amarillo**: Advertencia
- **Azul**: Información
- **Magenta**: Vulnerabilidad detectada

### Reportes
Los reportes se guardan en el directorio `reports/` (o el directorio configurado):

#### JSON
Estructura detallada para procesamiento con otras herramientas.

#### HTML
Reporte visual para revisar en el navegador con:
- Resumen de vulnerabilidades por severidad
- Detalles de cada vulnerabilidad encontrada
- Evidencia y recomendaciones

## Niveles de Severidad

- **CRITICAL**: Vulnerabilidades críticas que requieren atención inmediata
- **HIGH**: Vulnerabilidades altas con riesgo significativo
- **MEDIUM**: Vulnerabilidades medias
- **LOW**: Vulnerabilidades bajas o configuraciones mejorables

## Aviso Legal

Al usar esta herramienta, debes:
1. Tener autorización explícita para escanear el objetivo
2. Usar la herramienta solo con fines éticos
3. Aceptar la responsabilidad del uso que le des

Para ver el aviso legal completo:
```bash
python -m app.main --disclaimer
```

## Solución de Problemas

### Error: "La URL debe comenzar con http:// o https://"
Asegúrate de incluir el protocolo en la URL (ej: `http://` o `https://`)

### Error de timeout
Aumenta el valor de `DEFAULT_TIMEOUT` en el archivo `.env`

### Fallo en autenticación
Verifica:
- Que la `--login-url` sea correcta
- Que las credenciales sean válidas
- Que los nombres de campos sean correctos (--login-username-field, --login-password-field)

## Limitaciones Actuales

- Solo soporta inyección en parámetros GET (no POST aún)
- La detección de XSS es básica (reflejado)
- SQLi funciona mejor con bases de datos que muestran errores

## Siguientes Pasos (Roadmap)

- Soporte para escaneo de formularios POST
- Mejor detección de XSS Stored y DOM-based
- Escáneres para: Broken Access Control, Auth Failures
- Integración con CI/CD
