"""
Enrutamiento Condicional y Manejo Robusto de Errores por Paso (Bloque 19 y 20, U2.3).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Orquestación de Consultas de Adquisiciones

Componentes:
1. Enrutador condicional basado en la intención de la consulta:
   - Ruta 'catalogo': Precios oficiales y especificaciones técnicas de medicamentos.
   - Ruta 'sobreprecio': Auditoría de ofertas y cálculo de desvío porcentual.
   - Ruta 'abastecimiento': Gestión de multas, stock crítico y logística hospitalaria.
   - Ruta por defecto: Consultas administrativas generales.
2. Mecanismo de contingencia (fallbacks) por rama especializada.
3. Función envolvente de ejecución segura 'procesar_mensaje_seguro' para contención total de fallas.
"""

import os
import sys
import logging
from typing import Dict, Any, Callable
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

from langchain_core.runnables import (
    RunnableLambda,
    RunnableBranch,
    RunnableWithFallbacks,
)
from cadena_tres_pasos import CATALOGO_PRECIOS, paso_1_clasificar


# Configuración básica de logging
logger = logging.getLogger("enrutamiento_cenabast")


def ruta_catalogo(datos: Dict[str, Any]) -> Dict[str, Any]:
    """Rama especializada para consultas de catálogo de precios de referencia."""
    farmaco = datos.get("farmaco")
    if farmaco and farmaco in CATALOGO_PRECIOS:
        precio = CATALOGO_PRECIOS[farmaco]
        texto = f"[RUTA CATÁLOGO] El precio de referencia de {farmaco.capitalize()} en el Catálogo 2026 es ${precio:.2f} CLP."
    else:
        texto = "[RUTA CATÁLOGO] Consulta general de catálogo. Consulte data/cenabast_catalogo_precios_referencia_2026.md."
    return {
        "ruta_ejecutada": "catalogo",
        "exito": True,
        "respuesta": texto,
        "datos": datos,
    }


def ruta_sobreprecio(datos: Dict[str, Any]) -> Dict[str, Any]:
    """Rama especializada para auditoría de ofertas y cálculo de sobreprecio."""
    farmaco = datos.get("farmaco")
    consulta = datos.get("consulta_original", "")
    import re
    numeros = re.findall(r"\b\d+(?:\.\d+)?\b", consulta)
    precio_ofertado = None
    for n in numeros:
        val = float(n)
        if val not in [500.0, 50.0, 1.0, 100.0, 2026.0]:
            precio_ofertado = val
            break

    if farmaco and precio_ofertado and farmaco in CATALOGO_PRECIOS:
        ref = CATALOGO_PRECIOS[farmaco]
        desviacion = ((precio_ofertado - ref) / ref) * 100
        if desviacion <= 5.0:
            dictamen = "Adjudicación recomendada (rango competitivo <= 5%)."
        elif desviacion <= 15.0:
            dictamen = "Negociación obligatoria requerida (desviación entre 5% y 15%)."
        else:
            dictamen = "Rechazo por sobreprecio crítico (> 15%). Requiere supervisión humana."

        texto = (
            f"[RUTA SOBREPRECIO] Auditoría {farmaco.capitalize()}: Oferta ${precio_ofertado} CLP vs "
            f"Referencia ${ref} CLP (Desviación: {desviacion:+.2f}%). Dictamen: {dictamen}"
        )
    else:
        texto = "[RUTA SOBREPRECIO] Debe proporcionar el fármaco y el precio ofertado para auditar la desviación."

    return {
        "ruta_ejecutada": "sobreprecio",
        "exito": True,
        "respuesta": texto,
        "datos": datos,
    }


def ruta_abastecimiento(datos: Dict[str, Any]) -> Dict[str, Any]:
    """Rama especializada para políticas de riesgo, multas y logística de abastecimiento."""
    texto = (
        "[RUTA ABASTECIMIENTO] Normativa CENABAST: Multa por atraso es del 1.0% diario (tope 15%). "
        "Rescisión contractual a los 15 días corridos. Nivel de cumplimiento exigido (INCL) >= 85%."
    )
    return {
        "ruta_ejecutada": "abastecimiento",
        "exito": True,
        "respuesta": texto,
        "datos": datos,
    }


def ruta_general(datos: Dict[str, Any]) -> Dict[str, Any]:
    """Ruta por defecto para consultas no clasificadas."""
    return {
        "ruta_ejecutada": "general",
        "exito": True,
        "respuesta": "[RUTA GENERAL] Requerimiento no clasificado. Se sugiere consultar bases de licitación o catálogo.",
        "datos": datos,
    }


def fallback_seguridad(datos: Dict[str, Any]) -> Dict[str, Any]:
    """Ruta de respaldo (fallback) activada ante excepciones en una rama especializada."""
    return {
        "ruta_ejecutada": "fallback_seguridad",
        "exito": False,
        "respuesta": "[CONTINGENCIA ACTIVADA] Se produjo un error al procesar la rama especializada. Respuesta de contingencia segura emitida.",
        "datos": datos,
    }


def construir_enrutador_con_fallbacks():
    """
    Construye el enrutador condicional LangChain con manejo de ramas y fallbacks integrados.
    """
    # Envolver ramas que puedan fallar con fallbacks
    rama_cat_segura = RunnableLambda(ruta_catalogo).with_fallbacks([RunnableLambda(fallback_seguridad)])
    rama_sob_segura = RunnableLambda(ruta_sobreprecio).with_fallbacks([RunnableLambda(fallback_seguridad)])
    rama_aba_segura = RunnableLambda(ruta_abastecimiento).with_fallbacks([RunnableLambda(fallback_seguridad)])
    rama_gen_segura = RunnableLambda(ruta_general)

    # Rama condicional basada en 'categoria'
    enrutador = RunnableBranch(
        (lambda d: d.get("categoria") == "catalogo", rama_cat_segura),
        (lambda d: d.get("categoria") == "sobreprecio", rama_sob_segura),
        (lambda d: d.get("categoria") == "abastecimiento", rama_aba_segura),
        rama_gen_segura,
    )

    # Pipeline completo: clasificación preliminar -> bifurcación condicional
    flujo_completo = RunnableLambda(paso_1_clasificar) | enrutador
    return flujo_completo


def procesar_mensaje_seguro(mensaje: str) -> Dict[str, Any]:
    """
    Envoltorio de ejecución segura (Bloque 20, U2.3).
    Garantiza que ninguna excepción no controlada interrumpa el servicio.
    
    Parámetros:
        mensaje: Texto de la consulta de compras públicas.
        
    Retorna:
        Dict estructurado con:
        - "estado": "ok" o "error_contenido"
        - "ruta_ejecutada": Nombre de la ruta o "fallback_general"
        - "respuesta": Mensaje procesado o texto de contingencia amigable
        - "error": Descripción del error si ocurrió, None en caso contrario
    """
    if not isinstance(mensaje, str) or not mensaje.strip():
        return {
            "estado": "error_contenido",
            "ruta_ejecutada": "validacion_entrada",
            "respuesta": "La consulta no puede estar vacía. Por favor ingrese una consulta válida sobre compras CENABAST.",
            "error": "Consulta vacía o tipo inválido",
        }

    try:
        orquestador = construir_enrutador_con_fallbacks()
        resultado = orquestador.invoke(mensaje)
        return {
            "estado": "ok",
            "ruta_ejecutada": resultado.get("ruta_ejecutada", "desconocida"),
            "respuesta": resultado.get("respuesta", ""),
            "error": None,
        }
    except Exception as err:
        logger.error(f"Falla interceptada en procesar_mensaje_seguro: {err}")
        return {
            "estado": "error_contenido",
            "ruta_ejecutada": "fallback_general",
            "respuesta": "No fue posible procesar la consulta por un error interno temporal. El servicio continúa operativo.",
            "error": str(err),
        }


if __name__ == "__main__":
    print("Demostración de Enrutamiento y Manejo de Errores (Bloque 19-20):")
    pruebas = [
        "¿Cuál es el precio de catálogo de Paracetamol?",
        "Evaluar sobreprecio de Losartán ofertado a 20.20 CLP",
        "¿Cuáles son las sanciones por atraso en abastecimiento?",
        "Consulta general sobre el proceso de compras",
        "",  # Consulta inválida para verificar contención de errores
    ]
    for p in pruebas:
        r = procesar_mensaje_seguro(p)
        print(f"\nMensaje: '{p}'")
        print(f"  Estado: {r['estado']} | Ruta: {r['ruta_ejecutada']}")
        print(f"  Salida: {r['respuesta']}")
