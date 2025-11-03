# 📚 Documentación Completa: Lifespan + Database

## 🎯 ¿Por Dónde Empezar?

### Si nunca has usado Lifespan:
1. ⭐ **[Cheat Sheet](./Cheat_Sheet_ES.md)** - Empieza aquí (5 minutos)
2. 📖 **[Explicación Completa](./Lifespan_Explained_ES.md)** - Lee esto después
3. 🎨 **[Flujo Visual](./Flujo_Visual_ES.md)** - Visualiza cómo funciona
4. 🧪 **[Tutorial Interactivo](../../examples/test_lifespan.py)** - Ejecuta y aprende

### Si vienes de Dependency Injection:
1. 📖 **[Explicación Completa](./Lifespan_Explained_ES.md)** - Lee esto primero
2. 🎨 **[Flujo Visual](./Flujo_Visual_ES.md)** - Ve el flujo completo
3. 📋 **[Cheat Sheet](./Cheat_Sheet_ES.md)** - Referencia rápida

### Si quieres implementar:
1. 📚 **[Best Practices](./Database_Best_Practices.md)** - Guía completa (inglés)
2. 💻 **[Ejemplo Comparativo](../../examples/lifespan_comparison.py)** - Código real
3. 📋 **[Cheat Sheet](./Cheat_Sheet_ES.md)** - Para copiar/pegar

---

## 📁 Documentación Disponible

### 🇪🇸 En Español

#### 1️⃣ **Cheat_Sheet_ES.md** ⚡
**Para:** Referencia rápida  
**Tiempo:** 5 minutos  
**Contenido:**
- ✅ Lo esencial en código
- ✅ Checklist de verificación
- ✅ Preguntas frecuentes
- ✅ Comandos para probar

```bash
# Ver el cheat sheet
$ cat docs/code/Cheat_Sheet_ES.md
```

#### 2️⃣ **Lifespan_Explained_ES.md** 📖
**Para:** Entender a fondo  
**Tiempo:** 20 minutos  
**Contenido:**
- ✅ ¿Qué es lifespan?
- ✅ Comparación con dependency injection
- ✅ Timeline completo de la app
- ✅ Ejemplos paso a paso
- ✅ Preguntas frecuentes

```bash
# Leer la explicación
$ cat docs/code/Lifespan_Explained_ES.md
```

#### 3️⃣ **Flujo_Visual_ES.md** 🎨
**Para:** Ver el flujo visualmente  
**Tiempo:** 10 minutos  
**Contenido:**
- ✅ Diagrama completo animado
- ✅ Flujo de startup a shutdown
- ✅ Analogía de la pizzería
- ✅ Tabla comparativa

```bash
# Ver el flujo visual
$ cat docs/code/Flujo_Visual_ES.md
```

### 🇬🇧 En Inglés

#### 4️⃣ **Database_Best_Practices.md** 📚
**Para:** Implementación profesional  
**Tiempo:** 30 minutos  
**Contenido:**
- ✅ Arquitectura completa
- ✅ Patrones de diseño
- ✅ Performance y optimización
- ✅ Testing
- ✅ Referencias oficiales

```bash
# Leer las best practices
$ cat docs/code/Database_Best_Practices.md
```

---

## 💻 Ejemplos de Código

### 🧪 **test_lifespan.py** (Interactivo)
**Para:** Aprender ejecutando  
**Tiempo:** 10 minutos  

```bash
# Ejecutar el tutorial interactivo
$ cd descubreboyaca-backend
$ uv run python examples/test_lifespan.py
```

**Qué hace:**
- Simula una app con y sin lifespan
- Muestra la diferencia en rendimiento
- Explica las variables globales
- Demuestra el flujo completo

### 📝 **lifespan_comparison.py** (Comparación)
**Para:** Ver código real  
**Tiempo:** 15 minutos  

```bash
# Ver el código
$ cat examples/lifespan_comparison.py

# Ejecutar ejemplo sin lifespan (lento)
$ uv run uvicorn examples.lifespan_comparison:app_sin_lifespan --reload

# Ejecutar ejemplo con lifespan (rápido)
$ uv run uvicorn examples.lifespan_comparison:app_con_lifespan --reload
```

**Qué hace:**
- Muestra dos implementaciones lado a lado
- Anti-patrón vs patrón correcto
- Comentarios explicativos
- Endpoints de ejemplo

---

## 🗺️ Mapa de Aprendizaje

```
NIVEL 1: Básico (30 min)
│
├─ 📋 Cheat_Sheet_ES.md (5 min)
│   └─ Conceptos clave + código básico
│
├─ 🧪 test_lifespan.py (10 min)
│   └─ Ejecutar y ver en acción
│
└─ 📖 Lifespan_Explained_ES.md (15 min)
    └─ Entender los conceptos

NIVEL 2: Intermedio (30 min)
│
├─ 🎨 Flujo_Visual_ES.md (10 min)
│   └─ Visualizar el flujo completo
│
└─ 💻 lifespan_comparison.py (20 min)
    └─ Código real comparativo

NIVEL 3: Avanzado (45 min)
│
└─ 📚 Database_Best_Practices.md (45 min)
    └─ Patrones profesionales + optimización
```

---

## 🎯 Rutas de Aprendizaje

### 🏃 Rápido (15 min)
Si solo tienes 15 minutos:
1. Lee **Cheat_Sheet_ES.md**
2. Ejecuta **test_lifespan.py**
3. Mira tu código en `app/core/lifespan.py`

### 🚶 Normal (1 hora)
Si tienes una hora:
1. Lee **Lifespan_Explained_ES.md** (20 min)
2. Ve **Flujo_Visual_ES.md** (10 min)
3. Ejecuta **test_lifespan.py** (10 min)
4. Estudia **lifespan_comparison.py** (20 min)

### 🧗 Completo (2 horas)
Si quieres dominarlo:
1. Lee **Lifespan_Explained_ES.md** (20 min)
2. Ve **Flujo_Visual_ES.md** (10 min)
3. Ejecuta **test_lifespan.py** (10 min)
4. Estudia **lifespan_comparison.py** (20 min)
5. Lee **Database_Best_Practices.md** (45 min)
6. Experimenta con tu código (15 min)

---

## 🔍 Buscar Información Específica

| Quiero saber... | Ir a... |
|----------------|---------|
| ¿Qué es lifespan? | Lifespan_Explained_ES.md → Sección "¿Qué es Lifespan?" |
| ¿Cómo funciona? | Flujo_Visual_ES.md → Diagrama completo |
| ¿Código de ejemplo? | lifespan_comparison.py |
| ¿Está bien mi código? | Cheat_Sheet_ES.md → Checklist |
| ¿Cómo probar? | test_lifespan.py |
| ¿Best practices? | Database_Best_Practices.md |
| ¿FAQ? | Cheat_Sheet_ES.md → Preguntas Frecuentes |

---

## 🎓 Conceptos Clave

### Lifespan
```python
@asynccontextmanager
async def lifespan(app):
    # STARTUP - una vez
    recurso = crear_recurso()
    yield
    # SHUTDOWN - una vez
    recurso.cerrar()
```

### Dependency Injection
```python
async def get_session():
    adapter = obtener_compartido()
    async with adapter.get_session() as session:
        yield session
```

### Relación
```
Lifespan (1x)
    ↓ crea
Adapter (compartido)
    ↓ usa
Dependency (Nx)
    ↓ crea
Session (temporal)
    ↓ usa
Endpoint
```

---

## ✅ Tu Implementación

Tu código ya está correcto:

```
app/
├─ core/
│  └─ lifespan.py ✅
│     └─ Define lifespan + adapter compartido
├─ main.py ✅
│  └─ app = FastAPI(lifespan=lifespan)
└─ shared/
   └─ dependencies/
      └─ sql.py ✅
         └─ get_async_session_dependency()
```

**No necesitas cambiar nada en tus endpoints.** 🎉

---

## 🚀 Comandos Útiles

```bash
# Ver tu implementación actual
$ cat app/core/lifespan.py
$ cat app/main.py
$ cat app/shared/dependencies/sql.py

# Ejecutar tutoriales
$ uv run python examples/test_lifespan.py

# Ejecutar tu app y ver los logs
$ uv run fastapi dev app/main.py

# Hacer un request de prueba
$ curl http://localhost:8000/api/v1/restaurants
```

---

## 📞 Resumen

1. **Lifespan** = Startup + Shutdown (1 vez cada uno)
2. **Dependency** = Por request (muchas veces)
3. **Tu app** = Ya usa este patrón correctamente ✅

**La magia está en:**
- Crear recursos pesados una sola vez (lifespan)
- Reutilizarlos muchas veces (dependency)
- Limpiar automáticamente (shutdown)

---

## 🎯 Siguiente Paso

```bash
# 1. Lee el cheat sheet (5 min)
$ cat docs/code/Cheat_Sheet_ES.md

# 2. Ejecuta el tutorial (10 min)
$ uv run python examples/test_lifespan.py

# 3. Ve tu app funcionando (5 min)
$ uv run fastapi dev app/main.py
```

**Total: 20 minutos para entender completamente.** ⏱️

---

¡Tu implementación ya está siguiendo las mejores prácticas! 🎉

