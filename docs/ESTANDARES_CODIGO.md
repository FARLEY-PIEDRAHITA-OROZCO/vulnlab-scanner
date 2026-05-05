# Estándares de Código - VulnLab Scanner

## 1. Convenciones Generales
- **Lenguaje**: Python 3.8+
- **Estilo**: PEP 8 (con línea máxima de 120 caracteres para mejor legibilidad)
- **Codificación**: UTF-8
- **Docstrings**: En español, formato Google Style

## 2. Estructura de Clases

### 2.1 Clase Base (BaseScanner)
Todos los escáneres deben heredar de esta clase ubicada en `app/scanner/base.py`:

```python
from abc import ABC, abstractmethod

class BaseScanner(ABC):
    """Clase base abstracta para todos los escáneres de vulnerabilidades.
    
    Attributes:
        name (str): Nombre del escáner.
        target_url (str): URL objetivo a escanear.
        session (Session): Sesión HTTP activa.
        results (list): Lista de resultados del escaneo.
    """
    
    def __init__(self, target_url: str, session):
        """Inicializa el escáner con la URL objetivo y sesión.
        
        Args:
            target_url: URL de la aplicación a escanear.
            session: Objeto de sesión HTTP para realizar peticiones.
        """
        self.name = self.__class__.__name__
        self.target_url = target_url
        self.session = session
        self.results = []
    
    @abstractmethod
    def scan(self) -> list:
        """Ejecuta el escaneo de vulnerabilidades.
        
        Returns:
            Lista de diccionarios con resultados del escaneo.
        """
        pass
    
    @abstractmethod
    def get_payloads(self) -> list:
        """Retorna la lista de payloads para este escáner.
        
        Returns:
            Lista de strings con payloads de ataque.
        """
        pass
    
    def add_result(self, vulnerability: str, severity: str, description: str, evidence: str = ""):
        """Agrega un resultado al listado de vulnerabilidades encontradas.
        
        Args:
            vulnerability: Nombre de la vulnerabilidad.
            severity: Nivel de severidad (CRITICAL, HIGH, MEDIUM, LOW).
            description: Descripción detallada.
            evidence: Evidencia encontrada (opcional).
        """
        self.results.append({
            "scanner": self.name,
            "vulnerability": vulnerability,
            "severity": severity,
            "url": self.target_url,
            "description": description,
            "evidence": evidence,
            "timestamp": datetime.now().isoformat()
        })
```

## 3. Documentación de Módulos

Cada archivo debe incluir un docstring al inicio explicando su propósito:

```python
"""Módulo para detección de vulnerabilidades XSS (Cross-Site Scripting).

Este módulo implementa detección de:
- Reflected XSS
- Stored XSS  
- DOM-based XSS

Basado en: OWASP Top 10 - A03: Injection
"""
```

## 4. Manejo de Errores
- Usar excepciones específicas de `requests` para errores HTTP
- No usar `except Exception:` genérico, ser específicos
- Los errores deben registrarse en `self.results` con severidad "ERROR"

## 5. Payloads
- **NUNCA** hardcodear payloads en el código del escáner
- Almacenar en `app/utils/payloads.py` organizados por categoría
- Formato de payloads: `{"type": "xss_reflected", "value": "<script>alert(1)</script>"}`

## 6. Salida y Logging
- Usar `app/utils/logger.py` para salida en consola
- Niveles: `info()`, `success()`, `warning()`, `error()`
- Colores: Verde=éxito, Rojo=error, Amarillo=advertencia, Azul=info

## 7. Configuración
- Variables sensibles (contraseñas) en `.env`
- Configuración general en `app/config.py`
- No subir `.env` al repositorio (debe estar en `.gitignore`)

## 8. Pruebas
- Cada módulo debe tener su archivo de prueba en `tests/`
- Formato: `test_[modulo].py`
- Usar `pytest` como framework de pruebas
