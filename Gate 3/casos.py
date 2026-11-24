"""Tabla compartida de casos validos e invalidos para pytest y cliente HTTP externo (Bloque 36.3)."""

CASOS = [
    # Casos validos (V-01..V-04)
    {
        "id": "V-01",
        "descripcion": "Healthcheck operativo sin exposicion de claves",
        "metodo": "GET",
        "ruta": "/salud",
        "estado": 200,
        "contiene": '"estado":"ok"',
    },
    {
        "id": "V-02",
        "descripcion": "Consulta RAG de precio de referencia Paracetamol (CA-01)",
        "metodo": "POST",
        "ruta": "/consultas",
        "json": {"pregunta": "Cual es el precio de referencia del Paracetamol 500 mg?"},
        "estado": 200,
        "contiene": "cenabast_catalogo_precios_referencia_2026.md",
    },
    {
        "id": "V-03",
        "descripcion": "Consulta fuera del corpus CENABAST sin fuentes (CA-02)",
        "metodo": "POST",
        "ruta": "/consultas",
        "json": {"pregunta": "Cual es la temperatura en Marte hoy?"},
        "estado": 200,
        "contiene": "No encuentro esa informacion",
    },
    {
        "id": "V-04",
        "descripcion": "Auditoria de sobreprecio critico Paracetamol +50% (CA-03)",
        "metodo": "POST",
        "ruta": "/precios/evaluar",
        "json": {"codigo_onu": "51181504", "precio_ofertado": 33.6},
        "estado": 200,
        "contiene": "SOBREPRECIO_CRITICO",
    },
    {
        "id": "V-05",
        "descripcion": "Consulta de expediente historico LIC-723 (CA-04)",
        "metodo": "GET",
        "ruta": "/licitaciones/LIC-723",
        "estado": 200,
        "contiene": "RECHAZAR",
    },
    # Casos invalidos (I-01..I-07: cubren 404, 405 y 422)
    {
        "id": "I-01",
        "descripcion": "Pregunta vacia o solo espacios rechazada con 422",
        "metodo": "POST",
        "ruta": "/consultas",
        "json": {"pregunta": "   "},
        "estado": 422,
        "contiene": '"codigo":"entrada_invalida"',
    },
    {
        "id": "I-02",
        "descripcion": "Cuerpo JSON malformado rechazado con 422 uniforme",
        "metodo": "POST",
        "ruta": "/consultas",
        "contenido": "{pregunta: sin comillas",
        "estado": 422,
        "contiene": '"codigo":"entrada_invalida"',
    },
    {
        "id": "I-03",
        "descripcion": "Precio ofertado negativo rechazado con 422",
        "metodo": "POST",
        "ruta": "/precios/evaluar",
        "json": {"codigo_onu": "51181504", "precio_ofertado": -10.0},
        "estado": 422,
        "contiene": '"codigo":"entrada_invalida"',
    },
    {
        "id": "I-04",
        "descripcion": "Formato invalido de identificador de licitacion (422)",
        "metodo": "GET",
        "ruta": "/licitaciones/INVALIDO-1",
        "estado": 422,
        "contiene": '"codigo":"entrada_invalida"',
    },
    {
        "id": "I-05",
        "descripcion": "Licitacion inexistente con formato valido retorna 404 uniforme (CA-04)",
        "metodo": "GET",
        "ruta": "/licitaciones/LIC-999",
        "estado": 404,
        "contiene": '"codigo":"no_encontrado"',
    },
    {
        "id": "I-06",
        "descripcion": "Medicamento inexistente en catalogo 2026 retorna 404 uniforme",
        "metodo": "POST",
        "ruta": "/precios/evaluar",
        "json": {"codigo_onu": "51999999", "precio_ofertado": 100.0},
        "estado": 404,
        "contiene": '"codigo":"no_encontrado"',
    },
    {
        "id": "I-07",
        "descripcion": "Metodo HTTP no permitido sobre /consultas retorna 405 uniforme",
        "metodo": "DELETE",
        "ruta": "/consultas",
        "estado": 405,
        "contiene": '"codigo":"metodo_no_permitido"',
    },
]


def ejecutar_caso(cliente, caso: dict) -> tuple[bool, int, str]:
    kwargs: dict = {}
    if "json" in caso:
        kwargs["json"] = caso["json"]
    elif "contenido" in caso:
        kwargs["content"] = caso["contenido"]
        kwargs["headers"] = {"Content-Type": "application/json"}

    r = cliente.request(caso["metodo"], caso["ruta"], **kwargs)
    cuerpo_compacto = r.text.replace(": ", ":")
    ok = r.status_code == caso["estado"] and (
        caso["contiene"] in r.text or caso["contiene"] in cuerpo_compacto
    )
    return ok, r.status_code, r.text
