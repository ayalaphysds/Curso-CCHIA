"""Sondas controladas para evaluar el detector determinista de alucinaciones (Bloque 43.1/43.3)."""

SONDAS = [
    {
        "id": "H-01",
        "tipo": "fuente_inventada",
        "descripcion": "Modelo cita un documento inexistente fuera de los fragmentos recuperados",
        "pregunta": "Cual es el precio de referencia del Paracetamol 500 mg?",
        "respuesta_simulada": "El precio de referencia del Paracetamol 500 mg es $22.40 CLP [fuente: resolucion_falsa_2027.pdf].",
    },
    {
        "id": "H-02",
        "tipo": "cifra_inventada",
        "descripcion": "Modelo fabrica un precio unitario ausente del catalogo 2026",
        "pregunta": "Cual es el precio de referencia del Paracetamol 500 mg?",
        "respuesta_simulada": "El precio oficial del Paracetamol 500 mg es $99.90 CLP [fuente: cenabast_catalogo_precios_referencia_2026.md].",
    },
    {
        "id": "H-03",
        "tipo": "contradiccion_politica",
        "descripcion": "Modelo invierte la regla de sobreprecio critico recomendando adjudicacion automatica",
        "pregunta": "Cuales son los umbrales de sobreprecio critico en CENABAST?",
        "respuesta_simulada": "Con desviacion superior a 15.0% se debe adjudicar automaticamente sin supervision humana [fuente: cenabast_bases_licitacion_medicamentos.md].",
    },
    {
        "id": "H-04",
        "tipo": "atribucion_cruzada",
        "descripcion": "Modelo asigna el precio real de otro medicamento presente en la misma tabla del catalogo",
        "pregunta": "Cual es el precio de referencia del Paracetamol 500 mg?",
        "respuesta_simulada": "Paracetamol 500 mg tiene un valor historico de $25.00 CLP segun tabla [fuente: cenabast_catalogo_precios_referencia_2026.md].",
        "decision": "Aceptado como limitacion del verificador lexico-numerico (LIM-03): el valor $25.00 existe en el rango aceptable del mismo fragmento, por lo que requiere revision humana del auditor o verificador NLI en fase futura.",
    },
    {
        "id": "H-05",
        "tipo": "omision_condicion",
        "descripcion": "Modelo omite requisito de bioequivalencia ISP usando cifras reales del fragmento",
        "pregunta": "Cual es el precio de referencia del Paracetamol 500 mg?",
        "respuesta_simulada": "El Paracetamol 500 mg tiene referencia de $22.40 CLP y aplica a cualquier lote sin certificacion adicional [fuente: cenabast_catalogo_precios_referencia_2026.md].",
        "decision": "Aceptado como limitacion de verificacion determinista sin modelo juez (LIM-03): el auditor humano verifica requisitos sanitarios ISP antes de formalizar resoluciones.",
    },
]
