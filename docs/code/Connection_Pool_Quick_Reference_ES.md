# ⚡ Referencia Rápida: Engine y Pool de Conexiones

## 🎯 La Respuesta Directa

### ¿Dónde debe crearse el Engine?

```
✅ EN EL LIFESPAN
❌ NO EN EL DEPENDENCY
```

### ¿Por qué?

| Engine en Lifespan (✅) | Engine en Dependency (❌) |
|-------------------------|---------------------------|
| Se crea 1 vez | Se crea en cada request |
| Rápido (1ms por request) | Lento (50-200ms por request) |
| Pool compartido | Pool no funciona bien |
| Eficiente en memoria | Desperdicia memoria |
| 👍 Recomendado | 👎 Anti-patrón |

---

## 📊 Diagrama Visual

```
┌─────────────────────────────────────────────┐
│         CICLO DE VIDA COMPLETO              │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  STARTUP (1 vez)                            │
│  ┌─────────────────────┐                    │
│  │ Lifespan ejecuta    │                    │
│  │ ↓                   │                    │
│  │ Crear Engine        │ ← 50-200ms         │
│  │ ↓                   │                    │
│  │ Configurar Pool     │                    │
│  │ ↓                   │                    │
│  │ Guardar globalmente │                    │
│  └─────────────────────┘                    │
└─────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│  RUNTIME (cada request)                     │
│  ┌─────────────────────┐                    │
│  │ Dependency ejecuta  │                    │
│  │ ↓                   │                    │
│  │ get_adapter()       │ ← < 1ms ⚡         │
│  │ ↓                   │                    │
│  │ get_session()       │                    │
│  │ ↓                   │                    │
│  │ Ejecutar queries    │                    │
│  │ ↓                   │                    │
│  │ Cerrar session      │                    │
│  │ ↓                   │                    │
│  │ Conexión → Pool     │                    │
│  └─────────────────────┘                    │
└─────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│  SHUTDOWN (1 vez)                           │
│  ┌─────────────────────┐                    │
│  │ Lifespan ejecuta    │                    │
│  │ ↓                   │                    │
│  │ engine.dispose()    │                    │
│  │ ↓                   │                    │
│  │ Cerrar conexiones   │                    │
│  │ ↓                   │                    │
│  │ Liberar recursos    │                    │
│  └─────────────────────┘                    │
└─────────────────────────────────────────────┘
```

---

## 🔌 Pool de Conexiones

### ¿Qué es?

Un caché de conexiones reutilizables a la base de datos.

```
┌──────────────────────────────────┐
│      POOL DE CONEXIONES          │
├──────────────────────────────────┤
│                                  │
│  Permanentes (pool_size=5):      │
│  [C1] [C2] [C3] [C4] [C5]        │
│                                  │
│  Temporales (max_overflow=10):   │
│  [T1] [T2] [T3] ... [T10]        │
│                                  │
│  Total: 15 conexiones            │
│                                  │
└──────────────────────────────────┘
```

### Parámetros Clave

```python
engine = create_async_engine(
    url,
    pool_pre_ping=True,    # Verifica conexión antes de usar
    pool_size=5,           # 5 conexiones permanentes
    max_overflow=10,       # 10 conexiones adicionales
    pool_recycle=3600,     # Recicla cada 1 hora
)
```

---

## ✅ Tu Código (Correcto)

### 1. Lifespan (app/core/lifespan.py)

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    global _async_adapter
    
    # STARTUP: Crear adapter con engine
    _async_adapter = create_async_sqlite_adapter(...)
    
    yield  # App corre
    
    # SHUTDOWN: Limpiar
    await _async_adapter.engine.dispose()
```

### 2. Adapter (app/clients/sql/adapters/.../asynchronous.py)

```python
class AsyncSQLiteAdapter:
    def __init__(self, database_url: str, echo: bool = False):
        # Engine creado 1 vez
        self.engine = create_async_engine(database_url, echo=echo)
        self.async_session = async_sessionmaker(self.engine, ...)
    
    @asynccontextmanager
    async def get_session(self):
        async with self.async_session() as session:
            yield session
```

### 3. Dependency (app/shared/dependencies/sql.py)

```python
async def get_async_session_dependency():
    # Obtiene adapter del lifespan
    adapter = get_async_adapter()
    
    # Crea session por request
    async with adapter.get_session() as session:
        yield session
```

### 4. Endpoint (app/domains/.../routes/.../py)

```python
@router.get("/items")
async def get_items(
    session: AsyncSession = Depends(get_async_session_dependency)
):
    return await session.exec(select(Item))
```

---

## 🚫 Anti-Patrones

### ❌ NO HACER: Engine en Dependency

```python
# MALO ❌
async def get_session():
    engine = create_async_engine(...)  # ¡Crea engine cada vez!
    async with AsyncSession(engine) as session:
        yield session
    await engine.dispose()

# Problemas:
# - Muy lento (50-200ms por request)
# - Pool no funciona
# - Desperdicia recursos
```

### ❌ NO HACER: Engine Global sin Lifespan

```python
# MALO ❌
engine = create_async_engine(...)  # Global fuera de lifespan

# Problemas:
# - Se crea al importar
# - No hay control de cuándo
# - No hay cleanup
```

---

## 📈 Configuración por Entorno

### SQLite (Desarrollo)

```python
engine = create_async_engine(
    "sqlite+aiosqlite:///./local.db",
    echo=True,  # Ver queries
    connect_args={"check_same_thread": False}
)
# No necesita configuración de pool
```

### PostgreSQL (Producción)

```python
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@host/db",
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
)
# Pool completamente configurado
```

---

## 🎯 Checklist de Verificación

```bash
✅ Engine creado en lifespan.py
✅ Adapter guardado globalmente
✅ get_async_adapter() retorna adapter compartido
✅ Dependency usa get_async_adapter()
✅ Session creada por request
✅ Context managers (@asynccontextmanager)
✅ engine.dispose() en shutdown
✅ pool_pre_ping=True para PostgreSQL
✅ pool_size configurado
✅ pool_recycle configurado
```

---

## 🔍 Troubleshooting Rápido

### "Too Many Connections"

```python
# Solución: Aumentar pool
pool_size=10        # De 5 a 10
max_overflow=20     # De 10 a 20
```

### "Connection Timeout"

```python
# Solución: Aumentar timeout o pool
pool_timeout=30     # Espera más tiempo
pool_size=10        # Más conexiones
```

### "SSL Connection Closed"

```python
# Solución: pool_recycle y pool_pre_ping
pool_pre_ping=True   # Verifica antes de usar
pool_recycle=3600    # Recicla cada hora
```

---

## 📚 Más Información

- **Guía Completa:** `Connection_Pool_Guide_ES.md`
- **Best Practices:** `Database_Best_Practices.md`
- **Lifespan:** `Lifespan_Explained_ES.md`
- **Flujo Visual:** `Flujo_Visual_ES.md`

---

## 💡 Resumen en 3 Puntos

1. **Engine en Lifespan** (no en Dependency)
2. **Pool configurado** (pre_ping, size, overflow, recycle)
3. **Sessions por request** (via Dependency)

**Tu implementación ya es correcta ✅**

Solo añadimos `pool_recycle=3600` a PostgreSQL adapters.

¡No necesitas más cambios! 🎉


