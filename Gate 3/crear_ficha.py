"""Genera el esqueleto inicial de la Ficha de Diseno Funcional sin sobrescribir (Bloque 33.3)."""

from pathlib import Path

DESTINO = Path("docs/ficha_diseno_funcional.md")

PLANTILLA = """# Ficha de Diseño Funcional

## 1. Problema de negocio

[COMPLETAR: problema de negocio, costo actual con estimación y resultado esperado]

## 2. Requerimientos y alcance (MVP)

### Requerimientos funcionales

- RF-01: [COMPLETAR]

### Requerimientos no funcionales

- RNF-01: [COMPLETAR con dato numérico]

### Alcance

Imprescindible: RF-01
Deseable:
Fuera de alcance:

## 3. Arquitectura de la solución

Diagrama: docs/diagrama_arquitectura.png

## 4. Criterios de aceptación

[PENDIENTE: se completa en el Bloque 34]

## 5. Plan de construcción por hitos

[PENDIENTE: se completa en el Bloque 34]
"""


def main() -> None:
    if DESTINO.exists():
        raise SystemExit(f"Ya existe {DESTINO}. No se sobrescribe para proteger tu trabajo.")
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(PLANTILLA, encoding="utf-8")
    print(f"Plantilla creada en {DESTINO}")


if __name__ == "__main__":
    main()
