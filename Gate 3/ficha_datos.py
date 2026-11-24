"""Extrae datos estructurados de docs/ficha_diseno_funcional.md (Bloque 34.2)."""

from pathlib import Path
import re

from verificar_ficha import FICHA, extraer_alcance, extraer_secciones

NUMERO = r"(\d+(?:[.,]\d+)?)"


def _a_float(texto: str) -> float:
    return float(texto.replace(",", "."))


def cargar_ficha(ruta: Path = FICHA) -> dict:
    texto = ruta.read_text(encoding="utf-8")
    secciones = extraer_secciones(texto)
    s2 = secciones["2"][1]
    s4 = secciones["4"][1]
    s5 = secciones["5"][1]

    rfs = dict(re.findall(r"(?m)^- (RF-\d{2}): (.+)$", s2))
    rnfs = dict(re.findall(r"(?m)^- (RNF-\d{2}): (.+)$", s2))
    alcance = extraer_alcance(s2)

    criterios = []
    for m in re.finditer(r"(?m)^- (CA-\d{2}) \(([^)]*)\): (.+)$", s4):
        cid, refs_raw, desc = m.group(1), m.group(2), m.group(3).strip()
        refs = re.findall(r"(?:RNF|RF)-\d{2}", refs_raw)
        criterios.append({"id": cid, "refs": refs, "texto": desc})

    m_disp = re.search(rf"(?m)^Horas disponibles:\s*{NUMERO} h", s5)
    m_marg = re.search(rf"(?m)^Margen de imprevistos:\s*{NUMERO} h", s5)

    hitos = []
    for m in re.finditer(rf"(?m)^- (H\d+) \({NUMERO} h\): (.+)$", s5):
        hid, horas_raw, desc = m.group(1), m.group(2), m.group(3).strip()
        m_cubre = re.search(r"Cubre:\s*([^.]+)", desc)
        m_comp = re.search(r"Se comprueba con:\s*([^.]+)", desc)
        cubre = re.findall(r"(?:RNF|RF)-\d{2}", m_cubre.group(1)) if m_cubre else []
        cas = re.findall(r"CA-\d{2}", m_comp.group(1)) if m_comp else []
        hitos.append(
            {
                "id": hid,
                "horas": _a_float(horas_raw),
                "texto": desc,
                "cubre": cubre,
                "criterios": cas,
            }
        )

    return {
        "ruta": str(ruta),
        "secciones": secciones,
        "rf": rfs,
        "rnf": rnfs,
        "alcance": alcance,
        "criterios": criterios,
        "horas_disponibles": _a_float(m_disp.group(1)) if m_disp else None,
        "margen_imprevistos": _a_float(m_marg.group(1)) if m_marg else None,
        "hitos": hitos,
    }
