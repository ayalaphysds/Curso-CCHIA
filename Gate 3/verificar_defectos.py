"""Helper de pruebas de mutacion controlada sobre copia temporal (Bloque 39.3)."""

from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


def main() -> int:
    if len(sys.argv) != 5:
        print('Uso: python verificar_defectos.py ARCHIVO "TEXTO_ACTUAL" "TEXTO_NUEVO" PRUEBA')
        return 2

    archivo_rel, actual, nuevo, prueba_rel = sys.argv[1:5]
    archivo = Path(archivo_rel)
    prueba = Path(prueba_rel)
    if not archivo.is_file() or not prueba.is_file():
        print(f"ERROR: archivo o prueba inexistente ({archivo_rel}, {prueba_rel})")
        return 2

    contenido = archivo.read_text(encoding="utf-8")
    veces = contenido.count(actual)
    if veces != 1:
        print(f"ERROR: el texto objetivo aparece {veces} veces en {archivo_rel} (debe aparecer exactamente 1)")
        return 2

    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / "repo"
        shutil.copytree(
            ".",
            copia,
            ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", ".git", ".venv"),
        )
        destino = copia / archivo_rel
        destino.write_text(contenido.replace(actual, nuevo, 1), encoding="utf-8")
        r = subprocess.run(
            [sys.executable, "-m", "pytest", prueba_rel, "-q", "--tb=no"],
            cwd=copia,
            capture_output=True,
            text=True,
        )
        fallas = re.findall(r"(?m)^FAILED (\S+)", r.stdout + "\n" + r.stderr)
        if r.returncode != 0 and fallas:
            print(f"DETECTADO: {len(fallas)} prueba(s) atraparon el defecto ({', '.join(fallas)})")
            return 0
        print("NO DETECTADO: ninguna prueba fallo al introducir el defecto")
        return 1


if __name__ == "__main__":
    sys.exit(main())
