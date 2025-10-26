# Alembic Database Migrations

Este directorio contiene las migraciones de base de datos para el proyecto Descubre Boyacá Backend, gestionadas con [Alembic](https://alembic.sqlalchemy.org/).

## 📁 Estructura

```
alembic/
├── env.py              # Configuración del entorno de Alembic
├── script.py.mako      # Template para nuevas migraciones
├── README.md           # Este archivo
└── versions/           # Migraciones versionadas
    ├── 20251021_0918_d91d67323aac_create_archive_table.py
    └── 20251021_0918_d6e1a4f9747b_create_restaurants_table.py
```

## 🚀 Comandos Principales

### Ver estado actual
```bash
# Ver migraciones aplicadas
alembic current

# Ver historial de migraciones
alembic history --verbose

# Ver migraciones pendientes
alembic heads
```

### Aplicar migraciones

```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head

# Aplicar hasta una migración específica
alembic upgrade d6e1a4f9747b

# Aplicar la siguiente migración
alembic upgrade +1
```

### Revertir migraciones

```bash
# Revertir la última migración
alembic downgrade -1

# Revertir hasta una migración específica
alembic downgrade d91d67323aac

# Revertir todas las migraciones
alembic downgrade base
```

### Crear nuevas migraciones

```bash
# Auto-generar migración detectando cambios en los modelos
alembic revision --autogenerate -m "add column to restaurants"

# Crear migración vacía (manual)
alembic revision -m "add custom index"
```

### Generar SQL (para enviar al DBA)

```bash
# Generar SQL sin ejecutarlo
alembic upgrade head --sql > migration.sql

# SQL de una migración específica
alembic upgrade d91d67323aac:d6e1a4f9747b --sql > add_restaurants.sql
```

## 📝 Flujo de Trabajo Recomendado

### Desarrollo Local

1. **Hacer cambios en los modelos** (`app/*/models/*.py`)

2. **Crear migración**:
   ```bash
   alembic revision --autogenerate -m "descripción del cambio"
   ```

3. **Revisar la migración generada** en `alembic/versions/`
   - ⚠️ Alembic puede no detectar todos los cambios
   - Revisa manualmente el código generado
   - Ajusta si es necesario

4. **Aplicar migración**:
   ```bash
   alembic upgrade head
   ```

5. **Probar rollback**:
   ```bash
   alembic downgrade -1
   alembic upgrade head
   ```

### Staging/Producción

#### Opción 1: Ejecución Directa (Recomendado si tienes acceso)
```bash
# En el servidor o contenedor
alembic upgrade head
```

#### Opción 2: SQL para DBA
```bash
# Generar SQL localmente
alembic upgrade head --sql > migration_v1.2.0.sql

# Enviar archivo al DBA
# El DBA ejecuta manualmente en la base de datos
```

## 🔍 Migraciones Actuales

### 1. `d91d67323aac` - Create archive table
**Fecha**: 2025-10-21 09:18

Crea la tabla `archive` para almacenar registros eliminados de cualquier entidad.

**Campos**:
- `id` (ULID): Identificador único
- `original_table`: Tabla de origen
- `original_id`: ID del registro original
- `data` (JSON): Datos completos del registro
- `deleted_at`: Timestamp de eliminación
- `deleted_by`: Usuario que eliminó
- `note`: Nota opcional

**Índices**:
- `ix_archive_original_table`
- `ix_archive_original_id`
- `ix_archive_deleted_at`

### 2. `d6e1a4f9747b` - Create restaurants table
**Fecha**: 2025-10-21 09:18  
**Depende de**: `d91d67323aac`

Crea la tabla `restaurants` con información completa de restaurantes.

**Campos principales**:
- Audit: `id`, `created_at`, `updated_at`, `created_by`, `updated_by`
- Básicos: `name`, `description`
- Dirección: `address`, `city`, `state`, `postal_code`, `country`
- Contacto: `phone`, `email`, `website`
- JSON: `location`, `social_media`, `cuisine_types`, `features`
- Negocio: `price_level` (1-4)

**Índices**:
- `ix_restaurants_name`
- `ix_restaurants_city`

**Constraints**:
- `price_level` entre 1 y 4

## 🛠️ Troubleshooting

### Error: "Can't locate revision identified by 'xxxx'"
```bash
# Eliminar la base de datos y recrear
rm test.db
alembic upgrade head
```

### Error: "Target database is not up to date"
```bash
# Ver estado
alembic current

# Aplicar migraciones pendientes
alembic upgrade head
```

### Conflicto de versiones
```bash
# Ver ramas
alembic branches

# Merge manual - editar el archivo de migración
# Cambiar down_revision para resolver el conflicto
```

## 📚 Recursos

- [Documentación de Alembic](https://alembic.sqlalchemy.org/)
- [Auto-generating Migrations](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
- [Cookbook de Alembic](https://alembic.sqlalchemy.org/en/latest/cookbook.html)

## ⚙️ Configuración por Entorno

El archivo `env.py` detecta automáticamente el entorno basándose en `settings.SCOPE`:

- **`local`**: SQLite (`sqlite:///./test.db`)
- **`staging`**: PostgreSQL (staging)
- **`prod`**: PostgreSQL (producción)

Para cambiar el entorno:
```bash
export SCOPE=staging
alembic upgrade head
```

