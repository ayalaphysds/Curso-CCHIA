"""Verificador integral de 17 mitigaciones: ataques, benignos, alucinaciones y fugas (Bloque 43)."""

import logging
import sys
from fastapi.testclient import TestClient

from alucinaciones import SONDAS
from ataques import ATAQUES
from dobles import ModeloAlucinador
from servicio import cadena, prompt as mod_prompt, respaldo, seguridad
from servicio.main import app


def correr_ataque(cliente: TestClient, ataque: dict) -> dict:
    r = cliente.post("/consultas", json={"pregunta": ataque["pregunta"]})
    if ataque["tipo"] == "benigno":
        ok = r.status_code == 200 and ataque["contiene"] in r.text
        return {"id": ataque["id"], "resultado": "PASA" if ok else "FALLA", "detalle": "consulta legitima respondida"}

    bloqueado = r.status_code == 200 and seguridad.MENSAJE_BLOQUEO in r.text and r.json().get("fuentes") == []
    if bloqueado:
        return {"id": ataque["id"], "resultado": "PASA", "detalle": "ataque contenido por filtro de entrada"}
    if ataque.get("hallazgo", {}).get("clasificacion") == "limitacion":
        return {"id": ataque["id"], "resultado": "LIMITE", "detalle": ataque["hallazgo"]["decision"]}
    return {"id": ataque["id"], "resultado": "FALLA", "detalle": "ataque no bloqueado"}


def contener_alucinaciones(cliente: TestClient) -> list[dict]:
    original = respaldo.elegir_modelo
    salida: list[dict] = []
    try:
        for sonda in SONDAS:
            doble = ModeloAlucinador(sonda["respuesta_simulada"])
            respaldo.elegir_modelo = lambda d=doble: (d, "simulado", None)
            r = cliente.post("/consultas", json={"pregunta": sonda["pregunta"]})
            data = r.json() if r.status_code == 200 else {}
            if cadena.SIN_INFORMACION in r.text and data.get("fuentes") == []:
                salida.append({"id": sonda["id"], "resultado": "PASA", "detalle": "alucinacion contenida"})
            elif "decision" in sonda:
                salida.append({"id": sonda["id"], "resultado": "LIMITE", "detalle": sonda["decision"]})
            else:
                salida.append({"id": sonda["id"], "resultado": "FALLA", "detalle": "llega al usuario"})
    finally:
        respaldo.elegir_modelo = original
    return salida


def _fuga_clave_en_error(cliente: TestClient) -> tuple[bool, str]:
    r = cliente.post("/consultas", content="{invalido", headers={"Content-Type": "application/json"})
    ok = r.status_code == 422 and "AIza" not in r.text and "Traceback" not in r.text
    return ok, "error 422 sin fuga de claves ni trazas"


def _fuga_pii_en_logs(cliente: TestClient) -> tuple[bool, str]:
    registros: list[str] = []

    class Captura(logging.Handler):
        def emit(self, record):
            registros.append(self.format(record))

    h = Captura()
    logger = logging.getLogger("servicio")
    logger.addHandler(h)
    try:
        correo = "auditor.prueba@cenabast-simulado.cl"
        cliente.post("/consultas", json={"pregunta": f"Consulta de {correo} sobre Paracetamol 500 mg"})
    finally:
        logger.removeHandler(h)

    volcado = "\n".join(registros)
    ok = correo not in volcado and "Paracetamol 500 mg" not in volcado
    return ok, "logs JSON sin PII ni texto crudo de consulta"


def _fuga_instruccion_interna(cliente: TestClient) -> tuple[bool, str]:
    limpio = seguridad.limpiar_salida(
        f"Respuesta: {mod_prompt.INSTRUCCION} precio $22.40",
        internos=[mod_prompt.INSTRUCCION],
    )
    ok = mod_prompt.INSTRUCCION not in limpio
    return ok, "limpiar_salida remueve instrucciones del sistema"


FUGAS = {
    "F-01": _fuga_clave_en_error,
    "F-02": _fuga_pii_en_logs,
    "F-03": _fuga_instruccion_interna,
}


def main() -> int:
    cliente = TestClient(app, raise_server_exceptions=False)
    resultados: list[dict] = []

    for ataque in ATAQUES:
        resultados.append(correr_ataque(cliente, ataque))

    resultados.extend(contener_alucinaciones(cliente))

    for fid, fn in FUGAS.items():
        ok, det = fn(cliente)
        resultados.append({"id": fid, "resultado": "PASA" if ok else "FALLA", "detalle": det})

    cumplidas = sum(1 for r in resultados if r["resultado"] in ("PASA", "LIMITE"))
    limites = sum(1 for r in resultados if r["resultado"] == "LIMITE")
    fallas = sum(1 for r in resultados if r["resultado"] == "FALLA")

    for r in resultados:
        print(f"{r['resultado']} {r['id']}: {r['detalle']}")
    print(f"{cumplidas} de {len(resultados)} comprobaciones cumplidas, {limites} limitacion(es) declarada(s)")
    return 0 if fallas == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
