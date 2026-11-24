"""Verificador de la prueba cruzada de transferencia (Bloque 45.2)."""

from pathlib import Path
import sys

import transferencia as tr

DOC_TRANS = Path("docs/transferencia.md")


def main() -> int:
    checks: list[tuple[str, bool, str]] = []

    # TRF-1: al menos 2 rondas y ultima cumple meta de tiempo
    ok_1 = len(tr.SESIONES) >= 2 and tr.SESIONES[-1]["exito"] and tr.SESIONES[-1]["minutos"] <= tr.META_MINUTOS
    checks.append(("TRF-1", ok_1, f"ultima ronda={tr.SESIONES[-1]['minutos']} min (meta <= {tr.META_MINUTOS} min)"))

    # TRF-2: mejora de tiempo entre primera y ultima ronda
    ok_2 = tr.SESIONES[-1]["minutos"] < tr.SESIONES[0]["minutos"]
    checks.append(("TRF-2", ok_2, f"reduccion de {tr.SESIONES[0]['minutos']} a {tr.SESIONES[-1]['minutos']} min"))

    # TRF-3: todas las observaciones de documento estan resueltas
    pend_doc = [o["id"] for o in tr.OBSERVACIONES if o["causa"] == "documento" and o["estado"] != "resuelta"]
    checks.append(("TRF-3", not pend_doc, "todas las fricciones de documento resueltas" if not pend_doc else f"pendientes: {pend_doc}"))

    # TRF-4: toda observacion de producto tiene ref LIM-xx
    sin_ref = [o["id"] for o in tr.OBSERVACIONES if o["causa"] == "producto" and not str(o.get("ref", "")).startswith("LIM-")]
    checks.append(("TRF-4", not sin_ref, "observaciones de producto enlazadas a LIM-xx" if not sin_ref else f"sin ref: {sin_ref}"))

    # TRF-5: documento docs/transferencia.md existe y cita todos los T-xx
    if not DOC_TRANS.is_file():
        checks.append(("TRF-5", False, f"no existe {DOC_TRANS}"))
    else:
        txt = DOC_TRANS.read_text(encoding="utf-8")
        faltan = [o["id"] for o in tr.OBSERVACIONES if o["id"] not in txt]
        checks.append(("TRF-5", not faltan, f"{len(tr.OBSERVACIONES)} observaciones registradas en {DOC_TRANS}" if not faltan else f"faltan: {faltan}"))

    cumplidas = sum(1 for _, ok, _ in checks if ok)
    for rid, ok, det in checks:
        print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
    print(f"{cumplidas} de {len(checks)} comprobaciones cumplidas")
    return 0 if cumplidas == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
