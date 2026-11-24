"""Verifica las secciones 1 a 3 de docs/ficha_diseno_funcional.md (Bloque 33.3)."""

from pathlib import Path
import re
import sys
import unicodedata

FICHA = Path("docs/ficha_diseno_funcional.md")
SECCIONES_ESPERADAS = {
    "1": "problema",
    "2": "requerimientos",
    "3": "arquitectura",
    "4": "criterios",
    "5": "plan",
}
PALABRAS_SOLUCION = ("chatbot", "rag", "modelo", "inteligencia artificial", "llm")
MAX_IMPRESCINDIBLES = 5


def normalizar(texto: str) -> str:
    sin_tildes = "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )
    return sin_tildes.lower()


def extraer_secciones(texto: str) -> dict[str, tuple[str, str]]:
    patron = re.compile(r"^## (\d)\.\s*(.+)$", re.M)
    matches = list(patron.finditer(texto))
    secciones: dict[str, tuple[str, str]] = {}
    for i, m in enumerate(matches):
        num = m.group(1)
        titulo = m.group(2).strip()
        inicio = m.end()
        fin = matches[i + 1].start() if i + 1 < len(matches) else len(texto)
        secciones[num] = (titulo, texto[inicio:fin].strip())
    return secciones


def extraer_alcance(cuerpo_s2: str) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {}
    for nombre in ("Imprescindible", "Deseable", "Fuera de alcance"):
        m = re.search(rf"(?m)^{nombre}:\s*(.*)$", cuerpo_s2)
        if m:
            buckets[nombre] = re.findall(r"RF-\d{2}", m.group(1))
    return buckets


def verificar(ruta: Path = FICHA) -> tuple[list[str], list[str]]:
    errores: list[str] = []
    avisos: list[str] = []

    if not ruta.is_file():
        return [f"No existe {ruta}"], avisos

    texto = ruta.read_text(encoding="utf-8")
    secciones = extraer_secciones(texto)

    for num, clave in SECCIONES_ESPERADAS.items():
        if num not in secciones:
            errores.append(f"Falta la seccion {num} ({clave})")
        else:
            titulo, _ = secciones[num]
            if clave not in normalizar(titulo):
                errores.append(f"Seccion {num} no contiene palabra clave '{clave}' en titulo '{titulo}'")

    if errores:
        return errores, avisos

    for num in ("1", "2", "3"):
        if "[COMPLETAR" in secciones[num][1]:
            errores.append(f"Seccion {num} aun contiene marcadores [COMPLETAR]")

    # Seccion 1: problema sin terminos de solucion
    s1_norm = normalizar(secciones["1"][1])
    for palabra in PALABRAS_SOLUCION:
        if re.search(rf"\b{re.escape(palabra)}\b", s1_norm):
            avisos.append(f"Seccion 1 menciona termino de solucion '{palabra}'")

    # Seccion 2: RF, RNF y alcance
    s2 = secciones["2"][1]
    rfs = re.findall(r"(?m)^- (RF-\d{2}): (.+)$", s2)
    rnfs = re.findall(r"(?m)^- (RNF-\d{2}): (.+)$", s2)

    if len(rfs) < 3:
        errores.append(f"Se requieren al menos 3 RF; encontrados {len(rfs)}")
    if len(rnfs) < 2:
        errores.append(f"Se requieren al menos 2 RNF; encontrados {len(rnfs)}")
    for rid, desc in rnfs:
        if not re.search(r"\d", desc):
            errores.append(f"{rid} no incluye ningun dato numerico medible")

    alcance = extraer_alcance(s2)
    for nombre in ("Imprescindible", "Deseable", "Fuera de alcance"):
        if nombre not in alcance:
            errores.append(f"Falta la linea '{nombre}:' en Alcance")

    if "Imprescindible" in alcance:
        n_imp = len(alcance["Imprescindible"])
        if n_imp < 1 or n_imp > MAX_IMPRESCINDIBLES:
            errores.append(f"Imprescindible debe tener entre 1 y {MAX_IMPRESCINDIBLES} RF; tiene {n_imp}")

    rf_ids = [rid for rid, _ in rfs]
    conteo: dict[str, int] = {rid: 0 for rid in rf_ids}
    for nombre, ids in alcance.items():
        for rid in ids:
            if rid not in conteo:
                errores.append(f"{rid} aparece en {nombre} pero no esta definido")
            else:
                conteo[rid] += 1

    for rid, veces in conteo.items():
        if veces == 0:
            errores.append(f"{rid} no fue clasificado en ninguna categoria de Alcance")
        elif veces > 1:
            errores.append(f"{rid} aparece clasificado {veces} veces en Alcance")

    # Seccion 3: diagrama existente
    s3 = secciones["3"][1]
    m_diag = re.search(r"docs/[\w\-./]+\.(?:png|jpg|jpeg)", s3)
    if not m_diag:
        errores.append("Seccion 3 no referencia un diagrama en docs/*.png|jpg|jpeg")
    else:
        ruta_diag = Path(m_diag.group(0))
        if not ruta_diag.is_file():
            errores.append(f"El diagrama referenciado no existe: {ruta_diag}")

    return errores, avisos


def main() -> int:
    errores, avisos = verificar()
    for av in avisos:
        print(f"AVISO: {av}")
    for err in errores:
        print(f"ERROR: {err}")
    if errores:
        return 1
    print("Ficha verificada: secciones 1 a 3 completas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
