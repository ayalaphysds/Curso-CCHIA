"""Cliente HTTP externo que ejecuta la tabla CASOS contra un servidor real (Bloque 36.2)."""

import sys
import httpx

from casos import CASOS, ejecutar_caso


def main() -> int:
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    try:
        with httpx.Client(base_url=base_url, timeout=5.0) as cliente:
            salud = cliente.get("/salud")
            if salud.status_code != 200:
                print(f"FALLA /salud devolvio HTTP {salud.status_code}")
                return 1

            cumplidos = 0
            for caso in CASOS:
                ok, estado, _ = ejecutar_caso(cliente, caso)
                marca = "PASA" if ok else "FALLA"
                if ok:
                    cumplidos += 1
                print(f"{marca} {caso['id']} ({caso['metodo']} {caso['ruta']}): esperado={caso['estado']} obtenido={estado}")

            print(f"{cumplidos} de {len(CASOS)} casos cumplidos")
            return 0 if cumplidos == len(CASOS) else 1
    except httpx.ConnectError:
        print(f"No se pudo conectar con {base_url}. Verifica que el servidor FastAPI este en ejecucion.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
