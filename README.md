# VulnLab Scanner

Herramienta profesional de escaneo de vulnerabilidades web basada en OWASP Top 10, diseñada para automatizar pruebas de seguridad de manera modular, fácil de instalar y usar.

## Características

- ✅ **XSS Scanner**: Detección de Cross-Site Scripting (Reflected, Stored, DOM-based)
- ✅ **SQLi Scanner**: Detección de SQL Injection (Error-based, Boolean-based)
- ✅ **Headers Checker**: Validación de HTTP Security Headers
- ✅ **Autenticación**: Soporte para login automático en sitios protegidos
- ✅ **Reportes**: Generación de reportes en JSON y HTML
- ✅ **Modo DRY-RUN**: Simulación sin ataques reales
- ✅ **Rate Limiting**: Control de velocidad para no saturar servidores
- ✅ **Aviso Legal**: Validación de permisos antes de escanear

## Requisitos

- Python 3.8+
- pip

## Instalación

1. **Clonar el repositorio** (o descargar el código):
```bash
git clone https://github.com/tu-usuario/vulnlab-scanner.git
cd vulnlab-scanner
```

2. **Crear entorno virtual** (recomendado):
```bash
python -m venv .venv
```

3. **Activar entorno virtual**:
   - **Windows**:
   ```bash
   .\.venv\Scripts\activate
   ```
   - **Linux/Mac**:
   ```bash
   source .venv/bin/activate
   ```

4. **Instalar dependencias**:
```bash
pip install -r requirements.txt
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
├── tests/                      # Pruebas unitarias
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
- `DOCS/GUIA_USUARIO.md` - Guía de usuario
- `DOCS/ROADMAP.md` - Futuras mejoras

## Pruebas

Para ejecutar las pruebas unitarias:
```bash
pytest tests/ -v
```

## Estado del Proyecto

**Fase actual**: Fase 3 - Desarrollo (Completado)
- ✅ Arquitectura modular implementada
- ✅ Escáneres OWASP básicos funcionando
- ✅ Pruebas unitarias (17 pruebas, 100% pasando)
- ✅ Documentación completa

## Roadmap

- [ ] Soporte para formularios POST
- [ ] Mejorar detección XSS Stored y DOM-based
- [ ] Escáner de Broken Access Control
- [ ] Escáner de Authentication Failures
- [ ] Integración con CI/CD

## Licencia

[Especificar licencia aquí]

## Contribuciones

Las contribuciones son bienvenidas. Por favor lee `DOCS/ESTANDARES_CODIGO.md` antes de contribuir.
