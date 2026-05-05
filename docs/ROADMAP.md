# Roadmap - VulnLab Scanner

## Estado Actual (Fase 3: Completada ✅)

### Completado ✅
- Arquitectura modular implementada con `BaseScanner`
- Configuración centralizada con `.env`
- Cliente HTTP con rate limiting y reintentos
- Gestión de sesiones con login automático
- Clase base `BaseScanner` para todos los escáneres
- Payloads centralizados en `utils/payloads.py`
- Escáner XSS (refactorizado, soporta reflected)
- Escáner SQLi (implementado con error-based y boolean-based)
- Escáner de Headers (refactorizado)
- Aviso legal y validación de permisos
- Generación de reportes JSON y HTML
- CLI actualizado con nuevos flags
- Pruebas unitarias (43 pruebas, 100% pasando)
- Documentación completa en español

## Plan de Desarrollo por Fases

### Fase 4: Nuevos Escáneres OWASP (Semanas 2-5)

#### 4.1 Escáner A01 - Broken Access Control ⭐ **Prioridad Alta**
**Objetivo**: Detectar falos de control de acceso (IDOR, escalación de privilegios)

| Tarea | Descripción | Estimación |
|------|----------------|------------|
| 4.1.1 | Crear `app/scanner/access_control.py` heredando de `BaseScanner` | 2 días |
| 4.1.2 | Implementar detección IDOR (cambio de IDs en URL) | 3 días |
| 4.1.3 | Implementar detección escalación privilegios | 3 días |
| 4.1.4 | Añadir payloads en `utils/payloads.py` | 1 día |
| 4.1.5 | Crear `tests/test_access_control.py` (8 pruebas) | 2 días |
| 4.1.6 | Actualizar documentación (`DOCS/ALCANCE.md`, `DOCS/ARQUITECTURA.md`) | 1 día |

**Total**: 12 días (2.5 semanas)

#### 4.2 Escáner A07 - Auth Failures ⭐ **Prioridad Alta**
**Objetivo**: Detectar fallos de autenticación y sesiones

| Tarea | Descripción | Estimación |
|------|----------------|------------|
| 4.2.1 | Crear `app/scanner/auth.py` | 2 días |
| 4.2.2 | Implementar detección fuerza bruta suave | 3 días |
| 4.2.3 | Implementar detección sesiones débiles | 2 días |
| 4.2.4 | Añadir payloads en `utils/payloads.py` | 1 día |
| 4.2.5 | Crear `tests/test_auth.py` (6 pruebas) | 2 días |
| 4.2.6 | Documentar A07 en `DOCS/` | 1 día |

**Total**: 11 días (2 semanas)

#### 4.3 Escáner A06 - Vulnerable Components ⭐ **Prioridad Alta**
**Objetivo**: Detectar componentes vulnerables (SCA básico)

| Tarea | Descripción | Estimación |
|------|----------------|------------|
| 4.3.1 | Crear `app/scanner/components.py` | 2 días |
| 4.3.2 | Implementar detección tecnologías (JS, CDN) | 3 días |
| 4.3.3 | Crear `tests/test_components.py` (5 pruebas) | 2 días |

**Total**: 7 días (1.5 semanas)

#### 4.4 Mejorar Escáneres Existentes
**XSS Scanner**: Añadir Stored XSS (vía POST), DOM XSS  
**SQLi Scanner**: Añadir Time-based Blind SQLi, soporte múltiples DB  
**Headers Scanner**: Validar valores específicos (CSP, HSTS, CORS)

**Total Fase 4**: ~6 semanas

---

### Fase 5: Mejoras Técnicas y Usabilidad (Semanas 6-9)

#### 5.1 Barras de Progreso y Multithreading
- [ ] Añadir `tqdm` para barras de progreso visual
- [ ] Implementar `concurrent.futures` para escaneo paralelo
- [ ] Tiempo estimado: 1 semana

#### 5.2 Mejorar Reportes
- [ ] Gráficos con Chart.js en HTML
- [ ] Exportación a PDF
- [ ] Comparación entre escaneos (diferencial)
- [ ] Tiempo estimado: 1.5 semanas

#### 5.3 Interfaz Web Básica (Opcional)
- [ ] API REST con FastAPI
- [ ] Interfaz web mínima con Flask
- [ ] Tiempo estimado: 2 semanas

#### 5.4 Funcionalidades Avanzadas (Opcional)
- [ ] Soporte para proxies (Burp, ZAP)
- [ ] Fuzzing de directorios/archivos
- [ ] Detección de tecnologías (Wappalyzer básico)
- [ ] Tiempo estimado: 2 semanas

**Total Fase 5**: ~4-6 semanas

---

### Fase 6: Empaquetado y Distribución (Semana 10)

#### 6.1 Publicar en PyPI
- [ ] Crear `setup.py` y `pyproject.toml`
- [ ] Configurar `entry_points` para CLI
- [ ] Publicar versión 1.0.0
- [ ] Tiempo estimado: 3 días

#### 6.2 CI/CD con GitHub Actions
- [ ] Crear workflow para pruebas automáticas
- [ ] Crear workflow para publicación automática a PyPI
- [ ] Tiempo estimado: 2 días

#### 6.3 Documentación Final
- [ ] Crear `CONTRIBUTING.md`
- [ ] Crear `CHANGELOG.md` (historial completo)
- [ ] Mejorar `README.md` con badges (pypi, tests, license)
- [ ] Tiempo estimado: 2 días

**Total Fase 6**: 1 semana

---

## Métricas de Éxito

### Técnicas
- ✅ Cobertura de pruebas > 80%
- [ ] Cobertura OWASP: 6/10 → 9/10
- [ ] Detección exitosa en OWASP Juice Shop > 90%
- [ ] Falsos positivos < 5%
- [ ] Tiempo de escaneo razonable (< 5 min para escaneo completo)

### Usabilidad
- ✅ Instalación en menos de 3 comandos
- [ ] `pip install vulnlab-scanner` disponible
- [ ] Documentación completa en español
- [ ] Mensajes de error claros y accionables
- [ ] Barras de progreso visual

### Profesional
- [ ] Publicado en PyPI
- [ ] GitHub Stars > 50 (primer mes)
- [ ] Integración con CI/CD
- [ ] Comunidad inicial activa

---

## Cronograma de Entregables (Gantt)

```
Semana   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
----------|---|---|---|---|---|---|---|---|---|----|
Fase 3   |███|   |   |   |   |   |   |   |   |    |
Fase 4A  |   |███|███|   |   |   |   |   |   |    |
Fase 4B  |   |   |   |███|███|   |   |   |   |    |
Fase 4C  |   |   |   |   |███|   |   |   |   |    |
Fase 4D  |   |   |   |   |   |███|███|   |   |    |
Fase 5    |   |   |   |   |   |   |   |███|███|    |
Fase 6    |   |   |   |   |   |   |   |   |   |███|
```

---

## Siguiente Paso Inmediato

**Hito**: Implementar **A01 - Broken Access Control** (Fase 4.1)

Tareas:
1. Crear rama `feature/add-access-control` desde `develop`
2. Implementar `app/scanner/access_control.py`
3. Añadir payloads en `app/utils/payloads.py`
4. Crear `tests/test_access_control.py`
5. Actualizar documentación
6. Merge a `develop` y luego a `main`

**Tiempo estimado**: 2.5 semanas  
**Calificación esperada después de Fase 4**: 6/10 (Profesional básico)

---

**Última actualización**: 2026-05-05  
**Próxima revisión**: Al completar Fase 4.1 (A01)
