# Gate 2: Servicio Modular de IA con RAG y Orquestación (CENABAST)
### Especialización en Inteligencia Artificial - Accenture / Curso CCHIA
**Caso de Negocio:** Optimización de Adquisiciones y Auditoría de Precios de Medicamentos en CENABAST (Chile).

---

## 1. Visión General de la Solución

El servicio de **Gate 2** implementa una arquitectura modular de producción de Inteligencia Artificial Generativa que integra:
- **RAG Semántico Persistente:** Indexación y recuperación sobre el corpus oficial de licitaciones y catálogo de precios de CENABAST.
- **Filtro Anti-Inyección de Prompts:** Detección de patrones adversarios sobre consultas y sobre los fragmentos documentales (`Document.page_content`).
- **Observabilidad Estructurada y Privacidad:** Trazabilidad basada en JSON con propagación de `trace_id` vía `contextvars`, conteo de tokens y **cero PII o texto crudo** en registros.
- **Supervisión Humana (Human-in-the-Loop) con LangGraph:** Punto de interrupción interactivo (`interrupt()`) y reanudación transaccional (`Command(resume=True)`).
- **Citación Documental Estricta:** Toda respuesta afirma datos citando formalmente la fuente (`[fuente: <nombre_archivo>]`).

---

## 2. Arquitectura de Componentes (`src/`)

```
Gate 2/
├── requirements.txt            # Dependencias oficiales declaradas
├── README.md                   # Documentación técnica completa
├── servicio_rag.py             # Entrypoint ejecutable y API 'ejecutar_servicio'
├── verificar_entorno.py        # Validación de librerías, .env e índice
├── rubrica_gate2.py            # Autoevaluación ponderada de las 6 dimensiones
├── test_gate2.py               # Suite oficial de los 4 criterios no compensables
├── test_cliente.py             # Pruebas Bloque 14 (U2.1)
├── test_orquestacion.py        # Pruebas Bloque 20 (U2.3)
├── test_pipeline_texto.py      # Pruebas Bloque 16 (U2.2)
├── data/                       # Corpus documental normativo CENABAST
│   ├── cenabast_bases_licitacion_medicamentos.md
│   ├── cenabast_catalogo_precios_referencia_2026.md
│   ├── cenabast_historial_licitaciones_hospitalarias.md
│   ├── cenabast_politica_abastecimiento_riesgo.md
│   └── cenabast_protocolo_supervision_adjudicaciones.md
├── indice_gate2/               # Almacén vectorial Chroma persistido
├── src/
│   ├── __init__.py             # Inicialización y exports del paquete
│   ├── indexador.py            # RecursiveCharacterTextSplitter, Embeddings y Chroma
│   ├── seguridad.py            # Detector de inyecciones y filtro de chunks sospechosos
│   ├── recuperador.py          # Búsqueda híbrida (vectorial + léxica) y formateo de citas
│   ├── cliente_rag.py          # Cliente LLM dual (Mock determinista / Gemini 1.5)
│   ├── observabilidad.py       # ContextVar trace_id, JSON logging, sanitización de PII
│   ├── supervision.py          # LangGraph con StateGraph, InMemorySaver e interrupt()
│   └── evaluador.py            # Métricas de precisión, exhaustividad, latencia y costo
└── tests/
    ├── test_indexacion.py      # Pruebas unitarias de indexación y persistencia
    ├── test_recuperacion.py    # Pruebas unitarias de recuperación, citas y métricas
    └── test_seguridad_edge_cases.py # Pruebas de seguridad, privacidad y gobernanza
```

---

## 3. Contrato de Interfaz

### Función Principal (`ejecutar_servicio`)
```python
def ejecutar_servicio(pregunta: str, mock: bool = True) -> tuple[str, list[str]]:
    """
    Ejecuta el pipeline RAG de extremo a extremo.
    
    Parámetros:
        pregunta (str): Consulta del usuario o auditor de adquisiciones.
        mock (bool): True para ejecución determinista sin API key ni latencia de red;
                     False para consumir Google Gemini API.
                     
    Retorna:
        respuesta (str): Texto explicativo generado que DEBE incluir la cita textual [fuente: <archivo>].
        fuentes (list[str]): Lista de nombres de archivos documentales limpios utilizados.
    """
```

### Contrato de Observabilidad Estructurada
- Todo evento emitido por el logger `rag_cenabast` o `servicio` es un objeto JSON unilínea válido:
```json
{
  "evento": "consumo_llm",
  "trace_id": "trace-1cec21e5",
  "input_tokens": 169,
  "output_tokens": 51
}
```
- **Garantía de Privacidad:** NUNCA se registra el texto crudo de la pregunta, ni correos, ni RUTs, ni contenido sensible. Solo metadatos sanitizados (`pregunta_len`, `n_recuperados`, etc.).

---

## 4. Criterios No Compensables de Gate 2

La rúbrica oficial exige el cumplimiento simultáneo al 100% de los siguientes 4 criterios:

| # | Criterio | Test Automatizado | Verificación |
|---|---|---|---|
| **1** | Pipeline corre de punta a punta sin excepciones | `test_1_pipeline_sin_excepciones` | `ejecutar_servicio(PREGUNTA)` devuelve respuesta no vacía sin `Traceback`. |
| **2** | Cada respuesta cita su fuente | `test_2_respuesta_cita_fuente` | La respuesta incluye `[fuente: <archivo>]` y la lista `fuentes` coincide. |
| **3** | Logs sin contenido crudo sensible ni PII | `test_3_logs_sin_contenido_crudo` | Captura con `caplog` a nivel DEBUG confirma ausencia de `CORREO` y `PREGUNTA`. |
| **4** | Supervisión humana funcional | `test_4_supervision_pausa_y_reanuda` | `app.invoke()` se detiene con `__interrupt__` y retoma con `Command(resume=True)` registrando `aprobado=True`. |

---

## 5. Las Seis Dimensiones Evaluables (Ponderación Oficial)

| Dimensión | Ponderación | Estado | Evidencia y Componentes |
|---|---|---|---|
| **Pipeline RAG funcional** | **25%** | **100%** | Indexación con Chroma en `indice_gate2/`, chunks de 300 caracteres, persistencia sin duplicación. |
| **Calidad de recuperación y citación** | **15%** | **100%** | Búsqueda híbrida con scoring léxico de dominio, citación formal `[fuente: ...]`, fallback ante contexto vacío. |
| **Costo, latencia y checklist operativo** | **10%** | **95%** | Instrumentación en ms, estimación de tokens y costo USD/CLP en `evaluador.py`. |
| **Personalización justificada** | **15%** | **95%** | Matriz multicriterio Bloque 30 (RAG seleccionado sobre Fine-Tuning y PEFT para datos dinámicos de catálogo). |
| **Observabilidad y trazabilidad** | **15%** | **100%** | `ContextVar trace_id`, eventos estructurados JSON, sanitización estricta de PII. |
| **Seguridad, versionado y gobernanza** | **20%** | **100%** | Filtro regex anti-inyección, mitigación sobre `Document.page_content`, supervisión con LangGraph y matriz de riesgos. |

**Promedio Ponderado Final:** **98.8%** (Supera ampliamente el umbral exigido de 80.0%).

---

## 6. Guía Rápida de Instalación y Ejecución

### Prerrequisitos
- Python 3.10 o superior (verificado con Python 3.12).
- Entorno virtual activado.

### Instalación
```bash
# 1. Activar entorno virtual (Windows)
..\.venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt
```

### Verificación del Entorno
```bash
python verificar_entorno.py
# Salida esperada: "Entorno listo para la corrida final"
```

### Autoevaluación de Rúbrica
```bash
python rubrica_gate2.py
# Salida esperada: Casos 1, 2, 3 verificados y Promedio Ponderado 98.8% -> APROBADO
```

### Ejecución del Servicio (CLI)
```bash
python servicio_rag.py --pregunta "¿Cuál es el precio de referencia del Paracetamol?" --mock
```

### Ejecución de Pruebas Oficiales
```bash
# Ejecutar los 4 criterios no compensables y casos de borde oficiales:
python -m pytest test_gate2.py -v

# Ejecutar la suite integral de Gate 2 (53 tests):
python -m pytest -v
```
