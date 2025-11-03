"""Script simple para entender lifespan visualmente.

Ejecuta este script para VER cómo funciona lifespan:
$ cd descubreboyaca-backend
$ uv run python examples/test_lifespan.py
"""

import asyncio
from contextlib import asynccontextmanager


# =============================================================================
# 🎬 SIMULACIÓN: Cómo funciona lifespan
# =============================================================================


class BaseDeDatos:
    """Simula un adapter de base de datos."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        print(f"    💰 [{self.nombre}] Creando engine... (operación COSTOSA)")
        print(f"    ⏱️  [{self.nombre}] Tardó 50ms")

    async def get_session(self):
        """Simula obtener una session."""
        print(f"        📝 [{self.nombre}] Creando session temporal (rápido)")
        return f"Session-{id(self)}"

    async def dispose(self):
        """Simula cerrar la base de datos."""
        print(f"    🗑️  [{self.nombre}] Cerrando engine...")


# =============================================================================
# ❌ FORMA INCORRECTA: Sin lifespan
# =============================================================================


async def forma_incorrecta():
    """Demuestra por qué NO usar lifespan es malo."""
    print("\n" + "=" * 70)
    print("❌ FORMA INCORRECTA: Sin lifespan")
    print("=" * 70)

    print("\n🚀 Simulando 3 requests...\n")

    for i in range(1, 4):
        print(f"📨 Request {i}:")

        # Crea una base de datos NUEVA en cada request
        db = BaseDeDatos(f"DB-Request{i}")

        # Usa la base de datos
        session = await db.get_session()
        print(f"        ✅ Ejecutando query con {session}")

        # Cierra la base de datos
        await db.dispose()

        print()

    print("📊 Resultado:")
    print("   - Creamos 3 bases de datos (3 × 50ms = 150ms)")
    print("   - Muy lento e ineficiente")
    print("   - No aprovecha connection pooling")


# =============================================================================
# ✅ FORMA CORRECTA: Con lifespan
# =============================================================================


@asynccontextmanager
async def simular_lifespan():
    """Simula el lifespan de FastAPI."""
    # STARTUP
    print("\n🟢 [LIFESPAN STARTUP]")
    db_compartida = BaseDeDatos("DB-Compartida")
    print("    ✅ Base de datos lista y compartida para todos los requests\n")

    yield db_compartida  # La app corre aquí

    # SHUTDOWN
    print("\n🔴 [LIFESPAN SHUTDOWN]")
    await db_compartida.dispose()
    print("    ✅ Base de datos cerrada correctamente")


async def forma_correcta():
    """Demuestra por qué usar lifespan es bueno."""
    print("\n" + "=" * 70)
    print("✅ FORMA CORRECTA: Con lifespan")
    print("=" * 70)

    async with simular_lifespan() as db_compartida:
        print("🚀 Simulando 3 requests...\n")

        for i in range(1, 4):
            print(f"📨 Request {i}:")

            # USA la base de datos compartida (no crea una nueva)
            session = await db_compartida.get_session()
            print(f"        ✅ Ejecutando query con {session}")
            print("        ↩️  Session cerrada automáticamente\n")

    print("\n📊 Resultado:")
    print("   - Creamos 1 base de datos (1 × 50ms = 50ms)")
    print("   - Muy rápido y eficiente")
    print("   - Aprovecha connection pooling")


# =============================================================================
# 🎯 COMPARACIÓN DIRECTA
# =============================================================================


async def comparacion():
    """Muestra la diferencia lado a lado."""
    await forma_incorrecta()
    await forma_correcta()

    print("\n" + "=" * 70)
    print("🎯 CONCLUSIÓN")
    print("=" * 70)
    print("""
❌ SIN LIFESPAN:
   ├─ Request 1: [Crear DB] → [Query] → [Cerrar DB]
   ├─ Request 2: [Crear DB] → [Query] → [Cerrar DB]
   └─ Request 3: [Crear DB] → [Query] → [Cerrar DB]
   Tiempo total: 150ms + tiempo de queries

✅ CON LIFESPAN:
   [Startup: Crear DB una vez = 50ms]
   ├─ Request 1: [Query]
   ├─ Request 2: [Query]
   └─ Request 3: [Query]
   [Shutdown: Cerrar DB una vez]
   Tiempo total: 50ms + tiempo de queries

RESULTADO: 3x más rápido con lifespan! 🚀

EN TU APLICACIÓN REAL:
- Ya tienes lifespan configurado en app/core/lifespan.py
- FastAPI lo ejecuta automáticamente
- Tus endpoints solo reciben la session (dependency injection)
- ¡No tienes que hacer nada especial!
    """)


# =============================================================================
# 🔍 BONUS: Ver las variables globales
# =============================================================================


_variable_global = None


@asynccontextmanager
async def lifespan_con_variable_global():
    """Muestra cómo funcionan las variables globales en lifespan."""
    global _variable_global

    print("\n" + "=" * 70)
    print("🔍 BONUS: Variables Globales en Lifespan")
    print("=" * 70)

    # STARTUP
    print("\n🟢 [STARTUP]")
    print(f"   Variable global antes: {_variable_global}")
    _variable_global = BaseDeDatos("DB-Global")
    print(f"   Variable global después: {_variable_global}")
    print("   ✅ Ahora cualquier función puede acceder a _variable_global\n")

    yield

    # SHUTDOWN
    print("\n🔴 [SHUTDOWN]")
    print(f"   Variable global: {_variable_global}")
    await _variable_global.dispose()
    _variable_global = None
    print(f"   Variable global después: {_variable_global}")


def obtener_db_global():
    """Simula get_async_adapter() en tu código."""
    if _variable_global is None:
        raise RuntimeError("⚠️  La aplicación no ha iniciado aún!")
    return _variable_global


async def usar_variable_global():
    """Muestra cómo usar la variable global."""
    async with lifespan_con_variable_global():
        print("📨 Simulando requests que usan la variable global:\n")

        for i in range(1, 3):
            print(f"Request {i}:")

            # Obtiene la DB de la variable global
            db = obtener_db_global()
            print(f"   ✅ Obtuve: {db}")

            session = await db.get_session()
            print(f"   ✅ Ejecutando query con {session}\n")

    print("\n📝 Explicación:")
    print("""
Esto es EXACTAMENTE lo que pasa en tu código:

1. app/core/lifespan.py:
   global _async_adapter
   _async_adapter = create_adapter()  ← STARTUP

2. app/shared/dependencies/sql.py:
   adapter = get_async_adapter()  ← Obtiene _async_adapter
   async with adapter.get_session() as session:
       yield session

3. Tu endpoint:
   async def handler(session = Depends(...)):
       # Usa la session que viene del adapter global
       pass

La variable global (_async_adapter) se crea UNA VEZ y vive
durante toda la ejecución de la aplicación.
    """)


# =============================================================================
# 🎬 EJECUTAR TODO
# =============================================================================


async def main():
    """Ejecuta todas las demostraciones."""
    print("\n" + "=" * 70)
    print("🎓 TUTORIAL INTERACTIVO: Entendiendo Lifespan")
    print("=" * 70)

    # 1. Comparación básica
    await comparacion()

    # 2. Variables globales
    await usar_variable_global()

    print("\n" + "=" * 70)
    print("✅ TUTORIAL COMPLETADO")
    print("=" * 70)
    print("""
Ahora entiendes:
1. ✅ Por qué usar lifespan (eficiencia)
2. ✅ Cómo funciona (startup + shutdown)
3. ✅ Variables globales (compartir recursos)
4. ✅ Relación con dependency injection

Tu código ya está usando este patrón correctamente! 🎉

Siguiente paso:
1. Lee: docs/code/Lifespan_Explained_ES.md
2. Mira: examples/lifespan_comparison.py
3. Tu app ya funciona con este patrón!
    """)


if __name__ == "__main__":
    asyncio.run(main())
