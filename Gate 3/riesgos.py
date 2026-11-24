"""Matriz de Riesgos de IA CENABAST con evidencia ejecutable y generador Markdown (Bloque 43.3 CORE)."""

from datetime import date
import hashlib
import json
from pathlib import Path
import sys

ESTADOS = ("verificada", "parcial", "aceptada")
SALIDA = Path("docs/matriz_riesgos.md")


def puntaje(probabilidad: int, impacto: int) -> int:
    return probabilidad * impacto


def residual(riesgo: dict) -> int:
    r = riesgo["residual"]
    return puntaje(r["probabilidad"], r["impacto"])


def categoria(valor: int) -> str:
    if valor >= 15:
        return "CRITICO"
    if valor >= 9:
        return "ALTO"
    if valor >= 4:
        return "MEDIO"
    return "BAJO"


RIESGOS = [
    {
        "id": "R-01",
        "riesgo": "Alucinacion de precios, fuentes inexistentes o contradiccion de umbrales CENABAST",
        "probabilidad": 4,
        "impacto": 5,
        "mitigacion": "Capa 4 de fundamentacion en servicio/cadena.py valida citas [fuente: ...], cifras contra fragmentos y contradicciones de politica; sondas H-04 y H-05 quedan bajo revision humana.",
        "evidencia": ["alucinacion:H-01", "alucinacion:H-02", "alucinacion:H-03"],
        "estado": "parcial",
        "residual": {"probabilidad": 2, "impacto": 5},
        "limites": ["H-04", "H-05"],
        "nota": "Las sondas semanticas H-04 (atribucion cruzada con cifras reales) y H-05 (omision de requisito ISP) escapan a reglas lexicas y se declaran en LIM-03.",
        "supervision": "Auditor de adquisiciones CENABAST revisa 100% de las minutas antes de adjudicar licitaciones y ejecuta registrar_alucinaciones.py en cada release.",
    },
    {
        "id": "R-02",
        "riesgo": "Inyeccion de prompts para forzar adjudicacion directa o exfiltrar instrucciones internas",
        "probabilidad": 4,
        "impacto": 5,
        "mitigacion": "Filtro bidireccional en servicio/seguridad.py sobre consultas y chunks recuperados + limpieza de salida.",
        "evidencia": ["ataques:A-01", "ataques:A-02", "ataques:A-03", "ataques:A-04", "ataques:A-05", "ataques:A-06"],
        "estado": "parcial",
        "residual": {"probabilidad": 2, "impacto": 4},
        "limites": ["A-07"],
        "nota": "Enmarcados hipoteticos sin patrones de override (A-07) se declaran en LIM-01; la salida sigue restringida al corpus y sin capacidad de adjudicacion.",
    },
    {
        "id": "R-03",
        "riesgo": "Exposicion de credenciales GEMINI_API_KEY en repositorio, imagen Docker o respuestas HTTP",
        "probabilidad": 3,
        "impacto": 5,
        "mitigacion": "Variables inyectadas solo en runtime (.env ignorado por Git y Docker), .env.example vacio y validacion en buscar_secretos.py.",
        "evidencia": ["comando:python buscar_secretos.py", "fuga:F-01"],
        "estado": "verificada",
        "residual": {"probabilidad": 1, "impacto": 4},
    },
    {
        "id": "R-04",
        "riesgo": "Fuga de datos personales (PII) o consultas sensibles en logs de observabilidad",
        "probabilidad": 3,
        "impacto": 4,
        "mitigacion": "Logger estructurado JSON en servicio/seguridad.py reemplaza texto crudo por longitudes y redacta correos/RUT.",
        "evidencia": ["fuga:F-02", "pruebas:tests/parciales/test_seguridad.py"],
        "estado": "verificada",
        "residual": {"probabilidad": 1, "impacto": 3},
    },
    {
        "id": "R-05",
        "riesgo": "Exposicion de instrucciones del sistema o trazas tecnicas ante entradas malformadas",
        "probabilidad": 3,
        "impacto": 3,
        "mitigacion": "Manejadores uniformes en servicio/errores.py (422/404/405/500) y limpiar_salida en servicio/seguridad.py.",
        "evidencia": ["fuga:F-03", "matriz:MP-04", "matriz:MP-05"],
        "estado": "verificada",
        "residual": {"probabilidad": 1, "impacto": 2},
    },
    {
        "id": "R-06",
        "riesgo": "Adjudicacion automatizada de ofertas con sobreprecio critico (> 15%) sin control humano",
        "probabilidad": 3,
        "impacto": 5,
        "mitigacion": "servicio/catalogo.py marca requiere_supervision=True sobre >15% y <-35%, prohibiendo adjudicacion automatica; el sistema nunca emite ordenes de compra.",
        "evidencia": ["matriz:MP-02", "pruebas:tests/parciales/test_catalogo.py"],
        "estado": "verificada",
        "residual": {"probabilidad": 1, "impacto": 5},
    },
    {
        "id": "R-07",
        "riesgo": "Caida silenciosa o simulacion oculta cuando falta clave del modelo real",
        "probabilidad": 3,
        "impacto": 4,
        "mitigacion": "servicio/respaldo.py devuelve HTTP 503 modelo_no_disponible por defecto y solo degrada si PERMITIR_RESPALDO=1 con advertencia explicita.",
        "evidencia": ["pruebas:tests/parciales/test_respaldo.py"],
        "estado": "verificada",
        "residual": {"probabilidad": 1, "impacto": 3},
    },
    {
        "id": "R-08",
        "riesgo": "Ejecucion de contenedores con privilegios root o imagenes no reproducibles (:latest)",
        "probabilidad": 3,
        "impacto": 4,
        "mitigacion": "Ambos Dockerfiles fijan python:3.12-slim, usuario no-root app, .dockerignore y HEALTHCHECK auditados por verificar_dockerfile.py.",
        "evidencia": ["comando:python verificar_dockerfile.py", "comando:python verificar_dockerfile.py interfaz/Dockerfile"],
        "estado": "verificada",
        "residual": {"probabilidad": 1, "impacto": 3},
    },
    {
        "id": "R-09",
        "riesgo": "Baja cobertura de recuperacion ante consultas en ingles o sinonimos coloquiales fuera del glosario CENABAST",
        "probabilidad": 3,
        "impacto": 3,
        "mitigacion": "Abstencion segura SIN_INFORMACION sin inventar datos; requiere usar principio activo en espanol segun catalogo ISP.",
        "evidencia": ["matriz_modelo:MP-08"],
        "estado": "aceptada",
        "residual": {"probabilidad": 3, "impacto": 3},
        "limites": ["MP-08", "T-05", "T-06"],
        "nota": "Aceptado para MVP determinista (LIM-02); la prueba de transferencia (T-05, T-06) y MP-08 confirman abstencion segura hasta integrar embeddings multilingues.",
        "supervision": "Jefatura tecnica revisa trimestralmente consultas sin cobertura para ampliar sinonimos farmaceuticos o activar indice vectorial multilingue.",
    },
]


def huella() -> str:
    crudo = json.dumps(RIESGOS, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(crudo.encode("utf-8")).hexdigest()[:12]


def renderizar_markdown() -> str:
    ordenados = sorted(RIESGOS, key=lambda r: (-residual(r), r["id"]))
    lineas = [
        "# Matriz de riesgos",
        "",
        f"Fecha: {date.today().isoformat()}",
        f"Huella de la matriz: {huella()}",
        f"Riesgos: {len(RIESGOS)}",
        "",
        "| ID | Riesgo | Inherente | Mitigacion | Evidencia | Estado | Residual | Supervision o nota |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in ordenados:
        inh = puntaje(r["probabilidad"], r["impacto"])
        res = residual(r)
        ev = ", ".join(r["evidencia"])
        sup_o_nota = r.get("supervision") or r.get("nota") or "Monitoreo en CI con verificar_riesgos.py"
        lineas.append(
            f"| {r['id']} | {r['riesgo']} | {inh} ({categoria(inh)}) | "
            f"{r['mitigacion'].replace('|', '/')} | {ev} | {r['estado']} | "
            f"{res} ({categoria(res)}) | {sup_o_nota.replace('|', '/')} |"
        )
    return "\n".join(lineas) + "\n"


def main() -> int:
    if "--escribir" in sys.argv:
        SALIDA.parent.mkdir(parents=True, exist_ok=True)
        SALIDA.write_text(renderizar_markdown(), encoding="utf-8")
        print(f"Escrito: {SALIDA} ({len(RIESGOS)} riesgos, huella {huella()})")
    else:
        for r in sorted(RIESGOS, key=lambda x: (-residual(x), x["id"])):
            print(
                f"{r['id']} | inh={puntaje(r['probabilidad'], r['impacto'])} | "
                f"res={residual(r)} ({categoria(residual(r))}) | estado={r['estado']}"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
