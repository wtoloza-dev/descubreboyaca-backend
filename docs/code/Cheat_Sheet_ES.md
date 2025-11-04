# 📋 Cheat Sheet: Lifespan en 5 Minutos

## 🎯 Lo Esencial

```python
# ❌ ANTES (mal - lento)
async def get_session():
    adapter = crear_adapter()  # Crea en CADA request
    session = adapter.get_session()
    yield session
    adapter.close()  # Manual

# ✅ AHORA (bien - rápido)
@asynccontextmanager
async def lifespan(app):
    adapter = crear_adapter()  # Crea UNA VEZ
    yield
    adapter.close()  # Cierra UNA VEZ

async def get_session():
    adapter = obtener_adapter_compartido()  # Usa el existente
    session = adapter.get_session()
    yield session
```

## 📝 Tu Código (Ya Está Correcto)

### 1. Lifespan (app/core/lifespan.py)
```python
_async_adapter = None  # Variable global

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _async_adapter
    
    # STARTUP (una vez al iniciar)
    _async_adapter = create_async_sqlite_adapter(...)
    
    yield  # App corre aquí
    
    # SHUTDOWN (una vez al cerrar)
    await _async_adapter.engine.dispose()
```

### 2. Conectar Lifespan (app/main.py)
```python
from app.core.lifespan import lifespan

app = FastAPI(
    lifespan=lifespan  # ← Esta línea conecta todo
)
```

### 3. Dependencia (app/shared/dependencies/sql.py)
```python
from app.core.lifespan import get_async_adapter

async def get_async_session_dependency():
    adapter = get_async_adapter()  # Obtiene el compartido
    async with adapter.get_session() as session:
        yield session
```

### 4. Tu Endpoint (NO CAMBIAS NADA)
```python
@router.get("/restaurants")
async def get_restaurants(
    session: AsyncSession = Depends(get_async_session_dependency)
):
    result = await session.exec(select(Restaurant))
    return result.all()
```

## ⚡ Cuándo Se Ejecuta Cada Cosa

```
$ uvicorn app.main:app
  │
  ├─ [1x] lifespan STARTUP
  │   └─ Crea _async_adapter
  │
  ├─ [∞] FastAPI escucha requests
  │   ├─ Request 1 → get_session_dependency() → endpoint
  │   ├─ Request 2 → get_session_dependency() → endpoint
  │   └─ Request N → get_session_dependency() → endpoint
  │
  └─ [1x] lifespan SHUTDOWN (Ctrl+C)
      └─ Cierra _async_adapter
```

## 🧠 Recordar Esto

| Pregunta | Respuesta |
|----------|-----------|
| ¿Qué es lifespan? | Startup + Shutdown de la app |
| ¿Cuándo se ejecuta? | 1 vez al iniciar + 1 vez al cerrar |
| ¿Para qué? | Crear recursos pesados una sola vez |
| ¿Cambio mis endpoints? | **NO** - siguen igual |
| ¿Es complicado? | **NO** - FastAPI lo maneja automático |

## 🎓 Analogías Simples

**Lifespan = Constructor/Destructor**
```python
class App:
    def __init__(self):      # ← lifespan startup
        self.db = crear_db()
    
    def procesar(self):      # ← dependency injection
        session = self.db.get_session()
        # ...
    
    def __del__(self):       # ← lifespan shutdown
        self.db.cerrar()
```

**Lifespan = Restaurant**
- Abrir restaurant → Instalar cocina (lifespan startup)
- Cliente llega → Usar cocina (dependency)
- Cerrar restaurant → Desinstalar cocina (lifespan shutdown)

## 🔍 Debugging: Ver Qué Pasa

Agrega prints para entender:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🟢 [STARTUP] Iniciando...")
    _adapter = create_adapter()
    print(f"✅ [STARTUP] Adapter creado: {_adapter}")
    
    yield
    
    print("🔴 [SHUTDOWN] Cerrando...")
    await _adapter.engine.dispose()
    print("✅ [SHUTDOWN] Adapter cerrado")

async def get_session():
    print("📥 [REQUEST] Obteniendo session...")
    adapter = get_adapter()
    async with adapter.get_session() as session:
        print(f"✅ [REQUEST] Session obtenida: {session}")
        yield session
    print("✅ [REQUEST] Session cerrada")
```

Verás en la consola:
```
🟢 [STARTUP] Iniciando...
✅ [STARTUP] Adapter creado: <SQLiteAdapter...>
📥 [REQUEST] Obteniendo session...
✅ [REQUEST] Session obtenida: <AsyncSession...>
✅ [REQUEST] Session cerrada
📥 [REQUEST] Obteniendo session...
✅ [REQUEST] Session obtenida: <AsyncSession...>
✅ [REQUEST] Session cerrada
^C
🔴 [SHUTDOWN] Cerrando...
✅ [SHUTDOWN] Adapter cerrado
```

## ✅ Checklist: ¿Lo Tengo Bien?

- [ ] ✅ Tengo `lifespan.py` con `@asynccontextmanager`
- [ ] ✅ Tengo `app = FastAPI(lifespan=lifespan)` en `main.py`
- [ ] ✅ Mi dependencia usa `get_async_adapter()` (no crea uno nuevo)
- [ ] ✅ Mis endpoints usan `Depends(get_async_session_dependency)`
- [ ] ✅ No tengo `adapter.close()` en mis dependencias

Si marcaste todos ✅ → **¡Está perfecto!** 🎉

## 🚀 Para Probar

```bash
# Terminal 1: Ejecuta el tutorial interactivo
$ cd descubreboyaca-backend
$ uv run python examples/test_lifespan.py

# Terminal 2: Ejecuta tu app y observa los logs
$ uv run fastapi dev app/main.py
# Verás los mensajes de startup/shutdown

# Terminal 3: Haz requests
$ curl http://localhost:8000/api/v1/restaurants
```

## 📚 Documentación Completa

1. **Introducción**: `docs/code/Lifespan_Explained_ES.md`
2. **Visualización**: `docs/code/Flujo_Visual_ES.md`
3. **Ejemplo de código**: `examples/lifespan_comparison.py`
4. **Tutorial interactivo**: `examples/test_lifespan.py`

## 💬 Preguntas Frecuentes

**P: ¿Tengo que cambiar algo en mis endpoints?**
R: **NO**. Siguen igual.

**P: ¿Dónde está el "close()" ahora?**
R: En `lifespan shutdown`. FastAPI lo llama automáticamente.

**P: ¿El adapter es compartido entre requests?**
R: **SÍ** - el adapter. **NO** - las sessions (cada request tiene la suya).

**P: ¿Es seguro compartir el adapter?**
R: **SÍ**. Es el patrón oficial de FastAPI + SQLAlchemy.

**P: ¿Y si no uso lifespan?**
R: Tu app funcionará pero será más lenta e ineficiente.

**P: ¿Es obligatorio en producción?**
R: No obligatorio, pero **altamente recomendado** para performance.

## 🎯 Resumen en 3 Puntos

1. **Lifespan** = Crea recursos pesados una vez
2. **Dependency** = Distribuye recursos en cada request
3. **Tu código** = Ya está usando este patrón ✅

¡Listo! Ya entiendes lifespan. 🚀


