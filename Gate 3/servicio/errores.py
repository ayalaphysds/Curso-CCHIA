"""Contrato uniforme de errores HTTP para FastAPI (Bloque 36.1)."""

import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from servicio.esquemas import ErrorRespuesta

logger = logging.getLogger("servicio.errores")

CODIGOS = {
    400: "peticion_invalida",
    404: "no_encontrado",
    405: "metodo_no_permitido",
    503: "modelo_no_disponible",
}

ERRORES = {
    404: {"model": ErrorRespuesta, "description": "Recurso solicitado no encontrado."},
    405: {"model": ErrorRespuesta, "description": "Metodo HTTP no permitido para esta ruta."},
    422: {"model": ErrorRespuesta, "description": "Entrada invalida segun esquema de validacion."},
    500: {"model": ErrorRespuesta, "description": "Error interno controlado sin exposicion de detalles."},
    503: {"model": ErrorRespuesta, "description": "Motor generativo no disponible sin respaldo habilitado."},
}


class ModeloNoDisponibleError(RuntimeError):
    """Se lanza cuando MODELO=real no tiene credencial y el respaldo no esta habilitado."""


def registrar(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def manejar_validacion(_request: Request, exc: RequestValidationError) -> JSONResponse:
        campos = []
        for err in exc.errors():
            loc = [str(x) for x in err.get("loc", ()) if x not in ("body",)]
            campo = ".".join(loc) if loc else "cuerpo"
            campos.append({"campo": campo, "problema": str(err.get("msg", "valor invalido"))})
        payload = ErrorRespuesta(
            codigo="entrada_invalida",
            mensaje="La peticion no cumple el formato esperado.",
            campos=campos,
        )
        return JSONResponse(status_code=422, content=payload.model_dump())

    @app.exception_handler(StarletteHTTPException)
    async def manejar_http(_request: Request, exc: StarletteHTTPException) -> JSONResponse:
        codigo = CODIGOS.get(exc.status_code, f"http_{exc.status_code}")
        payload = ErrorRespuesta(codigo=codigo, mensaje=str(exc.detail))
        return JSONResponse(status_code=exc.status_code, content=payload.model_dump(exclude_none=True))

    @app.exception_handler(ModeloNoDisponibleError)
    async def manejar_modelo_no_disponible(_request: Request, exc: ModeloNoDisponibleError) -> JSONResponse:
        payload = ErrorRespuesta(codigo="modelo_no_disponible", mensaje=str(exc))
        return JSONResponse(status_code=503, content=payload.model_dump(exclude_none=True))

    @app.exception_handler(Exception)
    async def manejar_inesperado(request: Request, exc: Exception) -> JSONResponse:
        logger.error(
            '{"evento":"error_interno","metodo":"%s","ruta":"%s","tipo":"%s"}',
            request.method,
            request.url.path,
            type(exc).__name__,
        )
        payload = ErrorRespuesta(codigo="error_interno", mensaje="Ocurrio un error inesperado.")
        return JSONResponse(status_code=500, content=payload.model_dump(exclude_none=True))
