"""Comparación: CON y SIN lifespan.

Este archivo muestra la diferencia entre usar lifespan y no usarlo.
Puedes ejecutar ambos ejemplos para ver cómo funcionan.
"""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.clients.sql import create_async_sqlite_adapter
from app.domains.restaurants.models import Restaurant


# =============================================================================
# ❌ EJEMPLO 1: SIN LIFESPAN (Anti-patrón - NO USAR)
# =============================================================================


async def get_session_sin_lifespan() -> AsyncSession:
    """Dependencia SIN lifespan - ANTI-PATRÓN.

    Problema: Crea un nuevo adapter en CADA request.
    Esto es lento e ineficiente.
    """
    print("⚠️  Creando adapter nuevo (costoso)...")

    # 🔴 PROBLEMA: Esto se ejecuta en CADA request
    adapter = create_async_sqlite_adapter(
        database_url="sqlite+aiosqlite:///./local.db",
        echo=False,
    )

    async with adapter.get_session() as session:
        yield session

    # 🔴 PROBLEMA: Tenemos que cerrar manualmente
    print("⚠️  Cerrando adapter...")
    await adapter.engine.dispose()


app_sin_lifespan = FastAPI(title="Sin Lifespan (Malo)")


@app_sin_lifespan.get("/restaurants")
async def get_restaurants_sin_lifespan(
    session: AsyncSession = Depends(get_session_sin_lifespan),
):
    """Endpoint que usa la dependencia sin lifespan.

    Cada vez que llamas a este endpoint:
    1. Crea un adapter nuevo (lento)
    2. Obtiene la session
    3. Ejecuta la query
    4. Cierra el adapter

    Resultado: Lento y costoso para cada request.
    """
    result = await session.exec(select(Restaurant))
    return result.all()


# =============================================================================
# ✅ EJEMPLO 2: CON LIFESPAN (Patrón correcto - USAR ESTE)
# =============================================================================

# Variable global para guardar el adapter (compartido por toda la app)
_shared_adapter = None


@asynccontextmanager
async def lifespan_correcto(app: FastAPI):
    """Lifespan que maneja el ciclo de vida del adapter.

    STARTUP (una vez):
    - Crea el adapter
    - Lo guarda en una variable global
    - Queda disponible para todos los requests

    SHUTDOWN (una vez):
    - Cierra el adapter
    - Libera recursos
    """
    global _shared_adapter

    # 🚀 STARTUP - Se ejecuta UNA VEZ cuando inicias la app
    print("🟢 [STARTUP] Creando adapter compartido...")
    _shared_adapter = create_async_sqlite_adapter(
        database_url="sqlite+aiosqlite:///./local.db",
        echo=False,
    )
    print("✅ [STARTUP] Adapter creado y listo para usar")
    print("📊 [INFO] Este adapter se reutilizará en todos los requests")

    # La aplicación corre aquí (puede ser horas/días)
    yield

    # 🛑 SHUTDOWN - Se ejecuta UNA VEZ cuando cierras la app
    print("🔴 [SHUTDOWN] Cerrando adapter compartido...")
    await _shared_adapter.engine.dispose()
    print("👋 [SHUTDOWN] Aplicación cerrada correctamente")


def get_shared_adapter():
    """Obtiene el adapter compartido creado en el lifespan.

    Raises:
        RuntimeError: Si se llama antes de que la app inicie
    """
    if _shared_adapter is None:
        msg = "El adapter no está disponible. ¿La app ha iniciado?"
        raise RuntimeError(msg)
    return _shared_adapter


async def get_session_con_lifespan() -> AsyncSession:
    """Dependencia CON lifespan - PATRÓN CORRECTO.

    Esta función se ejecuta en cada request, pero:
    - NO crea un adapter nuevo
    - USA el adapter compartido del lifespan
    - Solo crea una session temporal
    """
    print("✅ Obteniendo session del adapter compartido (rápido)...")

    # ✅ Obtiene el adapter que ya existe (compartido)
    adapter = get_shared_adapter()

    # Crea una session temporal solo para este request
    async with adapter.get_session() as session:
        yield session

    print("✅ Session cerrada automáticamente")
    # No necesitamos cerrar el adapter - sigue vivo para otros requests


app_con_lifespan = FastAPI(
    title="Con Lifespan (Correcto)",
    lifespan=lifespan_correcto,  # ← Aquí conectamos el lifespan
)


@app_con_lifespan.get("/restaurants")
async def get_restaurants_con_lifespan(
    session: AsyncSession = Depends(get_session_con_lifespan),
):
    """Endpoint que usa la dependencia con lifespan.

    Primera vez que llamas al endpoint:
    1. Lifespan ya creó el adapter (en startup)
    2. Obtiene session del adapter compartido (rápido)
    3. Ejecuta la query
    4. Cierra la session (adapter sigue vivo)

    Siguientes veces:
    1. Usa el mismo adapter (sin crear nada)
    2. Obtiene session del adapter compartido (rápido)
    3. Ejecuta la query
    4. Cierra la session (adapter sigue vivo)

    Resultado: Rápido y eficiente. El adapter se reutiliza.
    """
    result = await session.exec(select(Restaurant))
    return result.all()


# =============================================================================
# 📊 COMPARACIÓN DE RENDIMIENTO
# =============================================================================

"""
Simulemos 100 requests:

❌ SIN LIFESPAN:
├─ Request 1: [Crear adapter] → [Query] → [Cerrar adapter] = 100ms
├─ Request 2: [Crear adapter] → [Query] → [Cerrar adapter] = 100ms
├─ Request 3: [Crear adapter] → [Query] → [Cerrar adapter] = 100ms
└─ ... (97 más) ...
Total: 100 requests × 100ms = 10 segundos 🐌

✅ CON LIFESPAN:
[Startup: Crear adapter una vez = 50ms]
├─ Request 1: [Query] = 10ms
├─ Request 2: [Query] = 10ms
├─ Request 3: [Query] = 10ms
└─ ... (97 más) ...
Total: 50ms + (100 requests × 10ms) = 1.05 segundos ⚡
[Shutdown: Cerrar adapter una vez = 50ms]

RESULTADO: 10x más rápido con lifespan! 🚀
"""

# =============================================================================
# 🎯 PARA USAR EN TU APP
# =============================================================================

"""
Ya lo tienes configurado correctamente en:

1. app/core/lifespan.py:
   - Define el lifespan
   - Crea adapters en startup
   - Los cierra en shutdown

2. app/main.py:
   - app = FastAPI(lifespan=lifespan)

3. app/shared/dependencies/sql.py:
   - get_async_session_dependency()
   - Usa el adapter del lifespan

4. Tus endpoints:
   - @router.get("/...")
   - async def handler(session = Depends(get_async_session_dependency))
   - ¡Ya funciona correctamente!

NO NECESITAS CAMBIAR NADA EN TUS ENDPOINTS.
La magia pasa detrás de escena. 🎩✨
"""

# =============================================================================
# 🧪 CÓMO PROBAR ESTE ARCHIVO
# =============================================================================

"""
Terminal 1 - Sin lifespan (lento):
$ uvicorn examples.lifespan_comparison:app_sin_lifespan --reload

Terminal 2 - Con lifespan (rápido):
$ uvicorn examples.lifespan_comparison:app_con_lifespan --reload

Luego haz varios requests y observa la diferencia en los logs:
$ curl http://localhost:8000/restaurants

Verás:
- Sin lifespan: "Creando adapter..." en CADA request
- Con lifespan: "Obteniendo session del adapter compartido" (mucho más rápido)
"""
