"""Utilidades de normalizacion y verificacion del diario de friccion (Bloque 44)."""

from pathlib import Path
import re
import sys
import unicodedata

SECCIONES_OBLIGATORIAS = (
    "requisitos",
    "instalacion",
    "configuracion",
    "arrancar",
    "comprobar",
    "pruebas",
    "decisiones",
    "limitaciones",
    "estructura",
    "problemas",
)


def normal(texto: str) -> str:
    sin_tildes = "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )
    return re.sub(r"\s+", " ", sin_tildes.lower()).strip()


def secciones(texto: str) -> dict[str, str]:
    patron = re.compile(r"^##\s+(.+)$", re.M)
    matches = list(patron.finditer(texto))
    salida: dict[str, str] = {}
    for i, m in enumerate(matches):
        titulo = normal(m.group(1))
        inicio = m.end()
        fin = matches[i + 1].start() if i + 1 < len(matches) else len(texto)
        salida[titulo] = texto[inicio:fin].strip()
    return salida


def faltantes_en_readme(texto: str) -> list[str]:
    secs = secciones(texto)
    titulos = list(secs.keys())
    return [clave for clave in SECCIONES_OBLIGATORIAS if not any(clave in t for t in titulos)]


def main() -> int:
    ruta = Path("README.md")
    if "--readme" in sys.argv:
        idx = sys.argv.index("--readme")
        if idx + 1 < len(sys.argv):
            ruta = Path(sys.argv[idx + 1])
    if not ruta.is_file():
        print(f"FALLA: no existe {ruta}")
        return 1
    faltan = faltantes_en_readme(ruta.read_text(encoding="utf-8"))
    if faltan:
        print(f"FALLA: faltan secciones del diario en {ruta}: {faltan}")
        return 1
    print(f"{ruta} tiene las {len(SECCIONES_OBLIGATORIAS)} secciones del diario")
    return 0


if __name__ == "__main__":
    sys.exit(main())
