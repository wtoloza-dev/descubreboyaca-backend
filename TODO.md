# TODO - Descubre Boyacá Backend

Lista de mejoras prioritarias para el proyecto.

**Última actualización**: 26 de Octubre, 2025  
**Coverage actual**: 76% (Meta: 85%+)  
**Tests**: 332 tests pasando

---

## 🔴 PRIORIDAD ALTA (Crítico)

### 1. 📝 Crear `.env.example` y documentar configuración
**Problema**: No existe archivo `.env.example` para documentar variables de entorno necesarias.

**Impacto**: Dificulta onboarding de nuevos developers y despliegues.

**Tareas**:
- [ ] Crear `.env.example` en la raíz del proyecto
- [ ] Documentar todas las variables necesarias:
  - `SCOPE` (local/staging/prod)
  - `DEBUG` (True/False)
  - `DATABASE_URL` (actualmente hardcodeado)
  - `JWT_SECRET_KEY`
  - `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET`
  - `CORS_ORIGINS`
- [ ] Agregar comentarios explicativos para cada variable
- [ ] Actualizar README.md con sección de configuración

**Estimación**: 30 minutos

---

### 2. ⚙️ Agregar DATABASE_URL a Settings
**Problema**: La URL de la base de datos está hardcodeada en `shared/dependencies/sql.py` como `"sqlite:///./local.db"`.

**Impacto**: No se puede cambiar fácilmente entre SQLite y PostgreSQL.

**Tareas**:
- [ ] Agregar `DATABASE_URL: str = "sqlite:///./local.db"` a `BaseAppSettings`
- [ ] Actualizar `LocalSettings` con `DATABASE_URL = "sqlite:///./local.db"`
- [ ] Actualizar `StagingSettings` con PostgreSQL URL
- [ ] Actualizar `ProdSettings` con PostgreSQL URL
- [ ] Modificar `shared/dependencies/sql.py` para usar `settings.DATABASE_URL`
- [ ] Agregar validación de formato de URL en settings

**Archivos afectados**:
- `app/core/settings/base.py`
- `app/core/settings/local.py`
- `app/core/settings/staging.py`
- `app/core/settings/prod.py`
- `app/shared/dependencies/sql.py`

**Estimación**: 1 hora

---

### 3. 🔧 Mejorar Health Check con verificación de DB
**Problema**: El health check actual solo retorna `{"status": "healthy"}` sin verificar conectividad real a la base de datos.

**Impacto**: No detecta problemas de DB en producción.

**Tareas**:
- [ ] Crear endpoint `/health` (básico, sin DB check)
- [ ] Crear endpoint `/health/ready` (con verificación de DB)
- [ ] Agregar timestamp, version, python version al response
- [ ] Agregar información de ambiente (SCOPE)
- [ ] Crear schema `HealthResponse` y `DetailedHealthResponse`
- [ ] Documentar endpoints en docstrings

**Archivos afectados**:
- `app/core/routes/health.py`

**Estimación**: 45 minutos

---

### 4. 🧪 Aumentar Coverage de 76% a 85%
**Problema**: Coverage actual es 76%, meta es 85%+.

**Áreas con bajo coverage**:
- `RestaurantOwnerService`: **38%** (crítico)
- `ArchiveService`: **43%**
- `SocialMedia` value object: **59%**
- `GeoLocation` value object: **77%**
- Rutas admin de restaurants: **82%**

**Tareas prioritarias**:
- [ ] Tests para `RestaurantOwnerService` (38% → 85%):
  - [ ] `assign_owner()` - asignar owner a restaurant
  - [ ] `remove_owner()` - remover owner
  - [ ] `transfer_ownership()` - transferir ownership
  - [ ] `get_team_members()` - obtener equipo
  - [ ] Casos edge: owner no existe, restaurant no existe, etc.
- [ ] Tests para `ArchiveService` (43% → 85%):
  - [ ] `archive_entity()` - archivar entidad
  - [ ] `restore_entity()` - restaurar entidad
  - [ ] `get_archived()` - obtener archivados
  - [ ] Casos edge: entidad ya archivada, etc.
- [ ] Tests para value objects:
  - [ ] `SocialMedia`: validaciones de URLs
  - [ ] `GeoLocation`: coordenadas límite, validaciones
- [ ] Tests para endpoints admin:
  - [ ] `transfer_ownership` endpoint
  - [ ] `update_owner_role` endpoint
- [ ] Tests para `list_favorites` (actualmente tiene TODO)
- [ ] Configurar `fail_under = 85` en `pyproject.toml`

**Estimación**: 2-3 días

---

### 5. 🚀 Implementar CI/CD Pipeline
**Problema**: No hay automatización de tests ni linting en GitHub Actions.

**Impacto**: No se valida código antes de merge, riesgo de bugs en producción.

**Tareas**:
- [ ] Crear `.github/workflows/test.yml`:
  - [ ] Job de linting con Ruff
  - [ ] Job de tests con pytest
  - [ ] Job de coverage con pytest-cov
  - [ ] Upload coverage a Codecov
- [ ] Crear `.github/workflows/deploy-staging.yml` (opcional)
- [ ] Configurar branch protection rules:
  - [ ] Require tests pass before merge
  - [ ] Require code review
- [ ] Agregar badges al README:
  - [ ] Build status
  - [ ] Coverage badge
  - [ ] Python version
  - [ ] License

**Estimación**: 2 horas

---

### 6. 🔐 Mejorar Seguridad de CORS
**Problema**: `CORS_ORIGINS` es string `"*"` (permite todos los orígenes). Debería ser lista configurable.

**Impacto**: Riesgo de seguridad en producción.

**Tareas**:
- [ ] Cambiar tipo de `CORS_ORIGINS` de `str` a `list[str]`
- [ ] En `LocalSettings`: permitir localhost con diferentes puertos
  ```python
  CORS_ORIGINS: list[str] = [
      "http://localhost:3000",
      "http://localhost:5173",
      "http://localhost:5174",
  ]
  ```
- [ ] En `StagingSettings`: solo dominios de staging
- [ ] En `ProdSettings`: solo dominios de producción verificados
- [ ] Actualizar `app/main.py` para manejar lista (ya lo hace correctamente)
- [ ] Documentar en `.env.example` cómo configurar CORS

**Estimación**: 30 minutos

---

## 🟡 PRIORIDAD MEDIA (Importante)

### 7. 📝 Implementar Logging Estructurado
**Problema**: No hay sistema de logging configurado, solo prints o logs básicos.

**Impacto**: Dificulta debugging en producción.

**Tareas**:
- [ ] Instalar `structlog` o `loguru`
  ```bash
  uv add structlog
  ```
- [ ] Crear módulo `app/core/logging/`:
  - [ ] `config.py` - configuración de loggers
  - [ ] `formatters.py` - JSON para prod, colorizado para local
  - [ ] `middleware.py` - log de requests/responses
- [ ] Configurar niveles por ambiente:
  - Local: DEBUG
  - Staging: INFO
  - Prod: WARNING
- [ ] Agregar logging en capas críticas:
  - [ ] Services: operaciones CRUD
  - [ ] Repositories: queries SQL
  - [ ] Exception handlers: todos los errores
  - [ ] Middleware: timing de requests
- [ ] Agregar settings de logging:
  - `LOG_LEVEL: str = "INFO"`
  - `LOG_FORMAT: str = "json"` o `"console"`

**Estimación**: 2-3 días

---

### 8. 🚦 Implementar Rate Limiting
**Problema**: API vulnerable a abuso y ataques DDoS.

**Impacto**: Servidor puede ser saturado fácilmente.

**Tareas**:
- [ ] Instalar `slowapi`
  ```bash
  uv add slowapi
  ```
- [ ] Configurar rate limiting global:
  - [ ] 60 requests/minuto por IP
  - [ ] 1000 requests/hora por IP
- [ ] Rate limiting por endpoint:
  - [ ] Endpoints públicos: más restrictivo (30/min)
  - [ ] Endpoints autenticados: menos restrictivo (100/min)
  - [ ] Endpoints admin: sin límite
- [ ] Configurar headers de rate limit:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`
- [ ] Respuestas 429 con mensaje claro
- [ ] Agregar settings:
  - `RATE_LIMIT_ENABLED: bool = True`
  - `RATE_LIMIT_PER_MINUTE: int = 60`

**Estimación**: 1-2 días

---

### 9. 📚 Mejorar README con Ejemplos
**Problema**: README muy básico, no tiene ejemplos de uso de la API.

**Impacto**: Dificulta uso de la API para otros developers.

**Tareas**:
- [ ] Agregar sección "Ejemplos de Uso":
  - [ ] Ejemplo de crear restaurant con curl
  - [ ] Ejemplo de obtener restaurant
  - [ ] Ejemplo de listar con paginación
  - [ ] Ejemplo de autenticación (login)
  - [ ] Ejemplo de usar token en requests
- [ ] Agregar sección "Respuestas":
  - [ ] Ejemplo de respuesta exitosa (201 Created)
  - [ ] Ejemplo de error (404 Not Found)
  - [ ] Ejemplo de error de validación (422)
- [ ] Agregar sección "Configuración":
  - [ ] Variables de entorno necesarias
  - [ ] Cómo configurar diferentes bases de datos
  - [ ] Cómo configurar Google OAuth
- [ ] Agregar badges (cuando CI/CD esté configurado):
  - [ ] Build status
  - [ ] Coverage
  - [ ] Python version
  - [ ] License
- [ ] Agregar diagrama de arquitectura (puede ser link a ARCHITECTURE.md)

**Estimación**: 2 horas

---

### 10. 🗄️ Setup de PostgreSQL para Desarrollo
**Problema**: Solo se usa SQLite, no hay forma fácil de probar con PostgreSQL localmente.

**Impacto**: Diferencias entre dev y prod pueden causar bugs.

**Tareas**:
- [ ] Crear `docker-compose.yml`:
  - [ ] Servicio PostgreSQL
  - [ ] Servicio pgAdmin (opcional)
  - [ ] Volumes para persistencia
  - [ ] Health checks
- [ ] Configurar PostgreSQL en settings:
  - [ ] URL de conexión
  - [ ] Pool size
  - [ ] Max overflow
- [ ] Actualizar README con instrucciones:
  - [ ] Cómo iniciar PostgreSQL con Docker
  - [ ] Cómo conectar desde la app
  - [ ] Cómo ejecutar migraciones
- [ ] Agregar comando en Makefile:
  - `make db-postgres-up` - iniciar PostgreSQL
  - `make db-postgres-down` - detener PostgreSQL

**Estimación**: 1-2 horas

---

### 11. ✅ Implementar Endpoint de Favoritos
**Problema**: El endpoint `/api/v1/restaurants/favorites` tiene `TODO: Implement` sin lógica real.

**Ubicación**: `app/domains/restaurants/routes/restaurant/public/list_favorites.py`

**Tareas**:
- [ ] Crear tabla `favorites` en la base de datos:
  - [ ] Migration con Alembic
  - [ ] Modelo `FavoriteModel` en SQLModel
  - [ ] Índices: `user_id`, `restaurant_id`, UNIQUE(user_id, restaurant_id)
- [ ] Crear dominio `favorites`:
  - [ ] Entity: `Favorite`
  - [ ] Repository: `FavoriteRepository`
  - [ ] Service: `FavoriteService`
- [ ] Implementar endpoints:
  - [ ] POST `/api/v1/restaurants/{id}/favorite` - agregar a favoritos
  - [ ] DELETE `/api/v1/restaurants/{id}/favorite` - quitar de favoritos
  - [ ] GET `/api/v1/restaurants/favorites` - listar mis favoritos
- [ ] Completar lógica en `list_favorites.py`
- [ ] Agregar tests E2E completos

**Estimación**: 1 día

---

### 12. 🔄 Reducir Duplicación en Repositorios
**Problema**: Los repositorios sync y async tienen mucho código duplicado.

**Impacto**: Dificulta mantenimiento.

**Tareas**:
- [ ] Crear helpers compartidos en `_helpers.py`:
  - [ ] `prepare_location_for_db()`
  - [ ] `prepare_social_media_for_db()`
  - [ ] `model_to_entity()`
- [ ] O crear clase base `BaseRestaurantRepository` con lógica compartida
- [ ] Aplicar a otros repositorios si tienen duplicación
- [ ] Actualizar tests para verificar que todo sigue funcionando

**Estimación**: 1 día

---

## 🟢 PRIORIDAD BAJA (Nice to Have)

### 13. 📊 Pre-commit Hooks
**Beneficio**: Código siempre formateado y limpio automáticamente.

**Tareas**:
- [ ] Instalar `pre-commit`
  ```bash
  uv add --dev pre-commit
  ```
- [ ] Crear `.pre-commit-config.yaml`:
  - [ ] Ruff linter
  - [ ] Ruff formatter
  - [ ] Trailing whitespace
  - [ ] End of file fixer
  - [ ] Check YAML
  - [ ] Check large files
- [ ] Instalar hooks: `uv run pre-commit install`
- [ ] Probar: `uv run pre-commit run --all-files`

**Estimación**: 30 minutos

---

### 14. 🎨 API Versioning Explícito
**Problema**: Actualmente se usa `/api/v1/` pero no hay estrategia definida para versiones futuras.

**Tareas**:
- [ ] Documentar estrategia de versionado en ARCHITECTURE.md
- [ ] Preparar estructura para v2 (si es necesario en el futuro)
- [ ] Agregar deprecation warnings mechanism
- [ ] Documentar breaking changes policy

**Estimación**: 2 horas

---

### 15. 🔒 Security Hardening
**Tareas**:
- [ ] Agregar security headers middleware:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Strict-Transport-Security` (solo HTTPS en prod)
- [ ] Instalar `pip-audit` para escanear vulnerabilidades:
  ```bash
  uv add --dev pip-audit
  ```
- [ ] Agregar comando en Makefile: `make security-audit`
- [ ] Configurar en CI/CD para ejecutar en cada push
- [ ] Integrar con Snyk o similar (opcional)

**Estimación**: 2-3 horas

---

### 16. 📊 Métricas y Observabilidad
**Tareas**:
- [ ] Implementar endpoint `/metrics` (Prometheus format)
- [ ] Métricas custom:
  - Número de requests por endpoint
  - Tiempo de respuesta
  - Error rate
  - Active users
- [ ] Integrar con Sentry para error tracking:
  ```bash
  uv add sentry-sdk[fastapi]
  ```
- [ ] Configurar Sentry DSN en settings
- [ ] Agregar breadcrumbs en operaciones críticas

**Estimación**: 1-2 días

---

### 17. 🗂️ Backup Automático
**Tareas**:
- [ ] Script de backup para SQLite (`scripts/backup-sqlite.sh`)
- [ ] Script de backup para PostgreSQL (`scripts/backup-postgres.sh`)
- [ ] Configurar cron job en producción
- [ ] Almacenamiento en S3 o cloud storage
- [ ] Retention policy (30 días)
- [ ] Script de restore
- [ ] Documentar proceso en README

**Estimación**: 1 día

---

### 18. 🐳 Dockerfile para Producción
**Tareas**:
- [ ] Crear `Dockerfile` optimizado:
  - [ ] Multi-stage build
  - [ ] Python 3.14 slim
  - [ ] UV para instalación rápida
  - [ ] Non-root user
  - [ ] Health check
- [ ] Crear `.dockerignore`
- [ ] Actualizar README con instrucciones de Docker
- [ ] Crear `docker-compose.prod.yml` para stack completo:
  - [ ] App
  - [ ] PostgreSQL
  - [ ] Redis (si se usa)

**Estimación**: 2-3 horas

---

## 📋 Checklist de Progreso

### Crítico (Hacer Ya)
- [ ] Crear `.env.example`
- [ ] Agregar `DATABASE_URL` a settings
- [ ] Mejorar health check con DB verification
- [ ] Aumentar coverage a 85%
- [ ] Implementar CI/CD pipeline
- [ ] Mejorar seguridad de CORS

### Importante (Próximas 2 Semanas)
- [ ] Logging estructurado
- [ ] Rate limiting
- [ ] Mejorar README
- [ ] Setup PostgreSQL con Docker
- [ ] Implementar endpoint de favoritos
- [ ] Reducir duplicación en repositorios

### Nice to Have (Backlog)
- [ ] Pre-commit hooks
- [ ] API versioning explícito
- [ ] Security hardening
- [ ] Métricas y observabilidad
- [ ] Backup automático
- [ ] Dockerfile para producción

---

## 📊 Métricas de Calidad

### Estado Actual
- ✅ Arquitectura: Excelente (Hexagonal + DDD + Clean)
- ✅ Tests: 332 tests pasando
- 🟡 Coverage: **76%** (meta: 85%+)
- ✅ Linting: Ruff configurado
- ❌ CI/CD: No implementado
- ❌ Logging: No implementado
- ❌ Rate Limiting: No implementado
- 🟡 Documentación: Básica (necesita mejoras)

### Objetivos
- [ ] Coverage >85%
- [ ] CI/CD funcionando
- [ ] Logging estructurado activo
- [ ] Rate limiting configurado
- [ ] README completo con ejemplos
- [ ] PostgreSQL en staging y prod

---

## 🎯 Plan de Acción Recomendado

### Esta Semana (5 días)
1. **Día 1** (2h): `.env.example` + `DATABASE_URL` en settings + CORS fix
2. **Día 2** (3h): Health check mejorado + CI/CD básico
3. **Día 3-5** (2-3 días): Aumentar coverage a 85%

### Próxima Semana (5 días)
1. **Día 1-2** (2 días): Logging estructurado
2. **Día 3** (1 día): Rate limiting
3. **Día 4** (1 día): Mejorar README
4. **Día 5** (1 día): PostgreSQL con Docker

### Semana 3 (5 días)
1. **Día 1** (1 día): Implementar favoritos
2. **Día 2** (1 día): Reducir duplicación
3. **Día 3-4** (2 días): Pre-commit + Security
4. **Día 5** (1 día): Métricas básicas

---

**Total estimado**: 3 semanas para completar tareas críticas e importantes.

**Próximo paso**: Empezar con `.env.example` y `DATABASE_URL` (1-2 horas).

---

**Última revisión**: 26 de Octubre, 2025  
**Mantenedor**: @wtoloza

