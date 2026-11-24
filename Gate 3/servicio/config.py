"""Configuracion diferida por variables de entorno (Bloque 38.1).

Nunca lee credenciales al importar el modulo para que la aplicacion y las pruebas
puedan arrancar sin claves externas.
"""

import os


class ConfiguracionIncompleta(RuntimeError):
    """Error lanzado cuando falta una variable obligatoria en tiempo de ejecucion."""


def entorno() -> str:
    return os.environ.get("ENTORNO", "desarrollo").strip() or "desarrollo"


def modelo_solicitado() -> str:
    valor = os.environ.get("MODELO", "simulado").strip().lower()
    return valor if valor in ("simulado", "real") else "simulado"


def permitir_respaldo() -> bool:
    return os.environ.get("PERMITIR_RESPALDO", "0").strip().lower() in ("1", "true", "si")


def umbral_sobreprecio_pct() -> float:
    raw = os.environ.get("UMBRAL_SOBREPRECIO_PCT", "15.0").strip()
    try:
        valor = float(raw)
        return valor if valor > 0 else 15.0
    except ValueError:
        return 15.0


def modelo_configurado() -> bool:
    return bool(os.environ.get("GEMINI_API_KEY", "").strip())


def clave_modelo() -> str:
    clave = os.environ.get("GEMINI_API_KEY", "").strip()
    if not clave:
        raise ConfiguracionIncompleta(
            "GEMINI_API_KEY no esta definida. Configurala como variable de entorno para usar MODELO=real."
        )
    return clave
