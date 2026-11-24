"""Aplicacion FastAPI principal — Servicio de Auditoria CENABAST (Bloques 35 y 36)."""

from typing import Annotated
from fastapi import FastAPI, HTTPException, Path as FastAPIPath

from servicio import errores, logica
from servicio.esquemas import (
    ConsultaRequest,
    ConsultaResponse,
    EvaluacionPrecioRequest,
    EvaluacionPrecioResponse,
    LicitacionResponse,
    SaludResponse,
)

app = FastAPI(
    title="API de Auditoria de Precios y Licitaciones CENABAST",
    version="1.0.0",
    description=(
        "Servicio generativo RAG y auditoria determinista de sobreprecios para adquisiciones "
        "publicas farmaceuticas de CENABAST (Especializacion IA Accenture — Gate 3 Capstone)."
    ),
)

errores.registrar(app)


@app.get(
    "/salud",
    response_model=SaludResponse,
    tags=["sistema"],
    summary="Verifica el estado operativo y configuracion del servicio",
    responses=errores.ERRORES,
)
def salud() -> dict:
    """Retorna estado del proceso, entorno activo y disponibilidad de clave sin exponer secretos."""
    return logica.estado_salud()


@app.post(
    "/consultas",
    response_model=ConsultaResponse,
    tags=["consultas"],
    summary="Consulta el corpus normativo CENABAST con citas verificadas",
    responses=errores.ERRORES,
)
def crear_consulta(entrada: ConsultaRequest) -> dict:
    """Ejecuta la cadena RAG de 4 capas (seguridad, recuperacion, generacion y fundamentacion)."""
    return logica.responder_consulta(entrada.pregunta)


@app.post(
    "/precios/evaluar",
    response_model=EvaluacionPrecioResponse,
    tags=["precios"],
    summary="Audita desviacion de precio unitario frente al catalogo CENABAST 2026",
    responses=errores.ERRORES,
)
def evaluar_precio(entrada: EvaluacionPrecioRequest) -> dict:
    """Clasifica una oferta en CLP segun umbrales BAS-CENABAST-2026-MED."""
    resultado = logica.auditar_precio(entrada.codigo_onu, entrada.precio_ofertado)
    if resultado is None:
        raise HTTPException(status_code=404, detail=f"Medicamento con codigo ONU {entrada.codigo_onu} no encontrado.")
    return resultado


@app.get(
    "/licitaciones/{licitacion_id}",
    response_model=LicitacionResponse,
    tags=["licitaciones"],
    summary="Consulta un expediente precedente de licitacion hospitalaria",
    responses=errores.ERRORES,
)
def obtener_licitacion(
    licitacion_id: Annotated[
        str,
        FastAPIPath(
            pattern=r"^LIC-\d{3}$",
            description="Identificador del expediente historico CENABAST (formato LIC-NNN).",
            examples=["LIC-723"],
        ),
    ],
) -> dict:
    """Retorna el dictamen historico de auditoria o error 404 uniforme si no existe."""
    expediente = logica.obtener_licitacion(licitacion_id)
    if expediente is None:
        raise HTTPException(status_code=404, detail=f"Licitacion {licitacion_id} no encontrada.")
    return expediente
