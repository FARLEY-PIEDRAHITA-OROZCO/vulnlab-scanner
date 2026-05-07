# Estándares de Código - VulnLab Scanner v1.4.3

## 1. Convenciones Generales

- **Lenguaje**: Python 3.8+
- **Estilo**: PEP 8 (con línea máxima de 127 caracteres para mejor legibilidad)
- **Codificación**: UTF-8
- **Docstrings**: En español, formato Google Style
- **Comentarios**: Evitar comentarios innecesarios (el código debe ser autodocumentado)
- **Nombres**:
  - Clases: `PascalCase` (ej. `BaseScanner`)
  - Funciones/métodos: `snake_case` (ej. `get_payloads`)
  - Constantes: `UPPER_SNAKE_CASE` (ej. `MAX_RETRIES`)
  - Variables: `snake_case` (ej. `target_url`)

## 2. Estructura de Clases

### 2.1 Clase Base (BaseScanner)
Todos los escáneres deben heredar de esta clase ubicada en `app/scanner/base.py`:

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseScanner(ABC):
    """Clase base abstracta para todos los escáneres de vulnerabilidades.

    Attributes:
        name (str): Nombre del escáner.
        target_url (str): URL objetivo a escanear.
        session: Sesión HTTP activa.
        results (list): Lista de resultados del escaneo.
        dry_run (bool): Si es True, solo simula sin atacar.
    """

    def __init__(self, target_url: str, session, dry_run: bool = False):
        """Inicializa el escáner con la URL objetivo y sesión.

        Args:
            target_url: URL de la aplicación a escanear.
            session: Objeto de sesión HTTP para realizar peticiones.
            dry_run: Si es True, simula sin realizar ataques.
        """
        self.name = self.__class__.__name__
        self.target_url = target_url
        self.session = session
        self.results = []
        self.dry_run = dry_run

    @abstractmethod
    def scan(self) -> List[Dict[str, Any]]:
        """Ejecuta el escaneo de vulnerabilidades.

        Returns:
            Lista de diccionarios con resultados del escaneo.
        """
        pass

    @abstractmethod
    def get_payloads(self) -> List[str]:
        """Retorna la lista de payloads para este escáner.

        Returns:
            Lista de strings con los payloads.
        """
        pass

    def add_result(self, vuln_name: str, severity: str,
                  description: str, evidence: str) -> None:
        """Añade un resultado del escaneo a la lista de resultados.

        Args:
            vuln_name: Nombre de la vulnerabilidad.
            severity: Severidad (CRITICAL, HIGH, MEDIUM, LOW).
            description: Descripción de la vulnerabilidad.
            evidence: Evidencia encontrada.
        """
        self.results.append({
            "vulnerability": vuln_name,
            "severity": severity,
            "description": description,
            "evidence": evidence
        })
```

## 3. Docstrings (Google Style en Español)

### 3.1 Formato para Clases
```python
class MiScanner(BaseScanner):
    """Breve descripción de lo que hace el escáner.

    Descripción más detallada si es necesario, explicando
    qué vulnerabilidades detecta y cómo funciona.

    Attributes:
        attr1 (str): Descripción del atributo 1.
        attr2 (int): Descripción del atributo 2.
    """
```

### 3.2 Formato para Métodos/Funciones
```python
def mi_funcion(param1: str, param2: int = 10) -> bool:
    """Breve descripción de lo que hace la función.

    Args:
        param1: Descripción del parámetro 1.
        param2: Descripción del parámetro 2 (default: 10).

    Returns:
        True si éxito, False en caso contrario.

    Raises:
        ValueError: Si param1 está vacío.
    """
    pass
```

## 4. Type Hints

- Usar type hints en todas las funciones y métodos públicos
- Usar `typing` para tipos complejos
- Ejemplos:
```python
from typing import List, Dict, Optional

def procesar_datos(data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Procesa una lista de diccionarios."""
    pass
```

## 5. Manejo de Errores

### 5.1 Excepciones
- Capturar excepciones específicas, no `Exception` genérica
- Usar `logging` para registrar errores
- No usar `print()` para depuración (usar `logger` o `print` de colorama)

```python
import logging
from requests.exceptions import RequestException

try:
    response = self.session.get(url)
except RequestException as e:
    logging.error(f"Error al conectar con {url}: {e}")
    return None
```

### 5.2 Validaciones
- Validar argumentos de entrada al inicio de funciones
- Usar `is_valid_url()` de `helpers.py` para URLs

## 6. Imports

### 6.1 Orden (sugerido por PEP 8)
1. Módulos estándar de Python
2. Módulos de terceros (requests, colorama, etc.)
3. Módulos locales (app.*)

```python
# Módulos estándar
import os
import re
from typing import List, Dict

# Módulos de terceros
import requests
from colorama import Fore

# Módulos locales
from app.scanner.base import BaseScanner
from app.utils.payloads import MI_PAYLOADS
```

### 6.2 Formato
- Un import por línea
- Usar `from X import Y` para importaciones específicas
- Evitar `from module import *`

## 7. Configuración (app/config.py)

- Usar la clase `Config` para valores configurables
- Obtener de variables de entorno con `os.getenv()`
- Proporcionar valores por defecto razonables

## 8. Pruebas Unitarias

### 8.1 Convenciones
- Archivos de pruebas: `test_<modulo>.py`
- Clases de prueba: `Test<Clase>`
- Métodos de prueba: `test_<funcionalidad>`
- Usar `pytest` y `unittest.mock` para mocking

### 8.2 Estructura de Pruebas
```python
import unittest
from unittest.mock import Mock, patch
import pytest

class TestMiScanner(unittest.TestCase):
    """Pruebas para MiScanner."""

    def setUp(self):
        """Configuración antes de cada prueba."""
        self.session = Mock()
        self.scanner = MiScanner("http://example.com", self.session)

    def test_initialization(self):
        """Prueba que el escáner se inicializa correctamente."""
        self.assertEqual(self.scanner.target_url, "http://example.com")
        self.assertEqual(self.scanner.name, "MiScanner")

    @patch('app.scanner.mi_scanner.requests.get')
    def test_scan_sin_vulnerabilidades(self, mock_get):
        """Prueba escaneo sin detectar vulnerabilidades."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "sin vulnerabilidades"
        mock_get.return_value = mock_response

        results = self.scanner.scan()
        self.assertEqual(len(results), 0)
```

## 9. Linting y Formateo

### 9.1 Herramientas Configuradas
- **flake8**: Linting (`.flake8` o `setup.cfg`)
  - max-line-length: 127
  - max-complexity: 10
  - ignore: E203, W503

- **black**: Formateo automático
  - line-length: 127

- **isort**: Ordenamiento de imports
  - profile: black

- **bandit**: Análisis de seguridad
  - Excluir tests/

### 9.2 Pre-commit Hooks
Configurado en `.pre-commit-config.yaml`:
- black, isort, flake8, bandit
- trailing-whitespace, end-of-file-fixer
- check-yaml, debug-statements

## 10. Logger (app/utils/logger.py)

Usar las funciones de `logger.py` para salida en consola:
```python
from app.utils.logger import info, success, warning, error

info("Mensaje informativo")
success("Operación exitosa")
warning("Advertencia")
error("Error ocurrido")
```

## 11. Commits Convencionales

Seguir el formato: `tipo(ámbito): descripción en español`

### Tipos:
- `feat`: Nueva característica
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formateo (no cambia lógica)
- `refactor`: Refactorización (no fix ni feat)
- `test`: Añadir o corregir pruebas
- `chore`: Tareas de mantenimiento

### Ejemplos:
```
feat(scanner): implementar A10 - SSRF scanner
fix(config): corregir USER_AGENT en config.py
docs(readme): actualizar badges y cobertura OWASP
test(ssrf): añadir 9 pruebas unitarias para SSRFScanner
```

## 12. Git Workflow

### 12.1 Ramas
- `main`: Producción estable
- `develop`: Desarrollo activo
- `feature/*`: Nuevas características
- `fix/*`: Correcciones

### 12.2 Flujo
1. Crear rama desde `develop`
2. Implementar cambios
3. Ejecutar pruebas: `pytest tests/ -v`
4. Hacer commit con formato convencional
5. Push y crear Pull Request a `develop`
6. Revisión de código
7. Merge a `develop`, luego a `main`

## 13. Archivos de Configuración

### 13.1 .editorconfig
- Charset: utf-8
- Indent: spaces (4 espacios para Python)
- Final newline: sí
- Trim trailing whitespace: sí

### 13.2 pyproject.toml
Configuración moderna para build y herramientas.

### 13.3 tox.ini
Pruebas en múltiples entornos Python.

---

**Versión del documento**: 1.4.3
**Fecha de actualización**: 2026-05-06
**Responsable**: @FARLEY-PIEDRAHITA-OROZCO
**Estado**: ✅ Completo y actualizado con estándares actuales
