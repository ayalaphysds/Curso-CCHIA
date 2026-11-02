"""
Banco de Prompts Estructurados con Salida JSON.
Especialización en IA Accenture - Curso CCHIA
Unidad U1.5 · Bloque 10: Prompt de sistema con salida JSON estructurada [Actividad Core]

Contiene el banco oficial de combinaciones de system_instruction, ejemplo_usuario,
claves_esperadas y response_schema para la miniaplicación de auditoría farmacéutica y compras públicas.
"""

BANCO_DE_PROMPTS = [
    {
        "nombre": "auditar_sobreprecio_farmaco",
        "descripcion": "Audita ofertas arancelarias de medicamentos contrastando contra mediana histórica y dispersión.",
        "system_instruction": (
            "Eres un auditor técnico de compras públicas hospitalarias de CENABAST. "
            "Tu tarea es evaluar si una oferta presenta sobreprecio respecto a la línea base histórica. "
            "Responde ÚNICAMENTE con un objeto JSON válido, sin bloques de código markdown ni texto adicional. "
            "El JSON debe tener exactamente las siguientes claves: "
            "'sobreprecio_detectado' (boolean: true si la oferta excede en más de 15% la mediana), "
            "'desviacion_porcentual' (number: porcentaje de desviación respecto a la mediana con 1 decimal), "
            "'recomendacion' (string: 'adjudicar', 'negociar' o 'rechazar'), "
            "'justificacion_corta' (string: dictamen técnico en un máximo de 25 palabras)."
        ),
        "ejemplo_usuario": (
            "Principio activo: PARACETAMOL 500 MG Comprimido. "
            "Precio ofertado por el laboratorio: $33.60 CLP. "
            "Mediana histórica de catálogo: $22.40 CLP. "
            "Coeficiente de variación histórico de mercado: 22.4%."
        ),
        "claves_esperadas": [
            "sobreprecio_detectado",
            "desviacion_porcentual",
            "recomendacion",
            "justificacion_corta",
        ],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "sobreprecio_detectado": {"type": "BOOLEAN"},
                "desviacion_porcentual": {"type": "NUMBER"},
                "recomendacion": {"type": "STRING"},
                "justificacion_corta": {"type": "STRING"},
            },
            "required": [
                "sobreprecio_detectado",
                "desviacion_porcentual",
                "recomendacion",
                "justificacion_corta",
            ],
        },
    },
    {
        "nombre": "evaluar_riesgo_proveedor",
        "descripcion": "Evalúa el riesgo logístico y de abastecimiento continuo de un proveedor farmacéutico.",
        "system_instruction": (
            "Eres un analista de gestión de riesgo en la cadena de suministro hospitalaria. "
            "Evalúa el desempeño de entrega de un proveedor y determina el riesgo de quiebre de stock. "
            "Responde ÚNICAMENTE con un objeto JSON válido, sin formato markdown ni texto complementario. "
            "El JSON debe tener exactamente estas claves: "
            "'nivel_riesgo' (string: 'bajo', 'medio' o 'critico'), "
            "'score_confiabilidad' (number: puntaje numérico del proveedor entre 0 y 100), "
            "'cuota_maxima_sugerida' (number: cuota anti-monopolio aconsejada entre 10 y 45 por ciento), "
            "'motivo_principal' (string: síntesis en una sola frase del riesgo detectado)."
        ),
        "ejemplo_usuario": (
            "Laboratorio oferente: Laboratorios Farmacéuticos del Sur. "
            "Tasa histórica de cumplimiento en plazo: 64.2%. "
            "Retraso logístico promedio: 18 días hábiles. "
            "Volumen ofertado: 45% de la demanda nacional de Ceftriaxona 1 G inyectable."
        ),
        "claves_esperadas": [
            "nivel_riesgo",
            "score_confiabilidad",
            "cuota_maxima_sugerida",
            "motivo_principal",
        ],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "nivel_riesgo": {"type": "STRING"},
                "score_confiabilidad": {"type": "NUMBER"},
                "cuota_maxima_sugerida": {"type": "NUMBER"},
                "motivo_principal": {"type": "STRING"},
            },
            "required": [
                "nivel_riesgo",
                "score_confiabilidad",
                "cuota_maxima_sugerida",
                "motivo_principal",
            ],
        },
    },
    {
        "nombre": "resumen_ejecutivo_licitacion",
        "descripcion": "Genera una síntesis ejecutiva de adjudicación con ahorro proyectado para la dirección nacional.",
        "system_instruction": (
            "Eres un asesor de adquisiciones públicas para la Dirección Nacional de Salud. "
            "Sintetiza la licitación farmacéutica informada y responde ÚNICAMENTE con un objeto JSON válido con estas claves: "
            "'id_licitacion' (string: código identificador del proceso), "
            "'ahorro_potencial_estimado_clp' (number: ahorro fiscal proyectado en CLP), "
            "'requiere_intervencion_urgente' (boolean: true si hay riesgo de monopolio o sobreprecio), "
            "'dictamen_ejecutivo' (string: recomendación directiva en exactamente dos oraciones)."
        ),
        "ejemplo_usuario": (
            "Proceso: LIC-2026-CARDIO-442. "
            "Insumo: Losartán 50 MG. "
            "Demanda total: 16.500.000 comprimidos. "
            "Oferta unitaria histórica adjudicada: $24.00 CLP. "
            "Oferta optimizada multi-proveedor: $18.50 CLP promedio. "
            "Número de laboratorios adjudicatarios: 2 firmas (60/40)."
        ),
        "claves_esperadas": [
            "id_licitacion",
            "ahorro_potencial_estimado_clp",
            "requiere_intervencion_urgente",
            "dictamen_ejecutivo",
        ],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "id_licitacion": {"type": "STRING"},
                "ahorro_potencial_estimado_clp": {"type": "NUMBER"},
                "requiere_intervencion_urgente": {"type": "BOOLEAN"},
                "dictamen_ejecutivo": {"type": "STRING"},
            },
            "required": [
                "id_licitacion",
                "ahorro_potencial_estimado_clp",
                "requiere_intervencion_urgente",
                "dictamen_ejecutivo",
            ],
        },
    },
]
