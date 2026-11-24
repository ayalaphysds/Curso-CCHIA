"""Adaptador dual de modelo generativo (Simulado determinista y Gemini API real)."""

import re
import httpx

from servicio.contratos import Fragmento
from servicio.recuperador import normalizar


class ModeloSimulado:
    """Generador determinista fundamentado en fragmentos CENABAST (cero red, cero costo)."""

    nombre = "simulado"

    def generar(self, prompt: str, pregunta: str = "", fragmentos: list[Fragmento] | None = None) -> str:
        frags = fragmentos or []
        if not frags:
            return "No encuentro esa informacion en la documentacion oficial de CENABAST."

        q = normalizar(pregunta or prompt)
        principal = frags[0]
        fuente = principal.fuente
        texto = principal.texto

        # 1. Precios de referencia de medicamentos (tabla de catalogo 2026)
        if "| **51" in texto:
            partes = [p.strip().replace("**", "") for p in texto.strip("|").split("|")]
            if len(partes) >= 7:
                cod, nombre, forma, unidad, mediana, rango, consumo = partes[:7]
                return (
                    f"Segun el catalogo oficial 2026 de CENABAST, {nombre} ({forma}, codigo ONU {cod}) "
                    f"tiene una mediana historica de referencia de {mediana} por {unidad.lower()}, "
                    f"con un rango aceptable de {rango} y un consumo anual estimado de {consumo} unidades "
                    f"[fuente: {fuente}]."
                )

        # 2. Umbrales de desviacion y sobreprecio
        if any(k in q for k in ("sobreprecio", "umbral", "negociacion", "temerario", "temeraria", "desviacion")):
            if "UMBRALES DE DESVIACIÓN" in texto.upper() or "SOBREPRECIO CRÍTICO" in texto.upper():
                return (
                    "Los umbrales operativos de CENABAST respecto al catalogo de referencia son: "
                    "rango competitivo aceptable <= 5.0%, negociacion obligatoria entre 5.0% y 15.0%, "
                    "sobreprecio critico > 15.0% (con prohibicion de adjudicacion automatizada y supervision humana obligatoria) "
                    "y precios temerarios < -35.0% "
                    f"[fuente: {fuente}]."
                )

        # 3. Multas por atraso y cadena de frio
        if any(k in q for k in ("multa", "multas", "atraso", "frio", "temperatura")):
            if "MULTAS POR ATRASO" in texto.upper() or "CADENA DE FRÍO" in texto.upper():
                return (
                    "Por atraso ordinario CENABAST aplica una multa de 1.0% diario del valor neto con tope del 15.0% "
                    "y posible rescision a los 15 dias corridos; ante incumplimiento de cadena de frio (2 a 8 grados C) "
                    "se rechaza el 100% del embarque con 48 horas para reposicion "
                    f"[fuente: {fuente}]."
                )

        # 4. Cupos maximos / concentracion / INCL
        if any(k in q for k in ("cupo", "concentracion", "incl", "cumplimiento", "logistico")):
            if "ANTI-CONCENTRACIÓN" in texto.upper() or "45.0%" in texto:
                return (
                    "Para mitigar riesgo de quiebre de stock, ningun proveedor individual puede adjudicarse mas del 45.0% "
                    "del volumen anual licitado si existen otros oferentes calificados, y debe acreditar reserva de seguridad "
                    "equivalente a 60 dias de consumo "
                    f"[fuente: {fuente}]."
                )
            if "INCL" in texto.upper() or "85.0%" in texto:
                return (
                    "El Indicador de Nivel de Cumplimiento Logistico (INCL) exige una tasa minima aceptable de 85.0% "
                    "acumulado semestral; proveedores entre 70.0% y 84.9% entran en auditoria semanal "
                    f"[fuente: {fuente}]."
                )

        # 5. Ponderacion de licitacion
        if any(k in q for k in ("ponderacion", "criterios", "evaluacion", "puntaje")):
            if "60%" in texto and "20%" in texto:
                return (
                    "La matriz de ponderacion de licitaciones CENABAST asigna 60% a oferta economica, "
                    "20% a plazo de entrega (< 10 dias corridos), 15% a calidad tecnica y registro ISP, "
                    "y 5% a requisitos formales "
                    f"[fuente: {fuente}]."
                )

        # 6. Supervision humana / LangGraph
        if any(k in q for k in ("supervision", "humana", "interrupt", "langgraph", "riesgo alto")):
            return (
                "Las operaciones de riesgo alto (adjudicacion formal de ordenes de compra, sobreprecio > 15%, "
                "multas y compras de emergencia) exigen interrupcion inmediata mediante interrupt() y aprobacion "
                "humana explicita con Command(resume=True) o rechazo con Command(resume=False) "
                f"[fuente: {fuente}]."
            )

        # 7. Resumen extractivo seguro directamente del fragmento principal
        lineas = [
            re.sub(r"[#*_`]+", "", ln).strip()
            for ln in texto.splitlines()
            if ln.strip() and not ln.strip().startswith("---")
        ]
        extracto = " ".join(lineas[:4])[:360].strip()
        return f"Segun la documentacion oficial de CENABAST: {extracto} [fuente: {fuente}]."


class ModeloGemini:
    """Cliente HTTP para Google Gemini API (activado solo con MODELO=real y GEMINI_API_KEY)."""

    nombre = "real"

    def __init__(self, api_key: str, modelo_id: str = "gemini-2.0-flash") -> None:
        self.api_key = api_key
        self.modelo_id = modelo_id

    def generar(self, prompt: str, pregunta: str = "", fragmentos: list[Fragmento] | None = None) -> str:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.modelo_id}:generateContent?key={self.api_key}"
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.1, "maxOutputTokens": 400},
        }
        r = httpx.post(url, json=payload, timeout=15.0)
        r.raise_for_status()
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
