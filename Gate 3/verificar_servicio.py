"""Verifica documentacion OpenAPI y criterios de aceptacion del servicio FastAPI (Bloque 35.3)."""

import sys
from fastapi.testclient import TestClient

from servicio.main import app


def main() -> int:
    cliente = TestClient(app, raise_server_exceptions=False)
    resultados: list[tuple[str, bool, str]] = []

    # DOC-1: /docs y /openapi.json accesibles con rutas clave
    r_docs = cliente.get("/docs")
    r_openapi = cliente.get("/openapi.json")
    rutas = set(r_openapi.json().get("paths", {}).keys()) if r_openapi.status_code == 200 else set()
    esperadas = {"/salud", "/consultas", "/precios/evaluar", "/licitaciones/{licitacion_id}"}
    ok_doc1 = r_docs.status_code == 200 and esperadas <= rutas
    resultados.append(("DOC-1", ok_doc1, f"/docs={r_docs.status_code}, rutas={sorted(rutas)}"))

    # DOC-2: todas las propiedades de los esquemas tienen description
    esquemas = r_openapi.json().get("components", {}).get("schemas", {}) if r_openapi.status_code == 200 else {}
    sin_desc = []
    for nombre, cuerpo in esquemas.items():
        if nombre in ("HTTPValidationError", "ValidationError"):
            continue
        for prop, meta in cuerpo.get("properties", {}).items():
            if not meta.get("description"):
                sin_desc.append(f"{nombre}.{prop}")
    resultados.append(("DOC-2", len(sin_desc) == 0, "todos los campos documentados" if not sin_desc else f"faltan: {sin_desc}"))

    # CA-01: consulta Paracetamol con cita
    r1 = cliente.post("/consultas", json={"pregunta": "Cual es el precio de referencia del Paracetamol 500 mg?"})
    d1 = r1.json() if r1.status_code == 200 else {}
    ok_ca1 = (
        r1.status_code == 200
        and "22.40" in d1.get("respuesta", "")
        and "cenabast_catalogo_precios_referencia_2026.md" in d1.get("fuentes", [])
    )
    resultados.append(("CA-01", ok_ca1, f"status={r1.status_code}, fuentes={d1.get('fuentes')}"))

    # CA-02: consulta fuera del corpus retorna abstencion sin fuentes
    r2 = cliente.post("/consultas", json={"pregunta": "Cual es la temperatura en Marte hoy?"})
    d2 = r2.json() if r2.status_code == 200 else {}
    ok_ca2 = (
        r2.status_code == 200
        and "No encuentro esa informacion" in d2.get("respuesta", "")
        and d2.get("fuentes") == []
    )
    resultados.append(("CA-02", ok_ca2, f"status={r2.status_code}, fuentes={d2.get('fuentes')}"))

    # CA-03: evaluacion de sobreprecio critico (+50%)
    r3 = cliente.post("/precios/evaluar", json={"codigo_onu": "51181504", "precio_ofertado": 33.6})
    d3 = r3.json() if r3.status_code == 200 else {}
    ok_ca3 = (
        r3.status_code == 200
        and d3.get("desviacion_pct") == 50.0
        and d3.get("categoria") == "SOBREPRECIO_CRITICO"
        and d3.get("requiere_supervision") is True
    )
    resultados.append(("CA-03", ok_ca3, f"status={r3.status_code}, categoria={d3.get('categoria')}"))

    # CA-04: precedente existente (200) e inexistente (404 uniforme)
    r4a = cliente.get("/licitaciones/LIC-723")
    r4b = cliente.get("/licitaciones/LIC-999")
    ok_ca4 = (
        r4a.status_code == 200
        and "RECHAZAR" in r4a.text
        and r4b.status_code == 404
        and '"codigo":"no_encontrado"' in r4b.text.replace(" ", "")
    )
    resultados.append(("CA-04", ok_ca4, f"LIC-723={r4a.status_code}, LIC-999={r4b.status_code}"))

    cumplidas = 0
    for cid, ok, detalle in resultados:
        etiqueta = "PASA" if ok else "FALLA"
        if ok:
            cumplidas += 1
        print(f"{etiqueta} {cid}: {detalle}")

    print(f"{cumplidas} de {len(resultados)} comprobaciones cumplidas")
    return 0 if cumplidas == len(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
