"""Verificador maestro de Gate 3: ejecuta las 22 fuentes y genera docs/gate3.md (Bloque S2.3)."""

from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import rubrica_gate3 as rg

PY = sys.executable
TOPE_DE_UNA_FUENTE = 300
INFORME = Path("docs/gate3.md")

FUENTES: dict[str, list[str]] = {
    # 19 fuentes sin Docker
    "ficha": [PY, "verificar_ficha_completa.py"],
    "decisiones": [PY, "verificar_decisiones.py"],
    "frio": [PY, "probar_en_frio.py"],
    "demo": [PY, "ensayo_demo.py"],
    "respaldo": [PY, "ensayo_demo.py", "--comprobar"],
    "mitigaciones": [PY, "verificar_mitigaciones.py"],
    "ia": [
        PY,
        "-m",
        "pytest",
        "-q",
        "tests/parciales/test_cadena.py",
        "tests/parciales/test_fundamentacion.py",
        "tests/parciales/test_modelo.py",
        "tests/parciales/test_respaldo.py",
        "tests/parciales/test_recuperar.py",
        "tests/parciales/test_prompt.py",
    ],
    "servicio": [PY, "verificar_servicio.py"],
    "api_md": [PY, "generar_api_md.py", "--comprobar"],
    "dockerfile": [PY, "verificar_dockerfile.py"],
    "compose": [PY, "verificar_entrega.py"],
    "pytest": [PY, "-m", "pytest", "-q"],
    "matriz": [PY, "verificar_matriz.py"],
    "parciales": [PY, "verificar_parciales.py"],
    "riesgos": [PY, "verificar_riesgos.py"],
    "secretos": [PY, "buscar_secretos.py"],
    "readme": [PY, "verificar_readme.py"],
    "transferencia": [PY, "verificar_transferencia.py"],
    "guion": [PY, "medir_guion.py"],
    # 3 fuentes que requieren Docker activo
    "stack": [PY, "verificar_stack.py"],
    "ejecucion": [PY, "verificar_ejecucion.py"],
    "registro": [PY, "verificar_registro.py"],
}

FUENTES_DOCKER = ("stack", "ejecucion", "registro")

LIMITES_DEL_INFORME = [
    "No verifica la ejecucion en vivo de la demo frente al jurado (confirmado manualmente por el evaluador en NC-3).",
    "No garantiza que las diapositivas visuales de la presentacion ejecutiva esten construidas aparte de docs/defensa.md.",
    "En modo sin Docker omite las 3 comprobaciones de contenedores (stack, ejecucion, registro) y emite veredicto PROVISIONAL.",
    "No prueba la calidad semantica de un modelo LLM externo con cuota activa (usa el modo determinista configurado).",
    "No reemplaza la revision humana de probidad y pertinencia clinica sobre las bases administrativas de CENABAST.",
]


def entregables_que_faltan(raiz: Path = Path(".")) -> list[tuple[str, list[str]]]:
    faltantes = []
    for nombre, archivos in rg.ENTREGABLES:
        ausentes = [a for a in archivos if not (raiz / a).is_file()]
        if ausentes:
            faltantes.append((nombre, ausentes))
    return faltantes


def leer_cifras(cmd: list[str], salida: str, returncode: int) -> tuple[int, int]:
    es_pytest = "pytest" in cmd
    if es_pytest:
        p = sum(int(x) for x in re.findall(r"(\d+) passed", salida))
        f = sum(int(x) for x in re.findall(r"(\d+) failed", salida))
        e = sum(int(x) for x in re.findall(r"(\d+) error", salida))
        if p + f + e > 0:
            return p, p + f + e

    coincidencias = re.findall(r"(\d+) de (\d+) (?:comprobaciones|reglas|pasos)", salida)
    if coincidencias:
        cumplidas, total = int(coincidencias[-1][0]), int(coincidencias[-1][1])
        if returncode != 0 and cumplidas == total:
            total += 1
        return cumplidas, total

    return (1, 1) if returncode == 0 else (0, 1)


def primera_causa(salida: str, returncode: int) -> str:
    if returncode == 0:
        return ""
    lineas = salida.splitlines()
    for i, ln in enumerate(lineas):
        if ln.startswith(("FALLA", "FAILED", "ERROR")):
            partes = [ln.strip()]
            j = i + 1
            while j < len(lineas) and lineas[j].startswith("      "):
                partes.append(lineas[j].strip())
                j += 1
            return " | ".join(partes)
    no_vacias = [ln.strip() for ln in lineas if ln.strip()]
    return no_vacias[-1] if no_vacias else f"codigo de salida {returncode}"


def nota(puntaje: float) -> float:
    if puntaje < rg.UMBRAL:
        return round(1.0 + 3.0 * puntaje / rg.UMBRAL, 2)
    return round(4.0 + 3.0 * (puntaje - rg.UMBRAL) / (100.0 - rg.UMBRAL), 2)


def puntuar(resultados: dict[str, dict]) -> tuple[list[dict], float]:
    detalle = []
    total_pts = 0.0
    for c in rg.CRITERIOS:
        usadas = [f for f in c["fuentes"] if f in resultados]
        if not usadas:
            pts = 0.0
            estado = "sin evidencia"
        else:
            fracciones = [
                (resultados[f]["cumplidas"] / resultados[f]["total"]) if resultados[f]["total"] > 0 else 0.0
                for f in usadas
            ]
            pts = round(c["peso"] * (sum(fracciones) / len(fracciones)), 2)
            estado = f"{len(usadas)}/{len(c['fuentes'])} fuentes"
        total_pts += pts
        detalle.append(
            {
                "id": c["id"],
                "nombre": c["nombre"],
                "peso": c["peso"],
                "puntos": pts,
                "estado": estado,
                "usadas": usadas,
            }
        )
    return detalle, round(total_pts, 2)


def no_compensables_que_fallan(resultados: dict[str, dict]) -> list[tuple[str, str]]:
    fallas = []
    for nc in rg.NO_COMPENSABLES:
        if not nc["fuentes"]:
            continue
        ejecutadas = [f for f in nc["fuentes"] if f in resultados]
        if not ejecutadas:
            fallas.append((nc["id"], "sin evidencia"))
            continue
        rotas = [f for f in ejecutadas if resultados[f]["cumplidas"] != resultados[f]["total"]]
        if rotas:
            fallas.append((nc["id"], "falla " + ", ".join(rotas)))
    return fallas


def decidir(puntaje: float, fallas_nc: list[tuple[str, str]], omitidas: list[str]) -> tuple[str, str, int]:
    if fallas_nc:
        return "NO APRUEBA", "un criterio no compensable falla", 1
    if puntaje < rg.UMBRAL:
        return "NO APRUEBA", f"el puntaje no llega a {rg.UMBRAL}", 1
    if omitidas:
        return "PROVISIONAL", f"faltan las comprobaciones con Docker: {', '.join(omitidas)}", 2
    return "APRUEBA", f"puntaje de al menos {rg.UMBRAL} y nada que falle", 0


def _ejecutar_fuente(nombre: str, cmd: list[str]) -> dict:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=TOPE_DE_UNA_FUENTE, env=env)
    salida = (r.stdout or "") + "\n" + (r.stderr or "")
    cumplidas, total = leer_cifras(cmd, salida, r.returncode)
    return {
        "nombre": nombre,
        "returncode": r.returncode,
        "cumplidas": cumplidas,
        "total": total,
        "causa": primera_causa(salida, r.returncode),
    }


def _bajar_docker() -> None:
    subprocess.run(["docker", "compose", "down"], capture_output=True)


def _levantar_docker() -> bool:
    r = subprocess.run(
        ["docker", "compose", "up", "-d", "--build", "--wait", "--wait-timeout", "120"],
        capture_output=True,
    )
    return r.returncode == 0


def renderizar_informe(
    modo: str,
    resultados: dict[str, dict],
    detalle_criterios: list[dict],
    puntaje: float,
    calif: float,
    veredicto: str,
    motivo: str,
    fallas_nc: list[tuple[str, str]],
    omitidas: list[str],
) -> str:
    huella = hashlib.sha256(
        json.dumps(resultados, sort_keys=True, ensure_ascii=True).encode("utf-8")
    ).hexdigest()[:12]
    fallas_map = dict(fallas_nc)

    lineas = [
        "# Informe de Verificación — Gate 3 / Capstone",
        "",
        f"- **Fecha:** {datetime.now().isoformat(timespec='seconds')}",
        f"- **Modo:** {modo}",
        f"- **Huella de la evidencia:** `{huella}`",
        f"- **Puntaje:** `{puntaje:.2f} / 100`",
        f"- **Nota:** `{calif:.2f}` (escala 1.0 a 7.0, exigencia 60%)",
        f"- **Resultado:** **{veredicto}** ({motivo})",
        "",
        "## Criterios",
        "",
        "| ID | Dimensión | Peso | Puntos | Cobertura |",
        "|---|---|---:|---:|---|",
    ]
    for c in detalle_criterios:
        lineas.append(f"| {c['id']} | {c['nombre']} | {c['peso']} | {c['puntos']:.2f} | {c['estado']} |")

    lineas.extend(
        [
            "",
            "## No compensables",
            "",
            "| ID | Criterio | Estado automatizado |",
            "|---|---|---|",
        ]
    )
    for nc in rg.NO_COMPENSABLES:
        if not nc["fuentes"]:
            est = "Confirmación manual del evaluador"
        elif nc["id"] in fallas_map:
            est = f"FALLA ({fallas_map[nc['id']]})"
        else:
            est = "PASA"
        lineas.append(f"| {nc['id']} | {nc['nombre']} | {est} |")

    lineas.extend(["", "## Lo que confirma el evaluador", ""])
    for nc in rg.NO_COMPENSABLES:
        if "evaluador" in nc:
            lineas.append(f"- **{nc['id']}:** {nc['evaluador']}")

    lineas.extend(["", "## Entregables", ""])
    for nombre, archivos in rg.ENTREGABLES:
        lineas.append(f"- **{nombre}:** {', '.join(f'`{a}`' for a in archivos)}")

    lineas.extend(["", "## Fuentes ejecutadas", "", "| Fuente | Resultado | Cumplidas | Detalle |", "|---|---|---:|---|"])
    for nombre, res in resultados.items():
        est = "PASA" if res["cumplidas"] == res["total"] and res["returncode"] == 0 else "FALLA"
        det = res["causa"] or "ok"
        lineas.append(f"| `{nombre}` | {est} | {res['cumplidas']}/{res['total']} | {det.replace('|', '/')} |")
    for om in omitidas:
        lineas.append(f"| `{om}` | OMITIDA | 0/0 | Requiere `--con-docker` |")

    lineas.extend(["", "## Lo que este informe no demuestra", ""])
    for lim in LIMITES_DEL_INFORME:
        lineas.append(f"- {lim}")

    return "\n".join(lineas) + "\n"


def main() -> int:
    con_docker = "--con-docker" in sys.argv
    escribir = "--escribir" in sys.argv

    faltantes = entregables_que_faltan()
    if faltantes:
        for nombre, ausentes in faltantes:
            print(f"FALTA {nombre} -> {ausentes}")
        return 1

    resultados: dict[str, dict] = {}
    omitidas: list[str] = []

    if con_docker:
        _bajar_docker()

    try:
        for nombre, cmd in FUENTES.items():
            if nombre in FUENTES_DOCKER:
                if not con_docker:
                    omitidas.append(nombre)
                    continue
                if nombre == "ejecucion":
                    _levantar_docker()
            res = _ejecutar_fuente(nombre, cmd)
            resultados[nombre] = res
            marca = "PASA" if res["cumplidas"] == res["total"] and res["returncode"] == 0 else "FALLA"
            extra = f" -> {res['causa']}" if res["causa"] else ""
            print(f"{marca} {nombre:14s}: {res['cumplidas']}/{res['total']}{extra}")
    finally:
        if con_docker:
            _bajar_docker()

    detalle, pts = puntuar(resultados)
    calif = nota(pts)
    fallas_nc = no_compensables_que_fallan(resultados)
    veredicto, motivo, rc = decidir(pts, fallas_nc, omitidas)

    print(f"\nPuntaje: {pts:.2f}/100 | Nota: {calif:.2f} | Resultado: {veredicto} ({motivo})")
    if escribir:
        modo = "con Docker" if con_docker else "sin Docker"
        INFORME.parent.mkdir(parents=True, exist_ok=True)
        INFORME.write_text(
            renderizar_informe(modo, resultados, detalle, pts, calif, veredicto, motivo, fallas_nc, omitidas),
            encoding="utf-8",
        )
        print(f"Informe escrito en {INFORME}")

    return rc


if __name__ == "__main__":
    sys.exit(main())
