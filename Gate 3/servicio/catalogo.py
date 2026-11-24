"""Logica pura de dominio para catalogo de precios y precedentes CENABAST (RF-02 y RF-03)."""

from servicio import config

FUENTE_CATALOGO = "cenabast_catalogo_precios_referencia_2026.md"
FUENTE_HISTORIAL = "cenabast_historial_licitaciones_hospitalarias.md"

CATALOGO_2026 = {
    "51181504": {"medicamento": "PARACETAMOL 500 MG", "precio_referencia": 22.40},
    "51101512": {"medicamento": "CEFTRIAXONA 1 G", "precio_referencia": 1250.00},
    "51141708": {"medicamento": "LOSARTAN POTASICO 50 MG", "precio_referencia": 18.50},
    "51101506": {"medicamento": "AMOXICILINA 500 MG", "precio_referencia": 45.00},
    "51181702": {"medicamento": "INSULINA HUMANA NPH 100 UI/ML", "precio_referencia": 3800.00},
}

LICITACIONES_HISTORICAS = {
    "LIC-723": {
        "licitacion_id": "LIC-723",
        "expediente_oficial": "723-14-LP24",
        "medicamento": "Paracetamol 500 mg comprimido oral",
        "proveedor": "Proveedor A",
        "precio_ofertado": 33.60,
        "precio_referencia": 22.40,
        "desviacion_pct": 50.0,
        "estado": "RECHAZAR",
        "dictamen": "Sobreprecio critico (+50.0%): vulnera umbral maximo (+15%). Se declaro desierto y se adjudico en $21.90 CLP.",
        "fuente": FUENTE_HISTORIAL,
    },
    "LIC-812": {
        "licitacion_id": "LIC-812",
        "expediente_oficial": "812-05-LR25",
        "medicamento": "Ceftriaxona 1 g polvo para solucion inyectable IV/IM",
        "proveedor": "Laboratorio Biosano",
        "precio_ofertado": 1290.00,
        "precio_referencia": 1250.00,
        "desviacion_pct": 3.2,
        "estado": "ADJUDICAR",
        "dictamen": "Desviacion dentro de margen competitivo aceptable (<= 5.0%), stock inmediato y certificacion ISP vigente.",
        "fuente": FUENTE_HISTORIAL,
    },
    "LIC-650": {
        "licitacion_id": "LIC-650",
        "expediente_oficial": "650-18-LP25",
        "medicamento": "Losartan potasico 50 mg comprimido recubierto",
        "proveedor": "Drogueria Andina",
        "precio_ofertado": 20.20,
        "precio_referencia": 18.50,
        "desviacion_pct": 9.19,
        "estado": "NEGOCIAR",
        "dictamen": "Rango de negociacion obligatoria (5.0% a 15.0%). Tras contraoferta a $18.90 CLP (+2.16%), se adjudico 50% de cuota.",
        "fuente": FUENTE_HISTORIAL,
    },
    "LIC-904": {
        "licitacion_id": "LIC-904",
        "expediente_oficial": "904-22-LR25",
        "medicamento": "Insulina humana NPH 100 UI/ml frasco ampolla 10 ml",
        "proveedor": "Distribuidora Sur Farma",
        "precio_ofertado": 4500.00,
        "precio_referencia": 3800.00,
        "desviacion_pct": 18.42,
        "estado": "SUPERVISION_HUMANA",
        "dictamen": "Rechazo preventivo y supervision humana por superar el 15%. Se convoco compra directa a precio internacional.",
        "fuente": FUENTE_HISTORIAL,
    },
    "LIC-501": {
        "licitacion_id": "LIC-501",
        "expediente_oficial": "501-11-LP24",
        "medicamento": "Amoxicilina 500 mg capsulas",
        "proveedor": "Proveedor Nuevo",
        "precio_ofertado": 25.00,
        "precio_referencia": 45.00,
        "desviacion_pct": -44.44,
        "estado": "REVISION_COSTOS",
        "dictamen": "Oferta temeraria (< -35.0%). Se exigio estructura de costos y poliza de fiel cumplimiento del 30%.",
        "fuente": FUENTE_HISTORIAL,
    },
}


def evaluar_precio(codigo_onu: str, precio_ofertado: float) -> dict | None:
    item = CATALOGO_2026.get(codigo_onu)
    if item is None:
        return None

    ref = item["precio_referencia"]
    desviacion = round(((precio_ofertado - ref) / ref) * 100.0, 2)
    umbral_critico = config.umbral_sobreprecio_pct()

    if desviacion < -35.0:
        categoria = "TEMERARIO"
        requiere_supervision = True
        recomendacion = "Solicitar estructura de costos y garantia de sostenibilidad antes de adjudicar."
    elif desviacion <= 5.0:
        categoria = "COMPETITIVO"
        requiere_supervision = False
        recomendacion = "Oferta competitiva dentro de rango (<= 5.0%): susceptible de adjudicacion estandar."
    elif desviacion <= umbral_critico:
        categoria = "NEGOCIACION"
        requiere_supervision = False
        recomendacion = f"Rango de negociacion obligatoria (5.0% a {umbral_critico:.1f}%): solicitar contraoferta."
    else:
        categoria = "SOBREPRECIO_CRITICO"
        requiere_supervision = True
        recomendacion = (
            f"Sobreprecio critico (> {umbral_critico:.1f}%): prohibida adjudicacion automatica; "
            "activar supervision humana de Jefatura de Adquisiciones."
        )

    return {
        "codigo_onu": codigo_onu,
        "medicamento": item["medicamento"],
        "precio_referencia": ref,
        "precio_ofertado": precio_ofertado,
        "desviacion_pct": desviacion,
        "categoria": categoria,
        "requiere_supervision": requiere_supervision,
        "recomendacion": recomendacion,
        "fuente": FUENTE_CATALOGO,
    }


def consultar_licitacion(licitacion_id: str) -> dict | None:
    return LICITACIONES_HISTORICAS.get(licitacion_id)
