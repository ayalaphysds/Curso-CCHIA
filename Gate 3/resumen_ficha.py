"""Imprime estadisticas objetivas de la Ficha de Diseno Funcional (Bloque 34.2)."""

from ficha_datos import cargar_ficha


def main() -> None:
    ficha = cargar_ficha()
    imp = ficha["alcance"].get("Imprescindible", [])
    des = ficha["alcance"].get("Deseable", [])
    fuera = ficha["alcance"].get("Fuera de alcance", [])

    cubiertos_por_ca = {ref for c in ficha["criterios"] for ref in c["refs"]}
    esperados = set(imp) | set(ficha["rnf"].keys())
    sin_criterio = sorted(esperados - cubiertos_por_ca)

    cas_en_hitos = {ca for h in ficha["hitos"] for ca in h["criterios"]}
    todos_cas = {c["id"] for c in ficha["criterios"]}
    cas_sin_hito = sorted(todos_cas - cas_en_hitos)
    hitos_sin_ca = [h["id"] for h in ficha["hitos"] if not h["criterios"]]

    horas_plan = sum(h["horas"] for h in ficha["hitos"])
    disp = ficha["horas_disponibles"]
    marg = ficha["margen_imprevistos"]

    print(f"RF: {len(ficha['rf'])} | RNF: {len(ficha['rnf'])}")
    print(f"Alcance: {len(imp)} imprescindibles, {len(des)} deseables, {len(fuera)} fuera de alcance")
    print(f"Criterios de aceptacion: {len(ficha['criterios'])}")
    print(f"Imprescindibles y RNF sin criterio: {', '.join(sin_criterio) if sin_criterio else 'ninguno'}")
    print(f"Hitos: {len(ficha['hitos'])}")
    print(f"Horas planificadas: {horas_plan:.1f} h (disponibles: {disp} h, margen: {marg} h)")
    print(f"Criterios que ningun hito comprueba: {', '.join(cas_sin_hito) if cas_sin_hito else 'ninguno'}")
    print(f"Hitos sin criterio: {', '.join(hitos_sin_ca) if hitos_sin_ca else 'ninguno'}")


if __name__ == "__main__":
    main()
