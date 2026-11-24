"""Esquemas Pydantic v2 tipados y documentados para OpenAPI (Bloques 35 y 36)."""

from pydantic import BaseModel, ConfigDict, Field


class CampoInvalido(BaseModel):
    campo: str = Field(description="Nombre o ruta del campo que incumple la regla de validacion.")
    problema: str = Field(description="Descripcion concisa de la regla incumplida.")


class ErrorRespuesta(BaseModel):
    codigo: str = Field(description="Codigo estable de error para consumo programatico.")
    mensaje: str = Field(description="Explicacion legible del error sin exponer detalles internos.")
    campos: list[CampoInvalido] | None = Field(
        default=None,
        description="Lista detallada de campos invalidos cuando el codigo es entrada_invalida.",
    )


class SaludResponse(BaseModel):
    estado: str = Field(description="Estado operativo del servicio HTTP (ok).")
    entorno: str = Field(description="Entorno de ejecucion activo (desarrollo, pruebas o produccion).")
    modelo: str = Field(description="Estado de disponibilidad de credencial externa (configurado o sin clave).")
    modelo_activo: str = Field(description="Modo efectivo del motor generativo (simulado, real o respaldo).")
    respaldo_activo: bool = Field(description="Indica si el servicio opera con respaldo declarado.")


class ConsultaRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    pregunta: str = Field(
        min_length=3,
        max_length=500,
        description="Pregunta en lenguaje natural sobre precios de referencia, bases o politicas CENABAST.",
        examples=["Cual es el precio de referencia del Paracetamol 500 mg?"],
    )


class ConsultaResponse(BaseModel):
    respuesta: str = Field(description="Respuesta generada y fundamentada con citas documentales [fuente: <archivo>].")
    fuentes: list[str] = Field(description="Lista de archivos oficiales del corpus CENABAST que respaldan la respuesta.")
    trace_id: str = Field(description="Identificador unico de trazabilidad para correlacion en logs estructurados.")
    modo_modelo: str = Field(description="Modo del modelo usado en la respuesta (simulado, real o respaldo).")
    advertencia_respaldo: str | None = Field(
        default=None,
        description="Aviso explicito cuando la consulta se atendio mediante componente de respaldo.",
    )


class EvaluacionPrecioRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    codigo_onu: str = Field(
        pattern=r"^51\d{6}$",
        description="Codigo ONU / Mercado Publico del medicamento esencial (8 digitos iniciando en 51).",
        examples=["51181504"],
    )
    precio_ofertado: float = Field(
        gt=0,
        le=10_000_000,
        description="Precio unitario neto ofertado por el proveedor en pesos chilenos (CLP).",
        examples=[33.6],
    )


class EvaluacionPrecioResponse(BaseModel):
    codigo_onu: str = Field(description="Codigo ONU del medicamento evaluado.")
    medicamento: str = Field(description="Principio activo y concentracion segun catalogo oficial 2026.")
    precio_referencia: float = Field(description="Mediana historica de referencia 2026 en CLP.")
    precio_ofertado: float = Field(description="Precio unitario neto ofertado en CLP.")
    desviacion_pct: float = Field(description="Desviacion porcentual respecto al precio de referencia.")
    categoria: str = Field(description="Clasificacion segun umbrales BAS-CENABAST-2026-MED.")
    requiere_supervision: bool = Field(description="Verdadero si exige aprobacion humana obligatoria (>15% o temeraria).")
    recomendacion: str = Field(description="Dictamen operativo sugerido para la comision evaluadora.")
    fuente: str = Field(description="Documento oficial que sustenta el precio de referencia y el umbral.")


class LicitacionResponse(BaseModel):
    licitacion_id: str = Field(description="Identificador corto del expediente precedente (formato LIC-NNN).")
    expediente_oficial: str = Field(description="Codigo oficial de licitacion en Mercado Publico.")
    medicamento: str = Field(description="Medicamento evaluado en el expediente historico.")
    proveedor: str = Field(description="Proveedor participante en el caso testigo.")
    precio_ofertado: float = Field(description="Precio unitario ofertado en CLP.")
    precio_referencia: float = Field(description="Mediana historica de referencia en CLP.")
    desviacion_pct: float = Field(description="Desviacion porcentual registrada en la auditoria.")
    estado: str = Field(description="Resolucion administrativa final del expediente.")
    dictamen: str = Field(description="Resumen del dictamen de auditoria hospitalaria.")
    fuente: str = Field(description="Archivo de jurisprudencia administrativa CENABAST.")
