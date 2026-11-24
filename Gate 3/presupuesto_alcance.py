"""Presupuesto de alcance para priorizar requerimientos del MVP (Bloque 33.2)."""

HORAS_DISPONIBLES = 24.0
RESERVA_CALIDAD_PCT = 0.30
MARGEN_IMPREVISTOS_PCT = 0.20

CAPAS_OBLIGATORIAS = {"rag", "api", "contenedor"}

FUNCIONALIDADES = [
    {"id": "RF-01", "nombre": "Consulta RAG normativa CENABAST con citas", "horas": 4.0, "prioridad": 1, "capa": "rag", "imprescindible": True},
    {"id": "RF-02", "nombre": "Evaluacion de sobreprecio por codigo ONU", "horas": 2.5, "prioridad": 1, "capa": "api", "imprescindible": True},
    {"id": "RF-03", "nombre": "Consulta de precedentes de licitaciones", "horas": 2.0, "prioridad": 1, "capa": "api", "imprescindible": True},
    {"id": "RF-04", "nombre": "Interfaz web desacoplada y Docker Compose", "horas": 3.5, "prioridad": 1, "capa": "contenedor", "imprescindible": True},
    {"id": "RF-05", "nombre": "Integracion directa firma Mercado Publico", "horas": 14.0, "prioridad": 2, "capa": "externa", "imprescindible": False},
    {"id": "RF-06", "nombre": "Pronostico macroeconomico de fletes 2027", "horas": 18.0, "prioridad": 3, "capa": "externa", "imprescindible": False},
]


def calcular_presupuesto() -> dict:
    horas_netas = round(HORAS_DISPONIBLES * (1.0 - RESERVA_CALIDAD_PCT - MARGEN_IMPREVISTOS_PCT), 2)
    imprescindibles = [f for f in FUNCIONALIDADES if f["imprescindible"]]
    horas_mvp = round(sum(f["horas"] for f in imprescindibles), 2)
    capas_cubiertas = {f["capa"] for f in imprescindibles}
    faltantes = sorted(CAPAS_OBLIGATORIAS - capas_cubiertas)
    return {
        "horas_disponibles": HORAS_DISPONIBLES,
        "horas_netas_construccion": horas_netas,
        "horas_mvp": horas_mvp,
        "cabe_en_presupuesto": horas_mvp <= horas_netas,
        "capas_obligatorias_sin_cubrir": faltantes,
    }


if __name__ == "__main__":
    res = calcular_presupuesto()
    print(f"Horas disponibles:          {res['horas_disponibles']} h")
    print(f"Horas netas construccion:   {res['horas_netas_construccion']} h")
    print(f"Horas MVP imprescindibles:  {res['horas_mvp']} h")
    print(f"Cabe en presupuesto:        {'SI' if res['cabe_en_presupuesto'] else 'NO'}")
    print(f"Capas obligatorias sin cubrir: {res['capas_obligatorias_sin_cubrir'] or 'ninguna'}")
