"""Verificador de 6 reglas que ejecuta toda la evidencia de riesgos.py (Bloque 43.3 CORE)."""

from pathlib import Path
import re
import subprocess
import sys
from fastapi.testclient import TestClient

from alucinaciones import SONDAS
from ataques import ATAQUES
import ejecutar_matriz as em
import riesgos as mod_riesgos
from servicio.main import app
import verificar_mitigaciones as vm

DOC_RIESGOS = Path("docs/matriz_riesgos.md")
CAMPOS = ("id", "riesgo", "probabilidad", "impacto", "mitigacion", "evidencia", "estado", "residual")


def resolver(ref: str, cliente: TestClient, cache_aluc: dict[str, str]) -> str:
    if ":" not in ref:
        return "DESCONOCIDA"
    tipo, nombre = ref.split(":", 1)

    if tipo == "ataques":
        mapa = {a["id"]: a for a in ATAQUES}
        if nombre not in mapa:
            return "DESCONOCIDA"
        return vm.correr_ataque(cliente, mapa[nombre])["resultado"]

    if tipo == "fuga":
        if nombre not in vm.FUGAS:
            return "DESCONOCIDA"
        ok, _ = vm.FUGAS[nombre](cliente)
        return "PASA" if ok else "FALLA"

    if tipo == "alucinacion":
        return cache_aluc.get(nombre, "DESCONOCIDA")

    if tipo in ("matriz", "matriz_modelo"):
        modulo = "matriz_pruebas" if tipo == "matriz" else "matriz_modelo"
        resultados = {r["id"]: r for r in em.ejecutar(em.cargar(modulo), cliente=cliente)}
        if nombre not in resultados:
            return "DESCONOCIDA"
        r = resultados[nombre]
        if r["resultado"] == "PASA":
            return "PASA"
        if (r.get("hallazgo") or {}).get("clasificacion") == "limitacion":
            return "LIMITE"
        return "FALLA"

    if tipo == "pruebas":
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", nombre], capture_output=True, text=True)
        return "PASA" if r.returncode == 0 else "FALLA"

    if tipo == "comando":
        partes = nombre.split()
        if partes and partes[0] == "python":
            partes[0] = sys.executable
        r = subprocess.run(partes, capture_output=True, text=True)
        return "PASA" if r.returncode == 0 else "FALLA"

    return "DESCONOCIDA"


def main() -> int:
    lista = mod_riesgos.RIESGOS
    cliente = TestClient(app, raise_server_exceptions=False)
    cache_aluc = {r["id"]: r["resultado"] for r in vm.contener_alucinaciones(cliente)}
    checks: list[tuple[str, bool, str]] = []

    # RIE-1: estructura
    ids = [r.get("id") for r in lista]
    ok_1 = len(lista) >= 6 and len(ids) == len(set(ids))
    for r in lista:
        if not all(k in r for k in CAMPOS):
            ok_1 = False
            break
        res = r.get("residual", {})
        scores = [r["probabilidad"], r["impacto"], res.get("probabilidad"), res.get("impacto")]
        if not all(isinstance(x, int) and 1 <= x <= 5 for x in scores):
            ok_1 = False
            break
        if r["estado"] not in mod_riesgos.ESTADOS or not r["evidencia"]:
            ok_1 = False
            break
    checks.append(("RIE-1", ok_1, f"{len(lista)} riesgos con esquema valido"))

    # RIE-2: residual_coherente
    incoherentes = []
    for r in lista:
        inh = mod_riesgos.puntaje(r["probabilidad"], r["impacto"])
        res = mod_riesgos.residual(r)
        if res > inh:
            incoherentes.append(f"{r['id']}(res>inh)")
        elif r["estado"] == "aceptada" and res != inh:
            incoherentes.append(f"{r['id']}(aceptada!=inh)")
        elif r["estado"] != "aceptada" and not (res < inh):
            incoherentes.append(f"{r['id']}(no reduce)")
    checks.append(("RIE-2", not incoherentes, "puntajes residuales coherentes" if not incoherentes else f"incoherentes: {incoherentes}"))

    # RIE-3: evidencia_ejecutada
    fallas_ev = []
    for r in lista:
        for ref in r["evidencia"]:
            ver = resolver(ref, cliente, cache_aluc)
            esperado = "LIMITE" if r["estado"] == "aceptada" else "PASA"
            if ver != esperado:
                fallas_ev.append(f"{r['id']}:{ref}={ver} (esp {esperado})")
    checks.append(("RIE-3", not fallas_ev, "toda la evidencia ejecutada con veredicto esperado" if not fallas_ev else f"fallas: {fallas_ev}"))

    # RIE-4: limites_declarados
    faltan_lim = []
    limites_en_riesgos: set[str] = set()
    for r in lista:
        if r["estado"] in ("parcial", "aceptada"):
            if len(str(r.get("nota", ""))) < 20 or not r.get("limites"):
                faltan_lim.append(f"{r['id']}(nota/limites)")
            limites_en_riesgos.update(r.get("limites", []))

    limites_codigo: set[str] = set()
    for a in ATAQUES:
        if a.get("hallazgo", {}).get("clasificacion") == "limitacion":
            limites_codigo.add(a["id"])
    for s in SONDAS:
        if "decision" in s:
            limites_codigo.add(s["id"])
    for e in em.cargar("matriz_modelo"):
        if e.get("hallazgo", {}).get("clasificacion") == "limitacion":
            limites_codigo.add(e["id"])

    no_cubiertos = sorted(limites_codigo - limites_en_riesgos)
    ok_4 = not faltan_lim and not no_cubiertos
    checks.append(("RIE-4", ok_4, f"todos los limites de codigo declarados ({sorted(limites_codigo)})" if ok_4 else f"faltan: {faltan_lim + no_cubiertos}"))

    # RIE-5: supervision para residual ALTO o CRITICO
    sin_sup = [
        r["id"] for r in lista
        if mod_riesgos.categoria(mod_riesgos.residual(r)) in ("ALTO", "CRITICO")
        and not str(r.get("supervision", "")).strip()
    ]
    checks.append(("RIE-5", not sin_sup, "riesgos ALTO/CRITICO con supervision asignada" if not sin_sup else f"sin supervision: {sin_sup}"))

    # RIE-6: registro_vigente
    if not DOC_RIESGOS.is_file():
        checks.append(("RIE-6", False, f"no existe {DOC_RIESGOS}"))
    else:
        m_h = re.search(r"Huella de la matriz: ([0-9a-f]{12})", DOC_RIESGOS.read_text(encoding="utf-8"))
        esp = mod_riesgos.huella()
        ok_6 = bool(m_h) and m_h.group(1) == esp
        checks.append(("RIE-6", ok_6, f"huella vigente {esp}" if ok_6 else "huella desactualizada"))

    cumplidas = sum(1 for _, ok, _ in checks if ok)
    for rid, ok, det in checks:
        print(f"{'PASA' if ok else 'FALLA'} {rid}: {det}")
    print(f"{cumplidas} de {len(checks)} comprobaciones cumplidas")
    return 0 if cumplidas == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
