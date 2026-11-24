"""Seleccion de modelo y mecanismo de respaldo explicito (Bloque 41)."""

from servicio import config
from servicio.errores import ModeloNoDisponibleError
from servicio.modelo import ModeloGemini, ModeloSimulado


def estado_respaldo() -> tuple[str, bool]:
    """Retorna (modo_efectivo, respaldo_activo) sin fallar al consultar /salud."""
    solicitado = config.modelo_solicitado()
    if solicitado == "simulado":
        return "simulado", False
    if config.modelo_configurado():
        return "real", False
    if config.permitir_respaldo():
        return "respaldo", True
    return "real_sin_clave", False


def elegir_modelo():
    """Retorna (instancia_modelo, modo_modelo, advertencia_respaldo).

    Si MODELO=real y falta GEMINI_API_KEY:
    - Con PERMITIR_RESPALDO=1 -> usa ModeloSimulado y declara respaldo visiblemente.
    - Sin PERMITIR_RESPALDO=1 -> lanza ModeloNoDisponibleError (HTTP 503 honesto).
    """
    solicitado = config.modelo_solicitado()
    if solicitado == "simulado":
        return ModeloSimulado(), "simulado", None

    if config.modelo_configurado():
        return ModeloGemini(config.clave_modelo()), "real", None

    if config.permitir_respaldo():
        return (
            ModeloSimulado(),
            "respaldo",
            "Modelo real sin credencial: respuesta generada con componente de respaldo declarado.",
        )

    raise ModeloNoDisponibleError(
        "El modelo real (MODELO=real) no esta disponible porque falta GEMINI_API_KEY "
        "y PERMITIR_RESPALDO no esta habilitado."
    )
