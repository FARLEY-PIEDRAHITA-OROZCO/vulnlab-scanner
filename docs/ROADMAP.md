# Roadmap - VulnLab Scanner

## Estado Actual (Fase 3: Desarrollo - 80%)

### Completado ✅
- Arquitectura modular implementada
- Configuración centralizada con `.env`
- Cliente HTTP con rate limiting
- Gestión de sesiones con login automático
- Clase base `BaseScanner` para todos los escáneres
- Payloads centralizados en `utils/payloads.py`
- Escáner XSS (refactorizado)
- Escáner SQLi (implementado con error-based y boolean-based)
- Escáner de Headers (refactorizado)
- Aviso legal y validación de permisos
- Generación de reportes JSON y HTML
- CLI actualizado con nuevos flags
- Pruebas unitarias iniciales

## Próximas Fases

### Fase 4: Pruebas y Validación (2 semanas)

#### 4.1 Pruebas Unitarias (Completar cobertura)
- [ ] Pruebas para `scanner/xss.py`
- [ ] Pruebas para `scanner/sqli.py`
- [ ] Pruebas para `scanner/headers.py`
- [ ] Pruebas para `core/session.py`
- [ ] Pruebas para `utils/reporter.py`
- [ ] Pruebas para `cli.py`

#### 4.2 Pruebas de Integración
- [ ] Probar con OWASP Juice Shop
- [ ] Probar con DVWA (Damn Vulnerable Web Application)
- [ ] Validar detección de vulnerabilidades reales
- [ ] Verificar falsos positivos/negativos

#### 4.3 Pruebas de Usabilidad
- [ ] Probar instalación desde cero
- [ ] Validar mensajes de error claros
- [ ] Verificar reportes HTML legibles

### Fase 5: Documentación de Usuario (1 semana)

#### 5.1 Documentación Existente ✅
- [x] `DOCS/REQUISITOS.md`
- [x] `DOCS/ALCANCE.md`
- [x] `DOCS/ARQUITECTURA.md`
- [x] `DOCS/ESTANDARES_CODIGO.md`
- [x] `DOCS/INTERFACES.md`
- [x] `DOCS/PROGRESO.md`
- [x] `DOCS/GUIA_USUARIO.md`

#### 5.2 Pendiente
- [ ] Actualizar `README.md` con instalación y uso
- [ ] Agregar ejemplos de salida en documentación
- [ ] Crear `CHANGELOG.md`
- [ ] Crear `CONTRIBUTING.md` (si es open source)

### Fase 6: Mantenimiento y Mejoras (Continuo)

#### 6.1 Mejoras Corto Plazo (1-2 meses)
- [ ] Soporte para inyección en formularios POST
- [ ] Mejorar detección de XSS Stored y DOM-based
- [ ] Agregar más payloads y verificaciones
- [ ] Implementar escáner de Broken Access Control
- [ ] Implementar escáner de Authentication Failures
- [ ] Soporte para configuración vía archivo YAML/JSON

#### 6.2 Mejoras Medio Plazo (3-6 meses)
- [ ] Escáner de Vulnerable Components (SCA)
- [ ] Detección de CSRF
- [ ] Detección de SSRF
- [ ] Detección de XXE
- [ ] Modo interactivo (opcional)
- [ ] Integración con CI/CD (GitHub Actions, GitLab CI)
- [ ] Dashboard web básico (opcional)

#### 6.3 Mejoras Largo Plazo (6+ meses)
- [ ] Escaneo distribuido/múltiples targets
- [ ] API REST para integración
- [ ] Base de datos para histórico de escaneos
- [ ] Comparación de escaneos (diferencial)
- [ ] Plugins de terceros

## Métricas de Éxito

### Técnicas
- Cobertura de pruebas > 80%
- Detección exitosa en OWASP Juice Shop > 90%
- Falsos positivos < 5%
- Tiempo de escaneo razonable (< 5 min para escaneo completo básico)

### Usabilidad
- Instalación en menos de 3 comandos
- Documentación completa en español
- Mensajes de error claros y accionables

## Contribuciones

Si este proyecto se vuelve open source, se busca:
- Código documentado
- Pruebas unitarias para nuevas funcionalidades
- Respeto por estándares de código (PEP8)
- Mensajes de commit descriptivos en español

---

**Última actualización**: 2026-05-05
**Próxima revisión**: Al completar Fase 4
