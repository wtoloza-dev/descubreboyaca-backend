# 🔌 Guía Completa: Pool de Conexiones y Gestión SQL

## 📖 Tabla de Contenidos

1. [¿Por qué Lifespan y no Dependency?](#por-qué-lifespan-y-no-dependency)
2. [Pool de Conexiones Explicado](#pool-de-conexiones-explicado)
3. [Arquitectura Actual](#arquitectura-actual)
4. [Configuración del Pool](#configuración-del-pool)
5. [Anti-Patrones](#anti-patrones)
6. [Diagrama de Flujo](#diagrama-de-flujo)
7. [Comparación SQLite vs PostgreSQL](#comparación-sqlite-vs-postgresql)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Por qué Lifespan y no Dependency?

### Respuesta Corta

**El Engine DEBE crearse en el Lifespan**, no en el Dependency.

### Respuesta Larga

```
┌─────────────────────────────────────────────────────────────┐
│               CICLO DE VIDA DE LA APLICACIÓN                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📍 1. STARTUP (Ocurre 1 vez)                                │
│     ┌──────────────────────────────────────────────┐        │
│     │ ✅ Crear Engine                              │        │
│     │ ✅ Configurar Pool de Conexiones             │        │
│     │ ✅ Inicializar Adapter                       │        │
│     └──────────────────────────────────────────────┘        │
│                                                              │
│  📍 2. RUNTIME (Ocurre N veces - millones de requests)       │
│     ┌──────────────────────────────────────────────┐        │
│     │ Request 1 → get_session() → Session 1        │        │
│     │ Request 2 → get_session() → Session 2        │        │
│     │ Request 3 → get_session() → Session 3        │        │
│     │ Request N → get_session() → Session N        │        │
│     └──────────────────────────────────────────────┘        │
│                                                              │
│  📍 3. SHUTDOWN (Ocurre 1 vez)                               │
│     ┌──────────────────────────────────────────────┐        │
│     │ ✅ Cerrar conexiones activas                 │        │
│     │ ✅ Dispose Engine                            │        │
│     │ ✅ Liberar recursos                          │        │
│     └──────────────────────────────────────────────┘        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Razones Técnicas

| Aspecto | Lifespan (✅) | Dependency (❌) |
|---------|---------------|-----------------|
| **Frecuencia** | 1 vez al iniciar | Cada request |
| **Costo** | Bajo (1x) | Alto (Nx) |
| **Pool de Conexiones** | Compartido | No efectivo |
| **Performance** | Óptimo | Lento |
| **Memoria** | Eficiente | Desperdicio |
| **Conexiones DB** | Controladas | Puede saturar |

### Ejemplo Visual

```
❌ MALO: Engine en Dependency
┌──────────┐   ┌──────────┐   ┌──────────┐
│Request 1 │   │Request 2 │   │Request 3 │
└────┬─────┘   └────┬─────┘   └────┬─────┘
     │              │              │
     ↓              ↓              ↓
┌────────┐     ┌────────┐     ┌────────┐
│Engine 1│     │Engine 2│     │Engine 3│  ← ¡Múltiples engines!
└────┬───┘     └────┬───┘     └────┬───┘
     ↓              ↓              ↓
┌────────┐     ┌────────┐     ┌────────┐
│  DB    │     │  DB    │     │  DB    │
└────────┘     └────────┘     └────────┘

Problemas:
- Crear engine es LENTO (50-200ms)
- Multiplica conexiones DB
- Desperdicia memoria
- Pool no funciona correctamente


✅ BUENO: Engine en Lifespan
          ┌──────────────┐
          │ Lifespan     │
          │ Engine (1x)  │ ← ¡Un solo engine!
          │ Pool         │
          └──────┬───────┘
                 │
     ┌───────────┼───────────┐
     ↓           ↓           ↓
┌─────────┐ ┌─────────┐ ┌─────────┐
│Request 1│ │Request 2│ │Request 3│
│Session 1│ │Session 2│ │Session 3│
└────┬────┘ └────┬────┘ └────┬────┘
     └───────────┼───────────┘
                 ↓
            ┌─────────┐
            │   DB    │
            └─────────┘

Beneficios:
- Engine creado 1 vez (rápido)
- Pool compartido (eficiente)
- Sesiones ligeras (óptimo)
- Conexiones controladas
```

---

## 💧 Pool de Conexiones Explicado

### ¿Qué es un Pool de Conexiones?

Un pool de conexiones es como una **piscina de conexiones reutilizables** a la base de datos.

**Analogía del Restaurant:**

```
🍽️ Restaurant sin Pool:
Cliente 1 → Contratar cocinero → Cocinar → Despedir cocinero
Cliente 2 → Contratar cocinero → Cocinar → Despedir cocinero
Cliente 3 → Contratar cocinero → Cocinar → Despedir cocinero
❌ Muy lento y costoso

🍽️ Restaurant con Pool:
Startup: Contratar 5 cocineros permanentes
Cliente 1 → Tomar cocinero del pool → Cocinar → Devolver al pool
Cliente 2 → Tomar cocinero del pool → Cocinar → Devolver al pool
Cliente 3 → Tomar cocinero del pool → Cocinar → Devolver al pool
✅ Rápido y eficiente
```

### Cómo Funciona

```
┌─────────────────────────────────────────────────┐
│         POOL DE CONEXIONES (Engine)              │
├─────────────────────────────────────────────────┤
│                                                  │
│  Conexiones Permanentes (pool_size=5):          │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐            │
│  │ C1 │ │ C2 │ │ C3 │ │ C4 │ │ C5 │            │
│  └────┘ └────┘ └────┘ └────┘ └────┘            │
│                                                  │
│  Conexiones Temporales (max_overflow=10):       │
│  ┌────┐ ┌────┐ ┌────┐      ...                 │
│  │ T1 │ │ T2 │ │ T3 │                           │
│  └────┘ └────┘ └────┘                           │
│                                                  │
└─────────────────────────────────────────────────┘

Flujo de un Request:
1. Request llega
2. Session pide conexión al pool
3. Pool entrega conexión disponible
4. Session usa conexión para queries
5. Session termina
6. Conexión vuelve al pool (NO se cierra)
7. Próximo request puede reutilizarla
```

### Parámetros del Pool

```python
engine = create_async_engine(
    database_url,
    
    # Verifica que la conexión esté viva antes de usarla
    # Evita errores de "connection closed" 
    pool_pre_ping=True,
    
    # Mantiene 5 conexiones siempre abiertas
    # Estas NUNCA se cierran (hasta shutdown)
    pool_size=5,
    
    # Puede crear hasta 10 conexiones adicionales
    # Estas SÍ se cierran después de usarse
    max_overflow=10,
    
    # Recicla conexiones después de 1 hora
    # Evita problemas con timeouts del servidor DB
    pool_recycle=3600,
)
```

#### Explicación de cada parámetro:

| Parámetro | Valor | Qué hace | Por qué es importante |
|-----------|-------|----------|----------------------|
| `pool_pre_ping` | `True` | Hace ping a la DB antes de usar conexión | Evita usar conexiones "muertas" |
| `pool_size` | `5` | Conexiones permanentes | Balance entre rendimiento y recursos |
| `max_overflow` | `10` | Conexiones temporales adicionales | Maneja picos de tráfico |
| `pool_recycle` | `3600` | Recicla cada 1 hora | Evita timeouts del servidor DB |

**Total de conexiones posibles: 15** (5 permanentes + 10 temporales)

### Ejemplo Práctico

```python
# Tienes 100 requests simultáneos:

# Requests 1-5: Usan las 5 conexiones permanentes
# Requests 6-15: Crean 10 conexiones temporales (max_overflow)
# Requests 16-100: ESPERAN a que se libere una conexión

# Cuando request 1 termina:
# - Su conexión vuelve al pool
# - Request 16 puede usarla inmediatamente
```

---

## 🏗️ Arquitectura Actual

### Tu Código (Ya está correcto ✅)

```python
# 1. LIFESPAN - Crea Engine
# app/core/lifespan.py

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    global _sync_adapter, _async_adapter

    # STARTUP: Crear adapters (1 vez)
    _sync_adapter = create_sqlite_adapter(
        database_url=settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
    )
    _async_adapter = create_async_sqlite_adapter(
        database_url=settings.DATABASE_ASYNC_URL,
        echo=settings.DATABASE_ECHO,
    )

    yield  # Aplicación corre

    # SHUTDOWN: Limpiar (1 vez)
    _sync_adapter.engine.dispose()
    await _async_adapter.engine.dispose()
```

```python
# 2. ADAPTER - Contiene Engine
# app/clients/sql/adapters/sqlite/asynchronous.py

class AsyncSQLiteAdapter:
    def __init__(self, database_url: str, echo: bool = False):
        # Engine creado 1 vez
        self.engine: AsyncEngine = create_async_engine(
            database_url,
            echo=echo,
            connect_args={"check_same_thread": False},
        )
        # Session maker configurado 1 vez
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        # Crea session por cada request
        async with self.async_session() as session:
            yield session
```

```python
# 3. DEPENDENCY - Usa Adapter compartido
# app/shared/dependencies/sql.py

async def get_async_session_dependency() -> AsyncGenerator[AsyncSession]:
    # Obtiene adapter del lifespan (compartido)
    adapter = get_async_adapter()
    
    # Crea session por request
    async with adapter.get_session() as session:
        yield session
    # Session se cierra automáticamente
    # Conexión vuelve al pool
```

```python
# 4. ENDPOINT - Recibe Session
# app/domains/restaurants/routes/...py

@router.get("/restaurants")
async def get_restaurants(
    session: AsyncSession = Depends(get_async_session_dependency)
):
    result = await session.exec(select(Restaurant))
    return result.all()
```

### Flujo Completo

```
┌─────────────────────────────────────────────────┐
│  FASE 1: STARTUP (1 vez)                        │
├─────────────────────────────────────────────────┤
│                                                  │
│  1. FastAPI inicia                               │
│  2. lifespan() ejecuta código de startup        │
│  3. create_async_sqlite_adapter() crea adapter  │
│  4. Adapter.__init__() crea Engine + Pool       │
│  5. Adapter guardado en variable global         │
│                                                  │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  FASE 2: RUNTIME (cada request)                 │
├─────────────────────────────────────────────────┤
│                                                  │
│  1. Request llega a endpoint                     │
│  2. FastAPI ejecuta get_async_session_dep()     │
│  3. Obtiene adapter compartido                   │
│  4. adapter.get_session() crea Session          │
│  5. Session pide conexión al Pool               │
│  6. Pool entrega conexión (o crea si necesita)  │
│  7. Session ejecuta queries                      │
│  8. Endpoint retorna respuesta                   │
│  9. Session se cierra                            │
│ 10. Conexión vuelve al Pool                     │
│                                                  │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  FASE 3: SHUTDOWN (1 vez)                       │
├─────────────────────────────────────────────────┤
│                                                  │
│  1. FastAPI recibe señal de shutdown            │
│  2. lifespan() ejecuta código de shutdown       │
│  3. adapter.engine.dispose() cierra pool        │
│  4. Todas las conexiones se cierran             │
│  5. Variables globales se resetean              │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## ⚙️ Configuración del Pool

### SQLite (Desarrollo Local)

```python
# SQLite usa NullPool por defecto
# No necesita configuración especial

engine = create_async_engine(
    "sqlite+aiosqlite:///./local.db",
    echo=False,
    connect_args={"check_same_thread": False}  # SQLite específico
)

# Características:
# - No mantiene pool (cada session crea conexión)
# - Apropiado para desarrollo local
# - No para producción con tráfico alto
```

### PostgreSQL (Staging/Producción)

```python
# PostgreSQL usa QueuePool con configuración

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@host:5432/db",
    echo=False,
    
    # ✅ Verifica conexión antes de usar
    pool_pre_ping=True,
    
    # ✅ 5 conexiones permanentes
    pool_size=5,
    
    # ✅ Hasta 10 conexiones adicionales
    max_overflow=10,
    
    # ✅ Recicla cada 1 hora
    pool_recycle=3600,
)

# Características:
# - Pool activo con 5 conexiones permanentes
# - Puede crecer hasta 15 conexiones totales
# - Ideal para producción
```

### ¿Cómo elegir los valores?

```python
# Para aplicaciones pequeñas (< 100 usuarios concurrentes)
pool_size = 5
max_overflow = 10

# Para aplicaciones medianas (100-1000 usuarios concurrentes)
pool_size = 10
max_overflow = 20

# Para aplicaciones grandes (1000+ usuarios concurrentes)
pool_size = 20
max_overflow = 40

# IMPORTANTE: Tu servidor DB debe soportar estas conexiones
# PostgreSQL por defecto permite 100 conexiones
# Calcula: pool_size + max_overflow < max_connections_db
```

---

## ❌ Anti-Patrones

### 1. Crear Engine en Dependency

```python
# ❌ MALO - NO HACER ESTO
async def get_session():
    # ¡Crea engine NUEVO por cada request!
    engine = create_async_engine("postgresql://...")  # ❌
    async with AsyncSession(engine) as session:
        yield session
    await engine.dispose()  # ❌

# Problemas:
# - Crear engine toma 50-200ms
# - Crear pool toma tiempo
# - Pool no se reutiliza
# - Desperdicia memoria
# - Puede causar "too many connections"
```

### 2. Engine Global sin Lifespan

```python
# ❌ MALO - NO HACER ESTO
# En algún archivo...
engine = create_async_engine("postgresql://...")  # ❌

# Problemas:
# - Se crea al importar el módulo
# - No hay control de cuándo se crea
# - No hay cleanup en shutdown
# - Puede causar errores en tests
# - No sigue patrones de FastAPI
```

### 3. No Usar Context Managers

```python
# ❌ MALO - NO HACER ESTO
async def get_restaurants():
    session = AsyncSession(engine)
    restaurants = await session.exec(select(Restaurant))
    session.close()  # ❌ Manual, puede olvidarse
    return restaurants

# Problemas:
# - Si hay error, session no se cierra
# - Conexión se pierde del pool
# - Eventualmente agotas conexiones
```

### 4. Sesiones de Larga Duración

```python
# ❌ MALO - NO HACER ESTO
session = AsyncSession(engine)  # ❌

async def operation_1():
    await session.exec(...)  # Usa misma session

async def operation_2():
    await session.exec(...)  # Usa misma session

# Problemas:
# - Sesión ocupa conexión mucho tiempo
# - Reduce conexiones disponibles
# - Problemas con transacciones
# - Difícil manejo de errores
```

---

## 📊 Diagrama de Flujo

### Comparación Visual: Malo vs Bueno

```
╔═══════════════════════════════════════════════════╗
║  ❌ ANTI-PATRÓN: Engine en Dependency             ║
╚═══════════════════════════════════════════════════╝

Request 1:
    ↓
┌───────────────┐
│ Dependency    │
│ ejecuta       │
└───────┬───────┘
        ↓
┌───────────────┐  50-200ms 😢
│ create_engine │──────────┐
└───────┬───────┘          │
        ↓                  │ Lento
┌───────────────┐          │
│ Crear Pool    │──────────┘
└───────┬───────┘
        ↓
┌───────────────┐
│ get_session   │
└───────┬───────┘
        ↓
┌───────────────┐
│ Usar session  │
└───────┬───────┘
        ↓
┌───────────────┐
│ dispose()     │
└───────────────┘

Request 2: ¡Repite todo otra vez! 😱


╔═══════════════════════════════════════════════════╗
║  ✅ PATRÓN CORRECTO: Engine en Lifespan           ║
╚═══════════════════════════════════════════════════╝

Startup (1 vez):
    ↓
┌───────────────┐  50-200ms (solo 1 vez) 😊
│ Lifespan      │────────┐
│ ejecuta       │        │
└───────┬───────┘        │
        ↓                │ Una vez
┌───────────────┐        │
│ create_engine │────────┘
└───────┬───────┘
        ↓
┌───────────────┐
│ Crear Pool    │
└───────┬───────┘
        ↓
┌───────────────┐
│ Guardar       │
│ globalmente   │
└───────────────┘

Request 1, 2, 3, ..., N:
    ↓
┌───────────────┐
│ Dependency    │
│ ejecuta       │
└───────┬───────┘
        ↓
┌───────────────┐  < 1ms 🚀
│ get_adapter   │────────┐
│ (compartido)  │        │ Rápido
└───────┬───────┘        │
        ↓                │
┌───────────────┐        │
│ get_session   │────────┘
└───────┬───────┘
        ↓
┌───────────────┐
│ Usar session  │
└───────┬───────┘
        ↓
┌───────────────┐
│ return conn   │
│ to pool       │
└───────────────┘

Todos los requests reutilizan el mismo Engine y Pool! 🎉
```

---

## 🔄 Comparación SQLite vs PostgreSQL

| Aspecto | SQLite | PostgreSQL |
|---------|--------|------------|
| **Pool Type** | NullPool | QueuePool |
| **pool_size** | N/A | 5-20 |
| **max_overflow** | N/A | 10-40 |
| **pool_recycle** | N/A | 3600 |
| **pool_pre_ping** | N/A | True |
| **Concurrencia** | Limitada | Alta |
| **Uso** | Desarrollo | Producción |
| **Conexiones** | 1 por vez | Múltiples |

### Cuándo usar cada uno

```python
# ✅ SQLite - Para desarrollo local
if settings.SCOPE == "local":
    engine = create_async_engine(
        "sqlite+aiosqlite:///./local.db",
        echo=True,  # Ver queries en desarrollo
        connect_args={"check_same_thread": False}
    )

# ✅ PostgreSQL - Para staging/producción
if settings.SCOPE in ["staging", "prod"]:
    engine = create_async_engine(
        "postgresql+asyncpg://user:pass@host/db",
        echo=False,  # No hacer spam en producción
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,
    )
```

---

## 🔧 Troubleshooting

### Problema 1: "Too Many Connections"

```
Error: could not connect to server: 
       too many connections for role "myuser"
```

**Causa:** Todas las conexiones del pool están en uso y no puedes crear más.

**Solución:**

```python
# Opción 1: Aumentar max_overflow
engine = create_async_engine(
    url,
    pool_size=5,
    max_overflow=20,  # Aumentado de 10
)

# Opción 2: Aumentar max_connections en PostgreSQL
# En postgresql.conf:
# max_connections = 200

# Opción 3: Reducir pool_size si tienes múltiples workers
# Si tienes 4 workers con pool_size=10 cada uno:
# Total conexiones = 4 * (10 + 10) = 80
```

### Problema 2: "Connection Timeout"

```
Error: QueuePool limit of size 5 overflow 10 reached,
       connection timed out
```

**Causa:** Todas las conexiones están ocupadas y los requests están esperando.

**Solución:**

```python
# Opción 1: Aumentar timeout
engine = create_async_engine(
    url,
    pool_timeout=30,  # Espera 30 segundos
)

# Opción 2: Aumentar pool
engine = create_async_engine(
    url,
    pool_size=10,  # Más conexiones
    max_overflow=20,
)

# Opción 3: Optimizar queries
# - Usa índices en DB
# - Reduce tiempo de queries
# - Cierra sesiones rápido
```

### Problema 3: "SSL Connection Has Been Closed"

```
Error: SSL connection has been closed unexpectedly
```

**Causa:** Conexión cerrada por timeout en el servidor DB.

**Solución:**

```python
# Añadir pool_recycle y pool_pre_ping
engine = create_async_engine(
    url,
    pool_pre_ping=True,  # Verifica antes de usar
    pool_recycle=3600,   # Recicla cada hora
)
```

### Problema 4: Session en Múltiples Endpoints

```python
# ❌ MALO - NO funciona
session = None

@app.on_event("startup")
async def startup():
    global session
    session = AsyncSession(engine)

@app.get("/restaurants")
async def get_restaurants():
    return await session.exec(select(Restaurant))
```

**Solución:**

```python
# ✅ BUENO - Usa Dependency
@app.get("/restaurants")
async def get_restaurants(
    session: AsyncSession = Depends(get_async_session_dependency)
):
    return await session.exec(select(Restaurant))
```

### Problema 5: Tests Fallan con Pool

```python
# ❌ MALO - Comparte engine con app
engine = create_async_engine(...)  # Global

# ✅ BUENO - Engine separado para tests
@pytest.fixture
async def test_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    yield engine
    await engine.dispose()
```

---

## 📝 Resumen Ejecutivo

### ¿Qué hicimos hoy?

1. ✅ **Confirmamos** que tu implementación ya está correcta
2. ✅ **Añadimos** `pool_recycle` a los adaptadores de PostgreSQL
3. ✅ **Explicamos** por qué Engine va en Lifespan y no en Dependency
4. ✅ **Documentamos** el pool de conexiones y su configuración

### ¿Qué NO debes cambiar?

- ❌ No muevas Engine a Dependency
- ❌ No crees Engine global fuera de Lifespan
- ❌ No cambies la arquitectura actual
- ❌ No remuevas los context managers

### ¿Qué SÍ puedes ajustar?

- ✅ Valores de `pool_size` según tu tráfico
- ✅ Valores de `max_overflow` según tus necesidades
- ✅ `pool_recycle` según timeout de tu DB
- ✅ `echo=True` en desarrollo para debug

### Checklist Final

```bash
✅ Engine creado en Lifespan
✅ Un solo adapter compartido
✅ Sessions por request vía Dependency
✅ Context managers para cleanup
✅ pool_pre_ping=True para PostgreSQL
✅ pool_size configurado
✅ max_overflow configurado
✅ pool_recycle configurado
✅ Engine.dispose() en shutdown
```

---

## 🎓 Para Profundizar

### Documentación Oficial

- [SQLAlchemy Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)
- [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)
- [SQLModel with FastAPI](https://sqlmodel.tiangolo.com/)
- [asyncpg Performance](https://github.com/MagicStack/asyncpg)

### Otras Guías en este Proyecto

- `Database_Best_Practices.md` - Mejores prácticas generales
- `Lifespan_Explained_ES.md` - Explicación detallada del lifespan
- `Flujo_Visual_ES.md` - Diagramas visuales del flujo
- `Cheat_Sheet_ES.md` - Referencia rápida

### Código de Ejemplo

```bash
# Ver adaptadores
$ cat app/clients/sql/adapters/postgres/asynchronous.py
$ cat app/clients/sql/adapters/sqlite/asynchronous.py

# Ver lifespan
$ cat app/core/lifespan.py

# Ver dependencies
$ cat app/shared/dependencies/sql.py

# Ejecutar ejemplos
$ uv run python examples/test_lifespan.py
```

---

## 🎯 Conclusión

Tu aplicación **YA está usando las mejores prácticas**:

1. ✅ Engine en Lifespan (no en Dependency)
2. ✅ Pool de conexiones configurado
3. ✅ Adapter compartido globalmente
4. ✅ Sessions por request
5. ✅ Cleanup automático

Los únicos cambios que hicimos fueron **añadir `pool_recycle`** para evitar timeouts en PostgreSQL.

**¡No necesitas hacer más cambios! Tu arquitectura es sólida.** 🎉

---

¿Preguntas? Lee las otras guías o ejecuta los ejemplos en `examples/`.


