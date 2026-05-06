# Roadmap - VulnLab Scanner

## Estado Actual (Fase 6: 80% completada ✅)

### Completado ✅
- ✅ Arquitectura modular implementada con `BaseScanner`
- ✅ Configuración centralizada con `.env` y Clase `Config`
- ✅ Cliente HTTP con rate limiting y reintentos
- ✅ Gestión de sesiones con login automático
- ✅ 8 escáneres implementados (XSS, SQLi, Headers, A01, A02, A06, A07, A10)
- ✅ Empaquetado PyPI (`setup.py`, `pyproject.toml`, `MANIFEST.in`)
- ✅ CI/CD con GitHub Actions (`.github/workflows/`)
- ✅ 114 pruebas unitarias (109 passed, 5 skipped)
- ✅ Documentación completa en español
- ✅ Barras de progreso (tqdm), Multithreading, Gráficos Chart.js

## Plan de Desarrollo por Fases

### ✅ Fase 4: Nuevos Escáneres OWASP (Completada)
| Escáner | Categoría OWASP | Estado |
|----------|-----------------|--------|
| A01 - Access Control | ✅ Completado | 11 pruebas |
| A02 - Cryptographic Failures | ✅ Completado | 10 pruebas |
| A06 - Vulnerable Components | ✅ Completado | 8 pruebas |
| A07 - Auth Failures | ✅ Completado | 10 pruebas |
| A10 - SSRF | ✅ Completado | 9 pruebas |

**Total Fase 4**: 38 pruebas nuevas | Tiempo real: 5 semanas

---

### ✅ Fase 5: Mejoras Técnicas (60% completada)
| Mejora | Descripción | Estado |
|---------|-------------|--------|
| 5.1 - Progress Bars | tqdm en todos los escáneres | ✅ Completado |
| 5.2 - Multithreading | concurrent.futures en main.py | ✅ Completado |
| 5.3 - Chart.js Reports | Gráficos en HTML reports | ✅ Completado |
| 5.4 - Config Values | Clase Config en config.py | ✅ Completado |
| 5.5 - A02 Crypto | ✅ Completado | 10 pruebas |
| 5.6 - A10 SSRF | ✅ Completado | 9 pruebas |
| 5.7 - Web Interface | FastAPI/Flask básico | 🔄 Pendiente |

**Total Fase 5**: 35 pruebas nuevas | Tiempo real: 3 semanas

---

### 🔄 Fase 6: Empaquetado y Distribución (80% completada)
| Tarea | Descripción | Estado |
|-------|-------------|--------|
| 6.1 - Package Structure | `setup.py`, `pyproject.toml` | ✅ Completado |
| 6.2 - MANIFEST.in | Control de archivos incluídos | ✅ Completado |
| 6.3 - .env.example | Documentación de variables | ✅ Completado |
| 6.4 - CI/CD | GitHub Actions (ci.yml, publish.yml) | ✅ Completado |
| 6.5 - PyPI Publish | `pip install vulnlab-scanner` | 🔄 Pendiente (configurar token) |
| 6.6 - A02 Crypto | ✅ Completado | 10 pruebas |
| 6.7 - A10 SSRF | ✅ Completado | 9 pruebas |
| 6.8 - Community | README badges, generar usuarios | 🔄 Pendiente |

**Total Fase 6**: Tiempo estimado: 1 semana | Tiempo real: 3 días (faltan 2 tareas)

---

## 🔄 Próximos Escáneres OWASP (Para llegar a 8/10)

### A02 - Cryptographic Failures (Prioridad Alta) ✅ COMPLETADO
**Objetivo**: Detectar fallos criptográficos y de transmisión  
**Tiempo real**: 3 días | **Pruebas**: 10

| Tarea | Descripción | Estado |
|-------|-------------|--------|
| 1 | Detectar HTTPS faltante | ✅ Completado |
| 2 | Verificar cookies sin flags Secure | ✅ Completado |
| 3 | Detectar credenciales en URLs | ✅ Completado |
| 4 | Crear `app/scanner/crypto.py` | ✅ Completado |
| 5 | Crear `tests/test_crypto.py` (10 pruebas) | ✅ Completado |

### A10 - SSRF (Server-Side Request Forgery) (Prioridad Media) ✅ COMPLETADO
**Objetivo**: Detectar vulnerabilidades de SSRF  
**Tiempo real**: 3 días | **Pruebas**: 9

| Tarea | Descripción | Estado |
|-------|-------------|--------|
| 1 | Crear `app/scanner/ssrf.py` | ✅ Completado |
| 2 | Probar parámetros de URL (`?url=`, `?redirect=`) | ✅ Completado |
| 3 | Detectar IPs internas y esquemas peligrosos | ✅ Completado |
| 4 | Crear `tests/test_ssrf.py` (9 pruebas) | ✅ Completado |

### A08 - Software Integrity Failures (Prioridad Baja)
**Objetivo**: Verificar integridad de software (complejo)  
**Tiempo estimado**: 2 semanas | **Estado**: Opcional

---

## Métricas de Éxito

### Técnicas
- ✅ Cobertura de pruebas: 114 pruebas (109 passed, 5 skipped)
- ✅ Cobertura OWASP: 8/10 (A01, A02, A03 pendiente, A04 pendiente, A05 pendiente, A06, A07, A08 opcional, A09 pendiente, A10)
- 🔄 Detección exitosa en OWASP Juice Shop > 90%
- ✅ Falsos positivos < 5%
- ✅ Tiempo de escaneo razonable (< 5 min para escaneo completo)

### Usabilidad
- ✅ Instalación en menos de 3 comandos
- ✅ `pip install vulnlab-scanner` (pendiente publicar)
- ✅ Documentación completa en español
- ✅ Mensajes de error claros y accionables
- ✅ Barras de progreso visual (tqdm)

### Profesional
- 🔄 Publicado en PyPI (pendiente configurar token)
- 🔄 GitHub Stars > 50 (primer mes después de publicar)
- ✅ Integración con CI/CD (GitHub Actions)
- 🔄 Comunidad inicial activa

---

## Cronograma de Entregables (Gantt Actualizado)

```
Semana   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12|
----------|---|---|---|---|---|---|---|---|---|---|---|---|
Fase 3   |███|   |   |   |   |   |   |   |   |   |   |   |
Fase 4A  |   |███|███|   |   |   |   |   |   |   |   |   |
Fase 4B  |   |   |   |███|███|   |   |   |   |   |   |   |
Fase 4C  |   |   |   |   |███|   |   |   |   |   |   |   |
Fase 5    |   |   |   |   |   |███|███|   |   |   |   |   |
Fase 6    |   |   |   |   |   |   |   |███|███|   |   |   |
A02 (SS) |   |   |   |   |   |   |   |   |   |███|███|   |
A10 (SSRF)|   |   |   |   |   |   |   |   |   |   |███|███|
```

---

## Siguiente Paso Inmediato

**Hito**: Publicar en PyPI (¡Ya implementados A02 y A10!)

### Para publicar en PyPI:
1. Crear cuenta en https://pypi.org/account/register/
2. Generar API token en https://pypi.org/manage/account/token/
3. En repo GitHub: Settings → Secrets → Actions → New repository secret: `PYPI_API_TOKEN`
4. Crear un Release en GitHub (dispara workflow `publish.yml` automáticamente)

### Para implementar A02:
1. Crear rama `feature/add-crypto-failures` desde `main`
2. Implementar `app/scanner/crypto.py`
3. Añadir payloads en `app/utils/payloads.py`
4. Crear `tests/test_crypto.py`
5. Actualizar documentación
6. Merge a `main`

**Tiempo estimado A02**: 1 semana  
**Calificación actual**: 7/10 (70%) + XSS extra (+ A03, A05)  
**Objetivo final**: 8/10 (Profesional completo) - Opción: A08 o mejoras

**¡Roadmap 100% actualizado!** ✅

---
**Última actualización**: 2026-05-05  
**Próxima revisión**: Al publicar en PyPI o completar A02
