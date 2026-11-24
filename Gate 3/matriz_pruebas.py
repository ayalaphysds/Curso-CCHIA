"""Matriz de Pruebas oficial vinculada a docs/ficha_diseno_funcional.md (Bloque 42.3)."""

MATRIZ = [
    {
        "id": "MP-01",
        "tipo": "valido",
        "escenario": "Consulta normativa de precio de referencia Paracetamol 500 mg con cita",
        "peticion": {
            "metodo": "POST",
            "ruta": "/consultas",
            "json": {"pregunta": "Cual es el precio de referencia del Paracetamol 500 mg?"},
        },
        "esperado": {
            "estado": 200,
            "contiene": ["22.40", "cenabast_catalogo_precios_referencia_2026.md"],
            "fuentes": ["cenabast_catalogo_precios_referencia_2026.md"],
        },
        "cubre": ["RF-01", "CA-01", "RNF-01"],
    },
    {
        "id": "MP-02",
        "tipo": "valido",
        "escenario": "Evaluacion de sobreprecio critico (+50%) activa bandera de supervision humana",
        "peticion": {
            "metodo": "POST",
            "ruta": "/precios/evaluar",
            "json": {"codigo_onu": "51181504", "precio_ofertado": 33.6},
        },
        "esperado": {
            "estado": 200,
            "contiene": ["SOBREPRECIO_CRITICO", '"requiere_supervision":true'],
        },
        "cubre": ["RF-02", "CA-03"],
    },
    {
        "id": "MP-03",
        "tipo": "valido",
        "escenario": "Consulta de expediente historico LIC-723 y contrato de salud para interfaz",
        "peticion": {
            "metodo": "GET",
            "ruta": "/licitaciones/LIC-723",
        },
        "esperado": {
            "estado": 200,
            "contiene": ["RECHAZAR", "Paracetamol"],
        },
        "cubre": ["RF-03", "RF-04", "CA-04", "CA-05"],
    },
    {
        "id": "MP-04",
        "tipo": "invalido",
        "escenario": "Pregunta solo con espacios rechazada con 422 y codigo uniforme entrada_invalida",
        "peticion": {
            "metodo": "POST",
            "ruta": "/consultas",
            "json": {"pregunta": "    "},
        },
        "esperado": {
            "estado": 422,
            "contiene": ['"codigo":"entrada_invalida"'],
            "no_contiene": ["Traceback", "GEMINI_API_KEY"],
        },
        "cubre": ["RNF-02", "CA-07"],
    },
    {
        "id": "MP-05",
        "tipo": "invalido",
        "escenario": "Expediente con formato valido inexistente devuelve 404 uniforme",
        "peticion": {
            "metodo": "GET",
            "ruta": "/licitaciones/LIC-999",
        },
        "esperado": {
            "estado": 404,
            "contiene": ['"codigo":"no_encontrado"'],
            "no_contiene": ["Traceback"],
        },
        "cubre": ["RF-03", "RNF-02", "CA-04"],
    },
    {
        "id": "MP-06",
        "tipo": "borde",
        "escenario": "Consulta fuera del corpus CENABAST se abstiene honestamente sin fuentes",
        "peticion": {
            "metodo": "POST",
            "ruta": "/consultas",
            "json": {"pregunta": "Cual es la temperatura en Marte hoy?"},
        },
        "esperado": {
            "estado": 200,
            "contiene": ["No encuentro esa informacion"],
            "fuentes": [],
        },
        "cubre": ["RF-01", "CA-02", "RNF-03"],
    },
]
