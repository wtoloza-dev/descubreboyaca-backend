# Entendiendo Lifespan en FastAPI

## 🎯 ¿Qué es Lifespan?

**Lifespan** es un concepto de FastAPI para manejar cosas que deben:
- ✅ Crearse **UNA VEZ** cuando la aplicación inicia
- ✅ Mantenerse **VIVAS** durante toda la ejecución
- ✅ Destruirse **UNA VEZ** cuando la aplicación termina

## 🔄 Timeline de la Aplicación

```
1. uvicorn app.main:app
   │
   ├─ ⚡ LIFESPAN STARTUP (una vez)
   │   └─ Crea adaptadores de base de datos
   │   └─ Crea pools de conexiones
   │   └─ Cualquier inicialización pesada
   │
   ├─ 🚀 APLICACIÓN CORRIENDO
   │   │
   │   ├─ Request 1 → Dependency Injection → Usa adapter compartido
   │   ├─ Request 2 → Dependency Injection → Usa adapter compartido
   │   ├─ Request 3 → Dependency Injection → Usa adapter compartido
   │   └─ ... miles de requests más ...
   │
   └─ ⚡ LIFESPAN SHUTDOWN (una vez)
       └─ Cierra adaptadores de base de datos
       └─ Libera recursos
```

## 🎭 Los Dos Actores

### Actor 1: Lifespan (El Gerente)
**Responsabilidad:** Crear recursos pesados una sola vez

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🚀 STARTUP - Se ejecuta UNA VEZ cuando inicias la app
    print("🟢 Iniciando aplicación...")
    
    global _db_adapter
    _db_adapter = crear_adaptador_db()  # COSTOSO - solo una vez
    
    print("✅ Aplicación lista para recibir requests")
    
    yield  # ← La app corre AQUÍ (puede ser horas/días)
    
    # 🛑 SHUTDOWN - Se ejecuta UNA VEZ cuando cierras la app
    print("🔴 Cerrando aplicación...")
    _db_adapter.engine.dispose()  # Limpieza
    print("👋 Aplicación cerrada")
```

### Actor 2: Dependency Injection (El Mesero)
**Responsabilidad:** Dar acceso al recurso en cada request

```python
async def get_session() -> AsyncSession:
    # 📥 Se ejecuta en CADA REQUEST
    adapter = get_adapter()  # Obtiene el adapter creado en lifespan
    async with adapter.get_session() as session:
        yield session  # ← Le da la session al endpoint
    # Automáticamente cierra la session cuando termina
```

## 📊 Comparación Visual

### ❌ SIN Lifespan (Anti-patrón)

```python
# Esto es lo que NO queremos hacer

async def get_session():
    # 🔴 PROBLEMA: Crea adapter en CADA request
    adapter = SQLiteAdapter("sqlite:///db.db")  # ¡Costoso!
    async with adapter.get_session() as session:
        yield session
    await adapter.close()  # Manual

# Resultado:
# Request 1: Crear adapter → Usar → Cerrar adapter
# Request 2: Crear adapter → Usar → Cerrar adapter
# Request 3: Crear adapter → Usar → Cerrar adapter
# ❌ Lento, ineficiente, no usa connection pooling
```

### ✅ CON Lifespan (Correcto)

```python
# 1️⃣ Lifespan - Crea adapter UNA VEZ
@asynccontextmanager
async def lifespan(app: FastAPI):
    global _adapter
    _adapter = SQLiteAdapter("sqlite:///db.db")  # UNA VEZ
    yield
    await _adapter.engine.dispose()  # UNA VEZ

# 2️⃣ Dependency - Usa adapter compartido
async def get_session():
    adapter = get_adapter()  # Obtiene el que ya existe
    async with adapter.get_session() as session:
        yield session

# Resultado:
# Startup: Crear adapter (una vez)
# Request 1: Obtener session del adapter
# Request 2: Obtener session del adapter
# Request 3: Obtener session del adapter
# Shutdown: Cerrar adapter (una vez)
# ✅ Rápido, eficiente, connection pooling funciona
```

## 🔍 Veamos tu Código Paso a Paso

### Paso 1: Lifespan crea recursos (app/core/lifespan.py)

```python
# Esta variable guarda el adapter para toda la app
_async_adapter = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _async_adapter
    
    # 🚀 ESTO SE EJECUTA UNA VEZ AL INICIAR
    print("Creando adapter de base de datos...")
    _async_adapter = create_async_sqlite_adapter(
        database_url="sqlite+aiosqlite:///./local.db",
        echo=False,
    )
    print("✅ Adapter creado y listo")
    
    # La app corre aquí ↓
    yield
    
    # 🛑 ESTO SE EJECUTA UNA VEZ AL CERRAR
    print("Cerrando adapter...")
    await _async_adapter.engine.dispose()
    print("✅ Adapter cerrado")

# Función helper para obtener el adapter desde cualquier lugar
def get_async_adapter():
    if _async_adapter is None:
        raise RuntimeError("App no ha iniciado aún!")
    return _async_adapter
```

### Paso 2: FastAPI usa el lifespan (app/main.py)

```python
from app.core.lifespan import lifespan

# Le dices a FastAPI: "Usa esta función para startup/shutdown"
app = FastAPI(
    title="Mi API",
    lifespan=lifespan,  # ← Aquí le pasas la función
)
```

### Paso 3: Dependencias usan el adapter (app/shared/dependencies/sql.py)

```python
from app.core.lifespan import get_async_adapter

async def get_async_session_dependency():
    # 📥 Esto se ejecuta en CADA REQUEST
    
    # Obtiene el adapter que se creó en startup (compartido)
    adapter = get_async_adapter()
    
    # Crea una session temporal para este request
    async with adapter.get_session() as session:
        yield session  # ← El endpoint usa esta session
    
    # La session se cierra automáticamente aquí
```

### Paso 4: Tus endpoints usan la dependencia (normal)

```python
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.shared.dependencies import get_async_session_dependency

@router.get("/restaurants")
async def get_restaurants(
    # 📥 FastAPI llama automáticamente a get_async_session_dependency
    session: AsyncSession = Depends(get_async_session_dependency)
):
    # Usas la session normalmente
    result = await session.exec(select(Restaurant))
    return result.all()
    
# Cuando termina el endpoint, la session se cierra automáticamente
```

## 🎬 Secuencia Completa

```
1. Terminal: uvicorn app.main:app
   │
2. FastAPI ve: app = FastAPI(lifespan=lifespan)
   │
3. FastAPI ejecuta: lifespan startup
   ├─ Crea _async_adapter
   └─ _async_adapter vive en memoria
   │
4. FastAPI: "Listo para recibir requests"
   │
5. Request llega a /restaurants
   │
6. FastAPI ve: session: AsyncSession = Depends(...)
   │
7. FastAPI llama: get_async_session_dependency()
   ├─ Llama: get_async_adapter() → devuelve _async_adapter existente
   ├─ Crea: session del adapter
   └─ Pasa session al endpoint
   │
8. Endpoint ejecuta con la session
   │
9. Endpoint termina
   │
10. FastAPI cierra la session automáticamente
   │
11. (Repeat 5-10 para cada request)
   │
12. Terminal: Ctrl+C (cerrar app)
   │
13. FastAPI ejecuta: lifespan shutdown
    └─ Cierra _async_adapter
    │
14. App terminada
```

## ❓ Preguntas Frecuentes

### P: ¿Por qué no crear el adapter en la dependencia?
```python
# ❌ Malo
async def get_session():
    adapter = SQLiteAdapter(...)  # Crea adapter nuevo cada vez
    ...
```

**R:** Porque crear un adapter (engine) es **costoso**:
- Inicializa connection pool
- Configura drivers
- Reserva recursos del sistema
- Toma tiempo

Hacerlo en cada request es lento e ineficiente.

### P: ¿El adapter se comparte entre todos los requests?
**R:** ✅ Sí, el **adapter** (engine) se comparte, pero cada request tiene su propia **session**:

```
┌─────────────────────────┐
│   UN Adapter (shared)    │  ← Creado en lifespan
│   ├─ Engine             │
│   └─ Connection Pool    │
└─────────────────────────┘
         │
    ┌────┴────┬────────┬────────┐
    │         │        │        │
┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
│Sess1│  │Sess2│  │Sess3│  │Sess4│  ← Una por request
└─────┘  └─────┘  └─────┘  └─────┘
```

### P: ¿Es seguro compartir el adapter entre requests?
**R:** ✅ **Totalmente seguro**. Es el patrón recomendado:
- El adapter/engine es thread-safe
- Cada request tiene su propia session
- SQLAlchemy maneja el connection pooling
- Es así como está diseñado para funcionar

### P: ¿Qué pasa si la app crashea?
**R:** Python ejecuta el cleanup automáticamente:
```python
@asynccontextmanager
async def lifespan(app):
    adapter = crear_adapter()
    try:
        yield  # App corre
    finally:  # SIEMPRE se ejecuta, incluso si hay error
        await adapter.engine.dispose()
```

## 🎯 Conclusión Simple

**Lifespan es como el constructor y destructor de tu aplicación:**

```python
class Aplicacion:
    def __init__(self):  # ← Lifespan STARTUP
        self.db = crear_base_datos()
    
    def procesar_request(self, request):  # ← Dependency Injection
        session = self.db.get_session()
        # ... procesar ...
        session.close()
    
    def __del__(self):  # ← Lifespan SHUTDOWN
        self.db.cerrar()
```

**En FastAPI:**
- Lifespan = `__init__` y `__del__`
- Dependency Injection = `procesar_request`

## 📚 Para Recordar

| Concepto | Cuándo | Cuántas veces | Para qué |
|----------|--------|---------------|----------|
| **Lifespan Startup** | Al iniciar app | 1 vez | Crear recursos pesados |
| **Dependency Injection** | En cada request | Miles de veces | Dar acceso a recursos |
| **Lifespan Shutdown** | Al cerrar app | 1 vez | Limpiar recursos |

## ✅ Esto es Normal y Correcto

- ✅ FastAPI recomienda este patrón
- ✅ SQLAlchemy está diseñado para esto
- ✅ Todas las apps grandes lo usan
- ✅ Es el patrón estándar de la industria

¡No te preocupes! Una vez que lo uses, verás que es muy simple y natural. 🚀

