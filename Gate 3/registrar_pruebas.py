"""Valida cobertura de CASOS, ejecuta contra HTTP real y genera docs/registro_pruebas.md (Bloque 36.3)."""

from datetime import date
import json
from pathlib import Path
import sys
import httpx

from casos import CASOS, ejecutar_caso

SALIDA = Path("docs/registro_pruebas.md")


def verificar_cobertura(casos: list[dict]) -> list[str]:
    errores: list[str] = []
    validos = [c for c in casos if c["id"].startswith("V-")]
    invalidos = [c for c in casos if c["id"].startswith("I-")]
    if len(validos) < 3:
        errores.append(f"Se requieren al menos 3 casos validos (V-); hay {len(validos)}")
    if len(invalidos) < 5:
        errores.append(f"Se requieren al menos 5 casos invalidos (I-); hay {len(invalidos)}")
    estados_inv = {c["estado"] for c in invalidos}
    faltantes = {404, 405, 422} - estados_inv
    if faltantes:
        errores.append(f"Faltan codigos de error obligatorios en casos invalidos: {sorted(faltantes)}")
    return errores


def formatear_peticion(caso: dict) -> str:
    base = f"{caso['metodo']} {caso['ruta']}"
    if "json" in caso:
        return f"{base} {json.dumps(caso['json'], ensure_ascii=False)}"
    if "contenido" in caso:
        return f"{base} `{caso['contenido']}`"
    return base


def main() -> int:
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    errores = verificar_cobertura(CASOS)
    if errores:
        for e in errores:
            print(f"ERROR cobertura: {e}")
        return 1

    try:
        filas = []
        cumplidos = 0
        with httpx.Client(base_url=base_url, timeout=5.0) as cliente:
            for caso in CASOS:
                ok, obtenido, _ = ejecutar_caso(cliente, caso)
                if ok:
                    cumplidos += 1
                pet = formatear_peticion(caso).replace("|", "/")
                filas.append(
                    f"| {caso['id']} | {caso['descripcion']} | {pet} | "
                    f"{caso['estado']} | {obtenido} | {'PASA' if ok else 'FALLA'} |"
                )
    except httpx.ConnectError:
        print(f"No se pudo conectar con {base_url}. Arranca el servicio antes de registrar pruebas.")
        return 1

    encabezado = [
        "# Registro de pruebas de la API",
        "",
        f"Fecha: {date.today().isoformat()}",
        f"Servicio probado: {base_url} (cliente: httpx)",
        f"Resultado: {cumplidos} de {len(CASOS)} casos cumplidos",
        "",
        "| Caso | Descripción | Petición | Esperado | Obtenido | Resultado |",
        "|---|---|---|---|---|---|",
    ]
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text("\n".join(encabezado + filas) + "\n", encoding="utf-8")
    print(f"Registro escrito en {SALIDA}: {cumplidos} de {len(CASOS)} casos")
    return 0 if cumplidos == len(CASOS) else 1


if __name__ == "__main__":
    sys.exit(main())
