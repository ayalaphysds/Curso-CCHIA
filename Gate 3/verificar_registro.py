"""Verificador offline de 6 reglas sobre docs/registro_ejecucion.md (Bloque 41.3 CORE)."""

from pathlib import Path
import re
import subprocess
import sys

import buscar_secretos
from escenarios import ESCENARIOS

REGISTRO = Path("docs/registro_ejecucion.md")
MARCA_INICIO = "<!-- AUTO:INICIO -->"
MARCA_FIN = "<!-- AUTO:FIN -->"
SECCIONES_MANUALES = ("Qué se observó", "Qué no se probó", "Siguiente paso")

PATRON_COMMIT = re.compile(r"\| Commit del código \| ([0-9a-f]{7,40}) \(([^)]*)\) \|")
PATRON_CIFRA = re.compile(r"Escenarios: (\d+) de (\d+) cumplidos")
PATRON_FILA_ESC = re.compile(r"(?m)^\| (E-\d+) \| [^|]+ \| ([^|]+) \|$")
PATRON_PRUEBAS = re.compile(r"Pruebas automáticas: (\d+) pasan, (\d+) fallan")
PATRON_RESPALDO = re.compile(r"\| ([^|]+) \| respaldo \|")


def _extraer_manual(texto: str, titulo: str) -> str | None:
    m = re.search(rf"(?ms)^## {re.escape(titulo)}\n(.*?)(?=^## |\Z)", texto)
    return m.group(1).strip() if m else None


def main() -> int:
    if not REGISTRO.is_file():
        print(f"FALLA REG-1 no existe {REGISTRO}")
        print("0 de 6 comprobaciones cumplidas")
        return 1

    texto = REGISTRO.read_text(encoding="utf-8")
    resultados: list[tuple[str, bool, str]] = []

    # REG-1: estructura
    secciones = {s: _extraer_manual(texto, s) for s in SECCIONES_MANUALES}
    ok_1 = (
        MARCA_INICIO in texto
        and MARCA_FIN in texto
        and all(v is not None for v in secciones.values())
    )
    resultados.append(("REG-1", ok_1, "marcadores AUTO y 3 secciones manuales presentes" if ok_1 else "estructura incompleta"))

    # REG-2: manual_completo
    incompletas = []
    for nombre, cuerpo in secciones.items():
        if cuerpo is None or "[COMPLETAR]" in cuerpo or len(cuerpo) < 40:
            incompletas.append(nombre)
    resultados.append(("REG-2", len(incompletas) == 0, "3 secciones manuales completas (>=40 chars)" if not incompletas else f"incompletas: {incompletas}"))

    # REG-3: commit_vigente
    m_c = PATRON_COMMIT.search(texto)
    if not m_c:
        resultados.append(("REG-3", False, "no se encontro linea de commit"))
    else:
        chash, estado = m_c.group(1), m_c.group(2).strip()
        existe = subprocess.run(["git", "cat-file", "-e", f"{chash}^{{commit}}"], capture_output=True).returncode == 0
        diff = subprocess.run(["git", "diff", "--name-only", chash, "HEAD", "--", "."], capture_output=True, text=True)
        cambiados_fuera_docs = [
            f for f in diff.stdout.splitlines()
            if f.strip() and not f.strip().startswith("docs/") and "/docs/" not in f.strip()
        ]
        ok_3 = estado == "sin cambios" and existe and len(cambiados_fuera_docs) == 0
        det_3 = f"commit {chash} vigente ({estado})" if ok_3 else f"estado={estado}, existe={existe}, cambios={cambiados_fuera_docs}"
        resultados.append(("REG-3", ok_3, det_3))

    # REG-4: cifras_coherentes
    m_cif = PATRON_CIFRA.search(texto)
    m_pru = PATRON_PRUEBAS.search(texto)
    filas_esc = PATRON_FILA_ESC.findall(texto)
    if not m_cif or not m_pru:
        resultados.append(("REG-4", False, "faltan cifras de escenarios o pruebas"))
    else:
        cumplidos, total = int(m_cif.group(1)), int(m_cif.group(2))
        pasan_t, fallan_t = int(m_pru.group(1)), int(m_pru.group(2))
        pasan_esc = sum(1 for _, res in filas_esc if res.strip().lower() == "pasa")
        ok_4 = (
            total == len(ESCENARIOS)
            and len(filas_esc) == total
            and pasan_esc == cumplidos
            and fallan_t == 0
        )
        resultados.append(("REG-4", ok_4, f"{cumplidos}/{total} escenarios y {pasan_t} pruebas pasan ({fallan_t} fallan)"))

    # REG-5: respaldos_declarados
    m_resp = PATRON_RESPALDO.search(texto)
    if not m_resp:
        resultados.append(("REG-5", True, "sin componentes en modo respaldo"))
    else:
        comp = m_resp.group(1).strip()
        no_probado = (secciones.get("Qué no se probó") or "").lower()
        ok_5 = comp.lower() in no_probado and "respaldo" in no_probado
        resultados.append(("REG-5", ok_5, f"respaldo de {comp} declarado en 'Qué no se probó'" if ok_5 else f"falta declarar respaldo de {comp}"))

    # REG-6: sin_secretos
    sin_sec = not buscar_secretos.CLAVE_GOOGLE.search(texto) and not buscar_secretos.ASIGNACION.search(texto)
    env_git = subprocess.run(["git", "ls-files", ".env"], capture_output=True, text=True).stdout.strip() == ""
    ok_6 = sin_sec and env_git
    resultados.append(("REG-6", ok_6, "registro libre de secretos y .env fuera de Git" if ok_6 else "secreto o .env detectado"))

    cumplidas = sum(1 for _, ok, _ in resultados if ok)
    for rid, ok, det in resultados:
        print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
    print(f"{cumplidas} de {len(resultados)} comprobaciones cumplidas")
    return 0 if cumplidas == len(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
