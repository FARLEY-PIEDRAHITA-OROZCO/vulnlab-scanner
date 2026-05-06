# Contributing to VulnLab Scanner v1.4.2

¡Gracias por tu interés en contribuir a VulnLab Scanner! 🎉

## Cómo Contribuir

### 1. Reportar Bugs
- Usa la pestaña "Issues" en GitHub
- Incluye: pasos para reproducir, comportamiento esperado vs actual, versión de Python
- Etiqueta como `bug`
- Usa la plantilla `bug_report.md` que configuramos

### 2. Sugerir Mejoras
- Crea un "Issue" con etiqueta `enhancement`
- Describe el caso de uso y beneficio
- Discute la implementación si es compleja

### 3. Enviar Código (Pull Requests)
1. Forkea el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Haz tus cambios siguiendo los estándares (ver abajo)
4. Añade pruebas en `tests/` para tus cambios
5. Asegura que `pytest tests/ -v` pasen (100%)
6. Haz commit: `git commit -m "feat(ámbito): descripción corta"`
7. Haz push: `git push origin feature/nueva-funcionalidad`
8. Crea un Pull Request a `main` usando la plantilla `PULL_REQUEST_TEMPLATE.md`

## Estándares de Código

### Convenciones Generales
- **Lenguaje**: Python 3.8+
- **Estilo**: PEP 8 (con línea máxima de 127 caracteres)
- **Codificación**: UTF-8
- **Docstrings**: En español, formato Google Style
- **Comentarios**: Evitar innecesarios (el código debe ser autodocumentado)

### Nombres
- Clases: `PascalCase` (ej. `BaseScanner`)
- Funciones/métodos: `snake_case` (ej. `get_payloads`)
- Constantes: `UPPER_SNAKE_CASE` (ej. `MAX_RETRIES`)
- Variables: `snake_case` (ej. `target_url`)

### Type Hints
- Usar type hints en todas las funciones y métodos públicos
- Usar `typing` para tipos complejos

### Ejemplo de Clase
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class MiScanner(BaseScanner):
    """Descripción de lo que hace el escáner.
    
    Attributes:
        attr1 (str): Descripción del atributo 1.
    """
    
    def __init__(self, target_url: str, session, dry_run: bool = False):
        """Inicializa el escáner.
        
        Args:
            target_url: URL de la aplicación a escanear.
            session: Sesión HTTP para realizar peticiones.
            dry_run: Si es True, solo simula sin atacar.
        """
        super().__init__(target_url, session, dry_run)
        self.payloads = self.get_payloads()
    
    def scan(self) -> List[Dict[str, Any]]:
        """Ejecuta el escaneo de vulnerabilidades.
        
        Returns:
            Lista de diccionarios con resultados del escaneo.
        """
        # Implementación aquí
        return self.results
    
    def get_payloads(self) -> List[str]:
        """Retorna la lista de payloads para este escáner.
        
        Returns:
            Lista de strings con los payloads.
        """
        return ["payload1", "payload2"]
```

## Configuración de Entorno de Desarrollo

### Instalación para Desarrollo
```bash
# 1. Forkea y clona el repositorio
git clone https://github.com/tu-usuario/vulnlab-scanner.git
cd vulnlab-scanner

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno virtual
# Windows:
.\.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e ".[dev]"

# 5. Instalar pre-commit hooks
pre-commit install
```

### Herramientas Configuradas
- **flake8**: Linting (max-line-length=127)
- **black**: Formateo automático de código
- **isort**: Ordenamiento de imports
- **bandit**: Análisis de seguridad estático
- **pytest**: Framework de pruebas
- **pytest-cov**: Cobertura de código

## Pruebas

### Ejecutar Todas las Pruebas
```bash
# Ejecutar todas las pruebas
pytest tests/ -v

# Con cobertura
pytest --cov=app tests/

# Solo pruebas específicas
pytest tests/test_xss.py -v
```

### Escribir Nuevas Pruebas
1. Crear `tests/test_nombre.py`
2. Heredar de `unittest.TestCase`
3. Usar `unittest.mock` para mocking
4. Seguir convención: `TestNombreClase` y `test_funcionalidad`
5. Ejecutar y verificar que pasen

### Cobertura Mínima
- 100% en módulos nuevos
- Todos los casos de éxito y error
- Mocks para requests externos

## Commits Convencionales

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
refactor(session): mejorar manejo de errores en login
chore(deps): actualizar dependencias en requirements.txt
```

## Git Workflow

### Ramas
- `main`: Producción estable
- `feature/*`: Nuevas características
- `fix/*`: Correcciones

### Flujo
1. Crear rama desde `main`
2. Implementar cambios
3. Ejecutar pruebas: `pytest tests/ -v`
4. Hacer commit con formato convencional
5. Push y crear Pull Request a `main`
6. Revisión de código
7. Merge a `main`

## Revisión de Código (Code Review)

### Criterios de Aceptación
- ✅ Sigue estándares de código (PEP 8)
- ✅ Docstrings en español
- ✅ Type hints presentes
- ✅ Pruebas unitarias añadidas (100% pasando)
- ✅ Sin nuevos warnings de flake8/bandit
- ✅ Commits siguen formato convencional
- ✅ Documentación actualizada si es necesario

## Contacto

- **Issues**: https://github.com/FARLEY-PIEDRAHITA-OROZCO/vulnlab-scanner/issues
- **Email**: contact@vulnlab.com
- **Seguridad**: security@vulnlab.com

## Código de Conducta

Por favor, lee nuestro [Código de Conducta](CODE_OF_CONDUCT.md) antes de contribuir.

---

**Versión del documento**: 1.4.2  
**Fecha de actualización**: 2026-05-06  
**Responsable**: @FARLEY-PIEDRAHITA-OROZCO  
**Estado**: ✅ Completo y actualizado con estándares actuales
