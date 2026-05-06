# Contributing to VulnLab Scanner

¡Gracias por tu interés en contribuir a VulnLab Scanner! 🎉

## Cómo Contribuir

### 1. Reportar Bugs
- Usa la pestaña "Issues" en GitHub
- Incluye: pasos para reproducir, comportamiento esperado vs actual, versión de Python
- Etiqueta como `bug`

### 2. Sugerir Mejoras
- Crea un "Issue" con etiqueta `enhancement`
- Describe el caso de uso y beneficio

### 3. Enviar Código (Pull Requests)
1. Forkea el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Haz tus cambios siguiendo los estándares (ver abajo)
4. Añade pruebas en `tests/`
5. Asegura que `pytest tests/ -v` pasen (100%)
6. Haz commit: `git commit -m "feat(ámbito): descripción corta"`
7. Haz push: `git push origin feature/nueva-funcionalidad`
8. Crea un Pull Request a `develop`

## Estándares de Código
- **PEP 8**: Usa un linter (flake8)
- **Docstrings**: En español, formato Google style
- **Commits**: Formato `<tipo>(<ámbito>): <descripción corta en español>`
  - Tipos: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`
- **Pruebas**: 1 commit por archivo de pruebas, 100% pasando

## Configuración de Entorno de Desarrollo
```bash
git clone https://github.com/tu-usuario/vulnlab-scanner.git
cd vulnlab-scanner
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
pip install -e ".[dev]"
```

## Pruebas
```bash
# Ejecutar todas las pruebas
pytest tests/ -v

# Con cobertura
pytest --cov=app tests/
```

## Contacto
- Issues: https://github.com/FARLEY-PIEDRAHITA-OROZCO/vulnlab-scanner/issues
- Email: contact@vulnlab.com
