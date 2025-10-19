# Descubre Boyacá Backend

Backend API para la plataforma Descubre Boyacá.

## Tecnologías

- **Python 3.14** - Última versión con mejoras de performance
- **FastAPI** - Framework web moderno y rápido
- **uv** - Gestor de paquetes y entornos virtuales ultrarrápido
- **Pydantic** - Validación de datos
- **Ruff** - Linter y formateador

## Requisitos

- Python 3.14+
- uv (gestor de paquetes)

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/wtoloza-dev/descubreboyaca-backend.git
cd descubreboyaca-backend

# Instalar dependencias
uv sync --all-extras

# Activar el entorno virtual
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate  # Windows
```

## Desarrollo

```bash
# Ejecutar el servidor de desarrollo
uv run fastapi dev app/main.py

# Ejecutar tests
uv run pytest

# Linting
uv run ruff check .

# Formatear código
uv run ruff format .
```

## Estructura del Proyecto

```
app/
├── core/           # Configuración y utilidades
├── clients/        # Clientes externos
├── domains/        # Dominios de negocio (DDD)
│   └── restaurants/
│       ├── entities/
│       ├── models/
│       ├── schemas/
│       ├── services/
│       ├── interfaces/
│       ├── repositories/
│       ├── dependencies/
│       └── routes/
└── main.py         # Entry point
```

## API Documentation

Una vez ejecutado el servidor, la documentación estará disponible en:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Licencia

Proprietary - Ver LICENSE para más detalles.

