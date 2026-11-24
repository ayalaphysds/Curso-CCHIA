"""Ejemplos ejecutables de la API para generar y verificar docs/api.md (Bloque 45.1)."""

EJEMPLOS = [
    {
        "id": "API-01",
        "titulo": "Estado operativo del servicio",
        "metodo": "GET",
        "ruta": "/salud",
        "estado": 200,
    },
    {
        "id": "API-02",
        "titulo": "Consulta normativa de precio de referencia (Paracetamol 500 mg)",
        "metodo": "POST",
        "ruta": "/consultas",
        "json": {"pregunta": "Cual es el precio de referencia del Paracetamol 500 mg?"},
        "estado": 200,
    },
    {
        "id": "API-03",
        "titulo": "Consulta fuera del corpus oficial (abstencion honesta)",
        "metodo": "POST",
        "ruta": "/consultas",
        "json": {"pregunta": "Cual es la temperatura en Marte hoy?"},
        "estado": 200,
    },
    {
        "id": "API-04",
        "titulo": "Evaluacion determinista de sobreprecio critico (+50%)",
        "metodo": "POST",
        "ruta": "/precios/evaluar",
        "json": {"codigo_onu": "51181504", "precio_ofertado": 33.6},
        "estado": 200,
    },
    {
        "id": "API-05",
        "titulo": "Consulta de expediente precedente de licitacion (LIC-723)",
        "metodo": "GET",
        "ruta": "/licitaciones/LIC-723",
        "estado": 200,
    },
    {
        "id": "API-06",
        "titulo": "Error uniforme 404 para expediente inexistente (LIC-999)",
        "metodo": "GET",
        "ruta": "/licitaciones/LIC-999",
        "estado": 404,
    },
]
