"""Genera docs/registro_alucinaciones.md probando SONDAS contra la cadena protegida (Bloque 43)."""

from datetime import date
from pathlib import Path
import sys
from fastapi.testclient import TestClient

from alucinaciones import SONDAS
from dobles import ModeloAlucinador
from servicio import cadena, respaldo
from servicio.main import app

SALIDA = Path("docs/registro_alucinaciones.md")


def evaluar_sondas(cliente: TestClient | None = None) -> list[dict]:
    cli = cliente or TestClient(app, raise_server_exceptions=False)
    original = respaldo.elegir_modelo
    resultados: list[dict] = []
    try:
        for sonda in SONDAS:
            doble = ModeloAlucinador(sonda["respuesta_simulada"])
            respaldo.elegir_modelo = lambda d=doble: (d, "simulado", None)
            r = cli.post("/consultas", json={"pregunta": sonda["pregunta"]})
            data = r.json() if r.status_code == 200 else {}
            contenida = cadena.SIN_INFORMACION in r.text and data.get("fuentes") == []
            if contenida:
                veredicto = "PASA"
                detalle = "alucinacion bloqueada por capa de fundamentacion"
            elif "decision" in sonda:
                veredicto = "LIMITE"
                detalle = sonda["decision"]
            else:
                veredicto = "FALLA"
                detalle = "llega al usuario"
            resultados.append(
                {
                    "id": sonda["id"],
                    "tipo": sonda["tipo"],
                    "descripcion": sonda["descripcion"],
                    "resultado": veredicto,
                    "detalle": detalle,
                }
            )
    finally:
        respaldo.elegir_modelo = original
    return resultados


def main() -> int:
    resultados = evaluar_sondas()
    for r in resultados:
        print(f"{r['resultado']} {r['id']} ({r['tipo']}): {r['detalle']}")

    if "--escribir" in sys.argv:
        lineas = [
            "# Registro de detección y contención de alucinaciones",
            "",
            f"Fecha: {date.today().isoformat()}",
            f"Sondas evaluadas: {len(resultados)}",
            "",
            "| ID | Tipo | Descripción | Resultado | Decisión / Evidencia |",
            "|---|---|---|---|---|",
        ]
        for r in resultados:
            lineas.append(
                f"| {r['id']} | {r['tipo']} | {r['descripcion']} | {r['resultado']} | {r['detalle'].replace('|', '/')} |"
            )
        SALIDA.parent.mkdir(parents=True, exist_ok=True)
        SALIDA.write_text("\n".join(lineas) + "\n", encoding="utf-8")
        print(f"Escrito: {SALIDA}")

    fallas = [r for r in resultados if r["resultado"] == "FALLA"]
    return 0 if not fallas else 1


if __name__ == "__main__":
    sys.exit(main())
