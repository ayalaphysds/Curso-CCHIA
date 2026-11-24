"""Matriz complementaria de casos modelo con limitacion de borde declarada (Bloque 42/43)."""

MATRIZ = [
    {
        "id": "MP-07",
        "tipo": "valido",
        "escenario": "Consulta de politica anti-concentracion (cupo maximo 45.0%)",
        "peticion": {
            "metodo": "POST",
            "ruta": "/consultas",
            "json": {"pregunta": "Cual es el cupo maximo de concentracion por proveedor en CENABAST?"},
        },
        "esperado": {
            "estado": 200,
            "contiene": ["45.0%", "cenabast_politica_abastecimiento_riesgo.md"],
            "fuentes": ["cenabast_politica_abastecimiento_riesgo.md"],
        },
        "cubre": ["RF-01"],
    },
    {
        "id": "MP-08",
        "tipo": "borde",
        "escenario": "Consulta con sinonimo coloquial ausente del corpus ('remedio para la fiebre')",
        "peticion": {
            "metodo": "POST",
            "ruta": "/consultas",
            "json": {"pregunta": "cuanto cuesta el remedio para la fiebre en el catalogo?"},
        },
        "esperado": {
            "estado": 200,
            "contiene": ["22.40"],
            "fuentes": ["cenabast_catalogo_precios_referencia_2026.md"],
        },
        "cubre": ["RF-01"],
        "hallazgo": {
            "clasificacion": "limitacion",
            "decision": "Aceptado como limitacion del recuperador lexico determinista (LIM-02); se exige principio activo oficial en la interfaz y se planifica expansion con embeddings densos en iteracion futura.",
        },
    },
]
