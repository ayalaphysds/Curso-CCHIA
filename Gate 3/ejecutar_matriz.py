"""Ejecutor de matrices de prueba sobre TestClient y generador de docs/matriz_pruebas.md (Bloque 42.3)."""

from datetime import date
import hashlib
import importlib
import json
from pathlib import Path
import sys
from fastapi.testclient import TestClient

from servicio.main import app

SALIDA = Path("docs/matriz_pruebas.md")


def cargar(nombre_modulo: str = "matriz_pruebas") -> list[dict]:
    mod = importlib.import_module(nombre_modulo)
    return list(mod.MATRIZ)


def huella(matriz: list[dict]) -> str:
    crudo = json.dumps(matriz, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(crudo.encode("utf-8")).hexdigest()[:12]


def motivos_de_falla(esperado: dict, estado: int, cuerpo: str, datos: dict | None = None) -> list[str]:
    motivos: list[str] = []
    if estado != esperado["estado"]:
        motivos.append(f"estado esperado={esperado['estado']} obtenido={estado}")
    compacto = cuerpo.replace(": ", ":")
    for texto in esperado.get("contiene", []):
        if texto not in cuerpo and texto not in compacto:
            motivos.append(f"falta texto {texto!r}")
    for prohibido in esperado.get("no_contiene", []):
        if prohibido in cuerpo:
            motivos.append(f"aparece texto prohibido {prohibido!r}")
    if "fuentes" in esperado:
        fuentes_esp = esperado["fuentes"]
        fuentes_obt = datos.get("fuentes", []) if isinstance(datos, dict) else []
        if fuentes_esp == []:
            if fuentes_obt != []:
                motivos.append(f"se esperaban fuentes vacias, obtenidas={fuentes_obt}")
        else:
            for f in fuentes_esp:
                if f not in fuentes_obt:
                    motivos.append(f"falta fuente {f!r}")
    return motivos


def ejecutar(matriz: list[dict], cliente: TestClient | None = None) -> list[dict]:
    cli = cliente or TestClient(app, raise_server_exceptions=False)
    resultados: list[dict] = []
    for esc in matriz:
        pet = esc["peticion"]
        kwargs: dict = {}
        if "json" in pet:
            kwargs["json"] = pet["json"]
        r = cli.request(pet["metodo"], pet["ruta"], **kwargs)
        try:
            datos = r.json()
        except Exception:
            datos = None
        motivos = motivos_de_falla(esc["esperado"], r.status_code, r.text, datos)
        resultados.append(
            {
                "id": esc["id"],
                "tipo": esc["tipo"],
                "escenario": esc["escenario"],
                "peticion": f"{pet['metodo']} {pet['ruta']}",
                "esperado": f"HTTP {esc['esperado']['estado']}",
                "cubre": ", ".join(esc["cubre"]),
                "estado": r.status_code,
                "motivos": motivos,
                "resultado": "PASA" if not motivos else "FALLA",
                "hallazgo": esc.get("hallazgo"),
            }
        )
    return resultados


def renderizar_markdown(matriz: list[dict], resultados: list[dict]) -> str:
    cumplidos = sum(1 for r in resultados if r["resultado"] == "PASA")
    lineas = [
        "# Matriz de Pruebas",
        "",
        f"Fecha: {date.today().isoformat()}",
        f"Huella de la matriz: {huella(matriz)}",
        f"Escenarios: {cumplidos} de {len(resultados)} cumplidos",
        "",
        "| ID | Tipo | Escenario | Peticion | Esperado | Cubre | Resultado | Hallazgo |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in resultados:
        hall = ""
        if r["hallazgo"]:
            hall = f"{r['hallazgo'].get('clasificacion', '')}: {r['hallazgo'].get('decision', '')}"
        elif r["motivos"]:
            hall = "; ".join(r["motivos"])
        else:
            hall = "Ninguno"
        lineas.append(
            f"| {r['id']} | {r['tipo']} | {r['escenario']} | {r['peticion']} | "
            f"{r['esperado']} | {r['cubre']} | {r['resultado']} | {hall.replace('|', '/')} |"
        )
    return "\n".join(lineas) + "\n"


def main() -> int:
    escribir = "--escribir" in sys.argv
    nombre = "matriz_pruebas"
    if "--matriz" in sys.argv:
        idx = sys.argv.index("--matriz")
        if idx + 1 < len(sys.argv):
            nombre = sys.argv[idx + 1]

    matriz = cargar(nombre)
    resultados = ejecutar(matriz)
    cumplidos = sum(1 for r in resultados if r["resultado"] == "PASA")
    for r in resultados:
        det = "ok" if not r["motivos"] else "; ".join(r["motivos"])
        print(f"{r['resultado']} {r['id']} [{r['tipo']}]: {det}")
    print(f"Escenarios: {cumplidos} de {len(resultados)} cumplidos")

    if escribir:
        SALIDA.parent.mkdir(parents=True, exist_ok=True)
        SALIDA.write_text(renderizar_markdown(matriz, resultados), encoding="utf-8")
        print(f"Escrito: {SALIDA} (huella {huella(matriz)})")

    return 0 if cumplidos == len(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
