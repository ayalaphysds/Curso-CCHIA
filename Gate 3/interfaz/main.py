"""Servicio Interfaz Web / BFF desacoplado que consume la API CENABAST por HTTP (Bloque 38.2)."""

import os
import httpx
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(
    title="Interfaz Web de Auditoria CENABAST",
    version="1.0.0",
    description="Gateway web liviano que consulta la API FastAPI CENABAST mediante la red interna de Compose.",
)


def obtener_api_url() -> str:
    return os.environ.get("API_URL", "http://127.0.0.1:8000").rstrip("/")


@app.get("/salud")
def salud() -> dict:
    return {"estado": "ok", "servicio": "interfaz", "api_url": obtener_api_url()}


@app.get("/", response_class=HTMLResponse)
def portada() -> str:
    return """<!doctype html>
<html lang="es">
<head><meta charset="utf-8"><title>Auditoria CENABAST — Gate 3</title></head>
<body style="font-family: system-ui, sans-serif; max-width: 780px; margin: 2rem auto; line-height: 1.5;">
  <h1>Plataforma de Auditoria de Precios y Licitaciones CENABAST</h1>
  <p>Consulta el corpus normativo CENABAST a traves del gateway <code>/preguntar?texto=...</code>.</p>
  <form action="/preguntar" method="get">
    <input name="texto" style="width: 75%; padding: 0.5rem;" placeholder="Cual es el precio de referencia del Paracetamol 500 mg?" required>
    <button type="submit" style="padding: 0.5rem 1rem;">Consultar</button>
  </form>
</body>
</html>"""


@app.get("/preguntar")
def preguntar(texto: str = Query(min_length=3, max_length=500)):
    url = f"{obtener_api_url()}/consultas"
    try:
        r = httpx.post(url, json={"pregunta": texto}, timeout=5.0)
        return JSONResponse(status_code=r.status_code, content=r.json())
    except (httpx.HTTPError, OSError):
        return JSONResponse(
            status_code=502,
            content={
                "codigo": "api_no_disponible",
                "mensaje": "No fue posible contactar a la API principal CENABAST.",
            },
        )


@app.get("/licitacion/{licitacion_id}")
def licitacion(licitacion_id: str):
    url = f"{obtener_api_url()}/licitaciones/{licitacion_id}"
    try:
        r = httpx.get(url, timeout=5.0)
        return JSONResponse(status_code=r.status_code, content=r.json())
    except (httpx.HTTPError, OSError):
        return JSONResponse(
            status_code=502,
            content={
                "codigo": "api_no_disponible",
                "mensaje": "No fue posible contactar a la API principal CENABAST.",
            },
        )
