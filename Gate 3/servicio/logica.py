"""Fachada de logica de negocio sin acoplamiento a HTTP (Bloque 35.3)."""

from servicio import cadena, catalogo, config, respaldo


def estado_salud() -> dict:
    modo_activo, respaldo_activo = respaldo.estado_respaldo()
    return {
        "estado": "ok",
        "entorno": config.entorno(),
        "modelo": "configurado" if config.modelo_configurado() else "sin clave",
        "modelo_activo": modo_activo,
        "respaldo_activo": respaldo_activo,
    }


def responder_consulta(pregunta: str) -> dict:
    return cadena.ejecutar(pregunta)


def auditar_precio(codigo_onu: str, precio_ofertado: float) -> dict | None:
    return catalogo.evaluar_precio(codigo_onu, precio_ofertado)


def obtener_licitacion(licitacion_id: str) -> dict | None:
    return catalogo.consultar_licitacion(licitacion_id)
