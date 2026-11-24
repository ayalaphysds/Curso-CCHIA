"""Recuperador documental hibrido determinista sobre el corpus CENABAST (Gate 3)."""

from pathlib import Path
import re
import unicodedata

from servicio.contratos import Fragmento, verificar_fragmento

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "al",
    "a", "en", "por", "para", "con", "sin", "sobre", "entre", "que", "cual",
    "cuales", "como", "cuando", "donde", "es", "son", "se", "su", "sus", "y",
    "o", "u", "si", "no", "mas", "pero", "este", "esta", "estos", "estas",
    "ese", "esa", "todo", "toda", "todos", "todas", "ser", "estar", "tiene",
    "tienen", "debe", "deben", "puede", "pueden", "hay", "fue", "han", "me",
    "te", "le", "nos", "mi", "tu", "ciento", "respecto", "ante", "segun",
}

TERMINOS_CLAVE_ALTO_PESO = {
    "paracetamol": 4.0,
    "ceftriaxona": 4.0,
    "losartan": 4.0,
    "amoxicilina": 4.0,
    "insulina": 4.0,
    "nph": 3.0,
    "sobreprecio": 3.0,
    "temerarios": 3.0,
    "temeraria": 3.0,
    "negociacion": 2.5,
    "multa": 3.0,
    "multas": 3.0,
    "atraso": 2.0,
    "frio": 2.0,
    "cadena": 1.5,
    "temperatura": 1.5,
    "incl": 3.5,
    "cupos": 2.5,
    "cupo": 2.5,
    "concentracion": 2.5,
    "supervision": 3.0,
    "interrupt": 3.0,
    "langgraph": 3.0,
    "ponderacion": 3.0,
    "bioequivalencia": 3.0,
    "isp": 2.5,
    "bpm": 2.5,
    "precio": 2.0,
    "precios": 2.0,
    "referencia": 2.0,
    "catalogo": 2.0,
    "umbral": 2.5,
    "umbrales": 2.5,
    "licitacion": 2.0,
    "licitaciones": 2.0,
    "adjudicacion": 2.0,
    "adjudicaciones": 2.0,
    "riesgo": 2.0,
    "sanciones": 2.5,
    "garantia": 2.0,
    "emergencia": 2.5,
    "plazo": 2.0,
    "entrega": 2.0,
    "stock": 2.5,
    "quiebre": 2.5,
    "cenabast": 1.2,
}

MARCADORES_INGLES = {
    "what", "which", "how", "when", "where", "who", "why", "the", "is", "are",
    "price", "policy", "return", "drug", "medicine", "threshold", "penalty",
    "human", "oversight", "catalog", "cold", "chain", "fine",
}

UMBRAL_MINIMO = 2.5


def normalizar(texto: str) -> str:
    sin_tildes = "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )
    return sin_tildes.lower()


def tokenizar(texto: str) -> list[str]:
    norm = normalizar(texto)
    crudos = re.findall(r"[a-z0-9]+", norm)
    return [t for t in crudos if len(t) >= 2 and t not in STOPWORDS]


def parece_otro_idioma(pregunta: str) -> bool:
    palabras = re.findall(r"[a-z]+", normalizar(pregunta))
    if not palabras:
        return False
    hits_en = sum(1 for p in palabras if p in MARCADORES_INGLES)
    return hits_en >= 2 and (hits_en / len(palabras)) >= 0.30


def cargar_corpus(directorio: Path = DATA_DIR) -> list[Fragmento]:
    fragmentos: list[Fragmento] = []
    if not directorio.is_dir():
        return fragmentos

    for ruta in sorted(directorio.glob("*.md")):
        contenido = ruta.read_text(encoding="utf-8")
        bloques = re.split(r"\n(?=##+ )", contenido)
        for bloque in bloques:
            limpio = bloque.strip()
            if len(limpio) < 40:
                continue
            primera_linea = limpio.splitlines()[0].lstrip("#").strip()
            # Para tablas grandes de catalogo, tambien indexar cada fila de medicamento
            if "LISTADO DE MEDICAMENTOS ESENCIALES" in primera_linea.upper():
                fragmentos.append(
                    verificar_fragmento(
                        Fragmento(fuente=ruta.name, seccion=primera_linea, texto=limpio, puntaje=0.0)
                    )
                )
                for linea in limpio.splitlines():
                    if linea.startswith("| **51"):
                        fragmentos.append(
                            verificar_fragmento(
                                Fragmento(
                                    fuente=ruta.name,
                                    seccion="Registro de medicamento - Catalogo 2026",
                                    texto=linea.strip(),
                                    puntaje=0.0,
                                )
                            )
                        )
            else:
                fragmentos.append(
                    verificar_fragmento(
                        Fragmento(fuente=ruta.name, seccion=primera_linea, texto=limpio, puntaje=0.0)
                    )
                )
    return fragmentos


def _puntaje_fragmento(tokens_q: list[str], frag: Fragmento) -> float:
    tokens_f = set(tokenizar(frag.seccion + " " + frag.texto))
    if not tokens_f or not tokens_q:
        return 0.0

    puntaje = 0.0
    coincidencias_especificas = 0
    for tok in set(tokens_q):
        if tok in tokens_f:
            peso = TERMINOS_CLAVE_ALTO_PESO.get(tok, 1.0)
            puntaje += peso
            if tok != "cenabast":
                coincidencias_especificas += 1

    # Si solo coincidio la palabra generica "cenabast", no cuenta como respaldo real
    if coincidencias_especificas == 0:
        return 0.0

    # Priorizar registros individuales de medicamento cuando el usuario pregunta por un farmaco puntual
    if frag.seccion.startswith("Registro de medicamento"):
        for farmaco in ("paracetamol", "ceftriaxona", "losartan", "amoxicilina", "insulina"):
            if farmaco in tokens_q and farmaco in tokens_f:
                puntaje += 5.0

    return round(puntaje, 3)


def recuperar(pregunta: str, k: int = 3, directorio: Path = DATA_DIR) -> list[Fragmento]:
    """Recupera hasta k fragmentos relevantes del corpus CENABAST.

    Limitacion conocida (LIM-02): el recuperador es lexico en espanol; consultas
    en otro idioma o con sinonimos coloquiales ausentes del corpus retornan [].
    """
    if not pregunta or not pregunta.strip() or k <= 0:
        return []
    if parece_otro_idioma(pregunta):
        return []

    tokens_q = tokenizar(pregunta)
    if not tokens_q:
        return []

    corpus = cargar_corpus(directorio)
    puntuados: list[Fragmento] = []
    for frag in corpus:
        score = _puntaje_fragmento(tokens_q, frag)
        if score >= UMBRAL_MINIMO:
            puntuados.append(
                Fragmento(
                    fuente=frag.fuente,
                    seccion=frag.seccion,
                    texto=frag.texto,
                    puntaje=score,
                )
            )

    puntuados.sort(key=lambda f: (-f.puntaje, f.fuente, f.seccion))
    return puntuados[:k]
