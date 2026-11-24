"""Verifica importaciones minimas de FastAPI y cliente HTTP (Bloque 35.1)."""

import fastapi
import httpx
import pydantic
import uvicorn

print(
    f"fastapi={fastapi.__version__} uvicorn={uvicorn.__version__} "
    f"pydantic={pydantic.__version__} httpx={httpx.__version__}"
)
print("Importaciones correctas")
