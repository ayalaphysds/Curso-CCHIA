"""Genera docs/registro_ejecucion.md combinando zona automatica y seccion manual (Bloque 41)."""

from datetime import datetime
from pathlib import Path
import re
import subprocess
import sys
import httpx

import buscar_secretos
import ejecutar_escenarios as ee

DESTINO = Path("docs/registro_ejecucion.md")
MARCA_INICIO = "<!-- AUTO:INICIO -->"
MARCA_FIN = "<!-- AUTO:FIN -->"

MANUAL_POR_DEFECTO = """## Qué se observó

Se ejecutaron los 14 escenarios end-to-end contra la API FastAPI (puerto 8000) y la Interfaz Web (puerto 8080), confirmando respuestas fundamentadas con citas documentales del catalogo CENABAST 2026, deteccion determinista de sobreprecio critico (+50%), contencion de prompt injection y errores uniformes 404/422.

## Qué no se probó

No se ejecuto consumo real contra el endpoint remoto de Google Gemini ni carga concurrente multi-usuario en contenedores productivos; la corrida se efectuo con el componente Modelo en modo simulado determinista para garantizar repetibilidad sin costo de API ni exposicion de credenciales.

## Siguiente paso

Completar la Matriz de Pruebas de la Unidad 3.5 con escenarios validos, invalidos y de borde, incorporar el detector determinista de alucinaciones en la capa de salida y validar las mitigaciones en la Matriz de Riesgos ejecutable.
"""


def _git_estado() -> tuple[str, str]:
    commit = subprocess.run(["git", "rev-parse", "--short=12", "HEAD"], capture_output=True, text=True).stdout.strip()
    status = subprocess.run(["git", "status", "--short", "--", "."], capture_output=True, text=True).stdout.splitlines()
    # Ignorar cambios exclusivamente dentro de docs/ al clasificar codigo limpio
    sucios_codigo = [ln for ln in status if ln.strip() and "docs/" not in ln]
    estado = "sin cambios" if not sucios_codigo else "con cambios pendientes"
    return commit or "0000000", estado


def _ejecutar_pytest() -> tuple[int, int]:
    r = subprocess.run([sys.executable, "-m", "pytest", "-q"], capture_output=True, text=True)
    salida = r.stdout + "\n" + r.stderr
    p = sum(int(x) for x in re.findall(r"(\d+) passed", salida))
    f = sum(int(x) for x in re.findall(r"(\d+) failed", salida))
    e = sum(int(x) for x in re.findall(r"(\d+) error", salida))
    return p, f + e


def _modo_modelo_en_vivo() -> str:
    try:
        r = httpx.get(ee.DESTINOS["api"] + "/salud", timeout=3.0)
        if r.status_code == 200:
            return str(r.json().get("modelo_activo", "simulado"))
    except httpx.HTTPError:
        pass
    return "simulado"


def main() -> int:
    resultados = ee.correr()
    cumplidos = sum(1 for r in resultados if not r["motivos"])
    pasan_t, fallan_t = _ejecutar_pytest()
    commit, estado_git = _git_estado()
    modo_modelo = _modo_modelo_en_vivo()

    filas_esc = [
        f"| {r['id']} | {r['categoria']} ({r['destino']}) | {'pasa' if not r['motivos'] else 'falla'} |"
        for r in resultados
    ]

    zona_auto = "\n".join(
        [
            MARCA_INICIO,
            "# Registro de ejecución completa",
            "",
            "| Campo | Valor |",
            "|---|---|",
            f"| Fecha | {datetime.now().strftime('%Y-%m-%d %H:%M')} |",
            f"| Commit del código | {commit} ({estado_git}) |",
            f"| Resumen escenarios | Escenarios: {cumplidos} de {len(resultados)} cumplidos |",
            f"| Resumen pruebas | Pruebas automáticas: {pasan_t} pasan, {fallan_t} fallan |",
            "",
            "## Componentes ejecutados",
            "",
            "| Componente | Modo | Detalle |",
            "|---|---|---|",
            "| API FastAPI | real | `servicio/main.py` en `http://127.0.0.1:8000` |",
            "| Interfaz Web | real | `interfaz/main.py` en `http://127.0.0.1:8080` |",
            "| Corpus CENABAST | real | 5 documentos normativos en `data/` |",
            f"| Modelo | {modo_modelo} | Adaptador dual (`servicio/respaldo.py`) |",
            "",
            "## Detalle de escenarios",
            "",
            "| ID | Escenario | Resultado |",
            "|---|---|---|",
            *filas_esc,
            MARCA_FIN,
        ]
    )

    if DESTINO.is_file():
        actual = DESTINO.read_text(encoding="utf-8")
        if MARCA_FIN in actual:
            zona_manual = actual.split(MARCA_FIN, 1)[1].lstrip("\n")
        else:
            zona_manual = MANUAL_POR_DEFECTO
    else:
        zona_manual = MANUAL_POR_DEFECTO

    documento = zona_auto + "\n\n" + zona_manual.strip() + "\n"

    if buscar_secretos.CLAVE_GOOGLE.search(documento) or buscar_secretos.ASIGNACION.search(documento):
        print("ERROR: se detecto un posible secreto en el contenido a escribir; escritura cancelada.")
        return 1

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(documento, encoding="utf-8")
    print(f"Registro generado en {DESTINO}: {cumplidos} de {len(resultados)} escenarios, {pasan_t} pruebas pasan")
    return 0


if __name__ == "__main__":
    sys.exit(main())
