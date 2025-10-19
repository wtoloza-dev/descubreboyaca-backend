# Shared Models

Este módulo contiene modelos base de SQLModel que proporcionan funcionalidad común para todos los modelos de dominio.

## Modelos Base

### `ULIDMixin`

Agrega un campo de clave primaria basado en ULID (Universally Unique Lexicographically Sortable Identifier):

- `id`: ULID de 26 caracteres, generado automáticamente

**Ventajas de ULID sobre UUID:**
- Ordenable lexicográficamente (respeta el orden temporal)
- Más corto en representación string (26 chars vs 36)
- Compatible con índices de base de datos
- Mejor rendimiento en queries

**Uso:**

```python
from sqlmodel import Field, SQLModel
from app.shared.models import ULIDMixin

class MyModel(ULIDMixin, SQLModel, table=True):
    __tablename__ = "my_table"
    
    name: str
    # El campo 'id' (ULID) se hereda automáticamente
```

### `TimestampMixin`

Agrega campos de timestamp automáticos a tu modelo:

- `created_at`: Timestamp de creación (UTC)
- `updated_at`: Timestamp de última actualización (UTC)

**Uso:**

```python
from sqlmodel import Field, SQLModel
from app.shared.models import TimestampMixin

class MyModel(TimestampMixin, SQLModel, table=True):
    __tablename__ = "my_table"
    
    id: int | None = Field(default=None, primary_key=True)
    name: str
```

### `AuditMixin`

Hereda de `ULIDMixin` y `TimestampMixin` y agrega campos de auditoría completa:

- `id`: ULID primary key (heredado de ULIDMixin)
- `created_at`: Timestamp de creación (UTC, heredado de TimestampMixin)
- `updated_at`: Timestamp de última actualización (UTC, heredado de TimestampMixin)
- `created_by`: ULID del usuario que creó el registro
- `updated_by`: ULID del usuario que actualizó el registro por última vez

**Uso:**

```python
from sqlmodel import Field, SQLModel
from app.shared.models import AuditMixin

class Restaurant(AuditMixin, SQLModel, table=True):
    __tablename__ = "restaurants"
    
    # El campo 'id' (ULID) se hereda automáticamente, no es necesario declararlo
    name: str = Field(max_length=255)
    address: str
    is_active: bool = Field(default=True)
    # También hereda: created_at, updated_at, created_by, updated_by
```

## Orden de Herencia

**Importante:** El orden de herencia múltiple en SQLModel es crucial. Siempre usa:

```python
class MyModel(AuditMixin, SQLModel, table=True):
    # ✅ Correcto: AuditMixin primero, luego SQLModel
```

**NO uses:**

```python
class MyModel(SQLModel, AuditMixin, table=True):
    # ❌ Incorrecto: puede causar problemas con la resolución de métodos
```

## Actualización de Timestamps

Los timestamps se actualizan automáticamente:

- `created_at`: Se establece automáticamente al crear el registro
- `updated_at`: Se actualiza automáticamente en cada modificación del registro

## Actualización de Campos de Usuario

Los campos `created_by` y `updated_by` deben actualizarse manualmente en tu lógica de negocio con ULIDs de usuario:

```python
# En tu service o repository
def create_restaurant(restaurant: Restaurant, user_ulid: str):
    # user_ulid debe ser un ULID válido del usuario autenticado
    restaurant.created_by = user_ulid
    restaurant.updated_by = user_ulid
    # ... guardar en DB

def update_restaurant(restaurant: Restaurant, user_ulid: str):
    restaurant.updated_by = user_ulid
    # ... actualizar en DB
```

### Generación manual de ULIDs

Si necesitas generar ULIDs manualmente:

```python
from ulid import ULID

# Generar un nuevo ULID
new_id = str(ULID())  # Ejemplo: "01ARZ3NDEKTSV4RRFFQ69G5FAV"

# Parsear un ULID existente
existing_ulid = ULID.from_str("01ARZ3NDEKTSV4RRFFQ69G5FAV")

# Obtener timestamp de un ULID
timestamp = existing_ulid.timestamp()
```

## Arquitectura

Esta estructura sigue principios de Clean Architecture:

```
app/
├── shared/          # Código compartido entre dominios
│   └── models/      # Modelos base (AuditMixin, TimestampMixin)
├── domains/         # Lógica de dominio específica
│   └── restaurants/
│       └── models/  # Modelos específicos del dominio (hereda de shared)
└── core/           # Configuración y bootstrapping
```

**Reglas de dependencia:**
- `domains/` puede depender de `shared/`
- `shared/` NO debe depender de `domains/`
- Todos pueden depender de `core/settings`

