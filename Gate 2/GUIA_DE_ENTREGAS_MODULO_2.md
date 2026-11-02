# GUÍA INTEGRAL DE ENTREGAS Y EVIDENCIAS - MÓDULO 2 (CONSTRUCCIÓN DE COMPONENTES IA)
**Especialización en Inteligencia Artificial Generativa - Accenture / CCHIA**  
**Proyecto Aplicado:** Asistente Inteligente de Auditoría de Precios y Licitaciones CENABAST  
**Alumno:** Sebastián Ayala  
**Entorno de Trabajo:** `Curso-CCHIA/Gate 2`  
**Versión de la Guía:** 2.0 (Consolidada para Evaluación y Aprobación en Plataforma Skillnest)

---

## 📌 PROPÓSITO DE ESTA GUÍA
Esta guía contiene las instrucciones exactas, paso a paso, para cada una de las **Actividades Core Sumativas** del Módulo 2 y la preparación del **Gate 2**. Para cada actividad se detalla:
1. **Identificación Curricular:** Nombre de la unidad y bloque.
2. **Contexto de Negocio CENABAST:** Problema de auditoría farmacéutica que resuelve el componente.
3. **Entregables de Código y Documentación:** Archivos exactos requeridos.
4. **Comandos de Terminal:** Comandos exactos para Windows PowerShell / CMD.
5. **Salida Esperada en Consola:** Salida estándar que debe visualizarse.
6. **Evidencia para Skillnest:** Qué captura de pantalla o enlace subir a la plataforma.
7. **Checklist de Aprobación:** Criterios con los que el evaluador calificará la entrega.

---

## ÍNDICE RÁPIDO DE ACTIVIDADES CORE
- [Actividad Core 1 (Bloque 14 · U2.1): Pruebas Unitarias del Cliente Modular](#actividad-core-1-bloque-14--u21-pruebas-unitarias-del-cliente-modular)
- [Actividad Core 2 (Bloque 17 · U2.2): Interpretación Cualitativa y Límites del Pipeline](#actividad-core-2-bloque-17--u22-interpretación-cualitativa-y-límites-del-pipeline)
- [Actividad Core 3 (Bloque 20 · U2.3): Manejo de Errores por Paso y Orquestación](#actividad-core-3-bloque-20--u23-manejo-de-errores-por-paso-y-orquestación)
- [Actividad Core 4 (Bloque 23 · U2.4): Límites de Autonomía del Agente y Supervisión Humana](#actividad-core-4-bloque-23--u24-límites-de-autonomía-del-agente-y-supervisión-humana)
- [Actividad Core 5 (Bloque 28 · U2.5): Latencia y Costo del Flujo RAG](#actividad-core-5-bloque-28--u25-latencia-y-costo-del-flujo-rag)
- [Actividad Core 6 (Bloque 30 · U2.6): Decisión Fundamentada de Personalización](#actividad-core-6-bloque-30--u26-decisión-fundamentada-de-personalización)
- [Actividad Core 7 (Bloque 32 · U2.7): Matriz de Riesgos y Versionado de Prompts](#actividad-core-7-bloque-32--u27-matriz-de-riesgos-y-versionado-de-prompts)
- [Hito Final Gate 2 (Bloque S1 · U2.8): Servicio RAG Modular e Integrado](#hito-final-gate-2-bloque-s1--u28-servicio-rag-modular-e-integrado)

---

## ACTIVIDAD CORE 1 (BLOQUE 14 · U2.1): PRUEBAS UNITARIAS DEL CLIENTE MODULAR

### 1. Ficha Curricular
- **Unidad:** U2.1 - APIs y Cliente Modular.
- **Lección / Bloque:** Bloque 14 — *Pruebas unitarias sobre el cliente modular*.
- **Tipo de Actividad:** Actividad Core Sumativa Obligatoria.

### 2. Contexto de Negocio CENABAST
El cliente HTTP de consulta de modelos generativos debe ser tolerante a fallas y predecible. En compras hospitalarias de alta urgencia, no se puede tolerar un fallo silencioso ni reintentar infinitamente ante claves inválidas (401/403). Se requiere una suite rigurosa que verifique clasificación temprana de errores, reintentos con backoff, reseteo del acumulador de costo de tokens y encapsulación a `RuntimeError`.

### 3. Entregables
- `Gate 2/cliente.py` (cliente modular con `registrar_costo` y `reiniciar_costo`).
- `Gate 2/test_cliente.py` (suite de al menos 7 pruebas unitarias; implementadas 10 pruebas con mocks 100% offline).

### 4. Comando de Ejecución
Abrir PowerShell en la raíz del repositorio y ejecutar:
```powershell
cd "Gate 2"
..\.venv\Scripts\python.exe -m pytest test_cliente.py -v
```
*(O alternativamente: `python -m unittest test_cliente.py`)*

### 5. Salida Esperada en Terminal
```text
============================= test session starts =============================
collected 10 items

test_cliente.py::TestClienteModularCENABAST::test_con_reintento_agota_reintentos_y_propaga_timeout_error PASSED [ 10%]
test_cliente.py::TestClienteModularCENABAST::test_con_reintento_no_reintenta_ante_value_error PASSED [ 20%]
test_cliente.py::TestClienteModularCENABAST::test_con_reintento_reintenta_y_recupera_exito PASSED [ 30%]
test_cliente.py::TestClienteModularCENABAST::test_consultar_modelo_convierte_agotamiento_en_runtime_error PASSED [ 40%]
test_cliente.py::TestClienteModularCENABAST::test_consultar_modelo_propaga_value_error_directamente PASSED [ 50%]
test_cliente.py::TestClienteModularCENABAST::test_enviar_peticion_clasifica_400_api_key_invalid_como_value_error PASSED [ 60%]
test_cliente.py::TestClienteModularCENABAST::test_enviar_peticion_clasifica_401_403_como_value_error PASSED [ 70%]
test_cliente.py::TestClienteModularCENABAST::test_enviar_peticion_clasifica_429_como_timeout_error PASSED [ 80%]
test_cliente.py::TestClienteModularCENABAST::test_enviar_peticion_clasifica_500_y_falla_de_red_como_timeout_error PASSED [ 90%]
test_cliente.py::TestClienteModularCENABAST::test_registrar_costo_acumula_correctamente_y_resetea PASSED [100%]

============================= 10 passed in 0.04s ==============================
```

### 6. Qué Evidencia Subir a Skillnest
1. **Captura de Pantalla:** Terminal completa mostrando la ejecución del comando `pytest test_cliente.py -v` con los 10 tests en verde (`PASSED [100%]`) y tiempo de ejecución menor a 1 segundo.
2. **Enlace a GitHub:** URL directa a `Gate 2/test_cliente.py` en tu repositorio.

### 7. Checklist de Aprobación
- [x] Contiene al menos 7 pruebas unitarias automatizadas (implementadas 10).
- [x] Ejecución 100% offline mediante `unittest.mock` sin consumir tokens ni requerir API Key activa.
- [x] Prueba fixture/setup con auto-reset del acumulador de costo por sesión.
- [x] Tiempo de ejecución inferior a 1 segundo.

---

## ACTIVIDAD CORE 2 (BLOQUE 17 · U2.2): INTERPRETACIÓN CUALITATIVA Y LÍMITES DEL PIPELINE

### 1. Ficha Curricular
- **Unidad:** U2.2 - NLP Básico y Métricas.
- **Lección / Bloque:** Bloque 17 — *Interpretación cualitativa y límites del pipeline*.
- **Tipo de Actividad:** Actividad Core Sumativa Obligatoria.

### 2. Contexto de Negocio CENABAST
En compras públicas farmacéuticas, una alta coincidencia de palabras (*F1-Score*) no garantiza que el dictamen sea correcto. Por ejemplo, intercambiar *"adjudicar"* por *"rechazar"* preserva el 90% de las palabras pero invierte completamente la decisión legal. Esta actividad audita 20 casos de precios de catálogo y documenta las limitaciones de las métricas superficiales.

### 3. Entregables
- `Gate 2/pipeline_texto.py` (función `procesar_texto` y `calcular_metricas`).
- `Gate 2/test_pipeline_texto.py` (8 pruebas unitarias).
- `Gate 2/revision_manual.py` (script de cálculo léxico sobre 20 casos).
- `Gate 2/resultados_metricas.json` (reporte estructurado de 20 casos con precisión, cobertura y F1).
- `Gate 2/revision_manual.json` (auditoría manual de 10 casos: corrección, completitud, contradicción).
- `Gate 2/docs/limites_metrica.md` (documento de límites estructurado en 4 secciones).

### 4. Comando de Ejecución
```powershell
cd "Gate 2"
..\.venv\Scripts\python.exe revision_manual.py
..\.venv\Scripts\python.exe -m pytest test_pipeline_texto.py -v
```

### 5. Salida Esperada en Terminal
```text
✓ Guardado: Gate 2\resultados_metricas.json (20 casos evaluados)
  Precisión promedio: 0.5041
  Cobertura promedio: 0.5823
  F1 promedio:        0.5378
✓ Guardado: Gate 2\revision_manual.json (10 casos auditados manualmente)

test_pipeline_texto.py::TestPipelineTexto::test_calcular_metricas_coincidencia_parcial PASSED [ 12%]
...
test_pipeline_texto.py::TestPipelineTexto::test_procesar_texto_vacio_y_espacios PASSED [100%]
============================== 8 passed in 0.03s ==============================
```

### 6. Qué Evidencia Subir a Skillnest
1. **Captura de Pantalla:** Ejecución de `revision_manual.py` en consola mostrando métricas promedio y generación de archivos JSON.
2. **Archivos a Adjuntar:** Carga de `Gate 2/docs/limites_metrica.md` y `Gate 2/revision_manual.json` (o enlace a los mismos en GitHub).

### 7. Checklist de Aprobación
- [x] Corpus de al menos 20 respuestas analizadas en `resultados_metricas.json`.
- [x] Muestra de al menos 10 casos calificados a mano en `revision_manual.json`.
- [x] Documento `docs/limites_metrica.md` con las 4 secciones requeridas (Qué mide, Modos de falla en precios, Muestra y Recomendaciones).
- [x] Casos de prueba cubriendo cadenas vacías y sólo puntuación.

---

## ACTIVIDAD CORE 3 (BLOQUE 20 · U2.3): MANEJO DE ERRORES POR PASO Y ORQUESTACIÓN

### 1. Ficha Curricular
- **Unidad:** U2.3 - LangChain y Orquestación.
- **Lección / Bloque:** Bloque 20 — *Verifica la ejecución de tu chain de extremo a extremo*.
- **Tipo de Actividad:** Actividad Core Sumativa Obligatoria.

### 2. Contexto de Negocio CENABAST
Las consultas al sistema de adquisiciones abarcan distintas áreas: consultas de catálogo, auditoría de sobreprecio de cotizaciones o políticas de multas y desabastecimiento. La arquitectura debe enrutar condicionalmente a la rama adecuada y contener fallos con mecanismos de respaldo (*fallbacks*) sin que el servicio colapse.

### 3. Entregables
- `Gate 2/cadena_tres_pasos.py` (chain LCEL con clasificación -> análisis -> dictamen).
- `Gate 2/enrutamiento.py` (enrutador con `with_fallbacks` y `procesar_mensaje_seguro`).
- `Gate 2/test_orquestacion.py` (suite de 7 pruebas unitarias verificando ramas, fallbacks y contención).

### 4. Comando de Ejecución
```powershell
cd "Gate 2"
..\.venv\Scripts\python.exe -m pytest test_orquestacion.py -v
..\.venv\Scripts\python.exe enrutamiento.py
```

### 5. Salida Esperada en Terminal
```text
test_orquestacion.py::TestOrquestacionCENABAST::test_activacion_fallback_en_rama_con_falla PASSED [ 14%]
test_orquestacion.py::TestOrquestacionCENABAST::test_enrutamiento_rama_abastecimiento PASSED [ 28%]
test_orquestacion.py::TestOrquestacionCENABAST::test_enrutamiento_rama_catalogo PASSED [ 42%]
test_orquestacion.py::TestOrquestacionCENABAST::test_enrutamiento_rama_general_por_defecto PASSED [ 57%]
test_orquestacion.py::TestOrquestacionCENABAST::test_enrutamiento_rama_sobreprecio PASSED [ 71%]
test_orquestacion.py::TestOrquestacionCENABAST::test_procesar_mensaje_seguro_con_entradas_invalidas PASSED [ 85%]
test_orquestacion.py::TestOrquestacionCENABAST::test_procesar_mensaje_seguro_contiene_excepcion_inesperada PASSED [100%]
============================== 7 passed in 0.30s ==============================
```

### 6. Qué Evidencia Subir a Skillnest
1. **Captura de Pantalla:** Suite `test_orquestacion.py` con 7 tests verdes demostrando contención de fallos.
2. **Enlace a GitHub:** URL a `Gate 2/enrutamiento.py` y `Gate 2/test_orquestacion.py`.

### 7. Checklist de Aprobación
- [x] Cadena encadenada de tres pasos (`cadena_tres_pasos.py`).
- [x] Enrutamiento condicional con al menos 3 ramas especializadas.
- [x] Mecanismo de contingencia `with_fallbacks` activo.
- [x] Envoltorio `procesar_mensaje_seguro` que contiene excepciones no controladas.

---

## ACTIVIDAD CORE 4 (BLOQUE 23 · U2.4): LÍMITES DE AUTONOMÍA DEL AGENTE Y SUPERVISIÓN HUMANA

### 1. Ficha Curricular
- **Unidad:** U2.4 - Agentes, Herramientas y Memoria.
- **Lección / Bloque:** Bloque 23 — *Documenta los límites de la autonomía de tu agente*.
- **Tipo de Actividad:** Actividad Core Sumativa Obligatoria.

### 2. Contexto de Negocio CENABAST
Un agente de compras públicas puede consultar catálogos o calcular porcentajes de forma autónoma (riesgo bajo). Sin embargo, la emisión formal de una orden de compra o la aprobación de sobreprecios críticos (> 15%) compromete recursos fiscales y está legalmente reservada a funcionarios públicos humanos. Se requiere un protocolo de supervisión que pause la ejecución ante acciones críticas.

### 3. Entregables
- `Gate 2/agente_con_herramientas.py` (agente con al menos dos herramientas e inspección de `intermediate_steps`).
- `Gate 2/mi_agente.py` (3 herramientas CENABAST, clasificación de riesgo y función `esperar_aprobacion`).
- `Gate 2/trazas_agente.jsonl` (log inmutable de activaciones y puntos de supervisión).
- `Gate 2/docs/limites_autonomia.md` (política formal de autonomía y supervisión).

### 4. Comando de Ejecución
```powershell
cd "Gate 2"
..\.venv\Scripts\python.exe mi_agente.py
```

### 5. Salida Esperada en Terminal
```text
===========================================================================
  AGENTE AUDITOR CENABAST CON LÍMITES DE AUTONOMÍA (BLOQUE 23)
===========================================================================
[OPERACIÓN 1 - RIESGO BAJO] Consulta de catálogo de referencia:
  Resultado: Catálogo CENABAST 2026: Paracetamol = $22.40 CLP netos por unidad.

[OPERACIÓN 2 - RIESGO BAJO] Cálculo de sobreprecio de oferta:
  Resultado: {'precio_ofertado': 33.6, 'precio_referencia': 22.4, 'desviacion_pct': 50.0, 'sobreprecio_critico': True, 'dictamen_sugerido': 'RECHAZAR'}

[OPERACIÓN 3 - RIESGO ALTO] Intento de adjudicación SIN aprobación humana:
[ALERTA DE GOBERNANZA - RIESGO ALTO] Operación: adjudicar_orden_compra
  Monto Comprometido: $150,000,000.00 CLP
  Resultado de Supervisión Humana: RECHAZADO / BLOQUEADO
  Resultado: {'estado': 'DETENIDO_POR_SUPERVISION', 'orden_compra_emitida': False}

[OPERACIÓN 4 - RIESGO ALTO] Adjudicación formal CON autorización del Jefe de Adquisiciones:
[ALERTA DE GOBERNANZA - RIESGO ALTO] Operación: adjudicar_orden_compra
  Monto Comprometido: $85,000,000.00 CLP
  Resultado de Supervisión Humana: AUTORIZADO
  Resultado: {'estado': 'ADJUDICADA_CON_AUTORIZACION', 'orden_compra_emitida': True}
```

### 6. Qué Evidencia Subir a Skillnest
1. **Captura de Pantalla:** Terminal mostrando el bloqueo de la Operación 3 y la autorización formal de la Operación 4.
2. **Archivos a Adjuntar:** Documento `Gate 2/docs/limites_autonomia.md` y fragmento de `Gate 2/trazas_agente.jsonl`.

### 7. Checklist de Aprobación
- [x] Herramientas tipadas clasificadas por nivel de riesgo (Bajo, Medio, Alto).
- [x] Función de pausa/aprobación humana implementada para operaciones de alto riesgo.
- [x] Registro auditable en `trazas_agente.jsonl`.
- [x] Documento de límites de autonomía formalizado en `docs/limites_autonomia.md`.

---

## ACTIVIDAD CORE 5 (BLOQUE 28 · U2.5): LATENCIA Y COSTO DEL FLUJO RAG

### 1. Ficha Curricular
- **Unidad:** U2.5 - RAG y Bases Vectoriales.
- **Lección / Bloque:** Bloque 28 — *Registra la latencia y el costo de tu flujo RAG*.
- **Tipo de Actividad:** Actividad Core Sumativa Obligatoria.

### 2. Contexto de Negocio CENABAST
Un sistema RAG en producción institucional debe ser auditado en sus tiempos de respuesta y en el consumo de presupuesto de inferencia. Es fundamental demostrar que la fase de generación domina la latencia y que aumentar $k$ de 3 a 6 incrementa proporcionalmente los tokens de entrada debido a la mayor carga de contexto.

### 3. Entregables
- `Gate 2/data/` (Corpus de 5 documentos oficiales markdown).
- `Gate 2/indexar_corpus.py` (indexación y persistencia de vector store en disco).
- `Gate 2/recuperacion.py` (búsqueda semántica, prompt dinámico y citas `{1: 'archivo.md'}`).
- `Gate 2/preflight.py` (validación de persistencia y `.gitignore`).
- `Gate 2/registro_rag.py` (cronometraje por etapa y registro de tokens).
- `Gate 2/registros_latencia_costo.jsonl` (bitácora de telemetría de latencias y costos).

### 4. Comando de Ejecución
```powershell
cd "Gate 2"
..\.venv\Scripts\python.exe preflight.py
..\.venv\Scripts\python.exe registro_rag.py
```

### 5. Salida Esperada en Terminal
```text
======================================================================
  VERIFICACIÓN PREFLIGHT DEL PROYECTO (BLOQUE 28)
======================================================================
✓ Índice vectorial persistido verificado (58 chunks en disco).
✓ Corpus de referencia verificado (5 documentos markdown en data/).
✓ Regla de exclusión '.env' presente en .gitignore
✓ Regla de exclusión 'indice_gate2' presente en .gitignore
✓ PREFLIGHT EXITOSO: Todos los componentes operativos y seguros.

===========================================================================
  MEDICIÓN DE LATENCIA Y COSTO DEL FLUJO RAG CENABAST (BLOQUE 28)
===========================================================================
Evaluando consulta: "¿Cuál es el precio de referencia de Paracetamol 500 mg..."
  [k=3] Latencia total: 32.33 ms (Búsqueda: 12.0 ms, Gen: 20.32 ms) | Tokens in: 644 | Costo: $0.000100 USD
  [k=6] Latencia total: 21.53 ms (Búsqueda: 1.19 ms, Gen: 20.34 ms) | Tokens in: 972 | Costo: $0.000133 USD
✓ Se guardaron 6 trazas de telemetría en: Gate 2\registros_latencia_costo.jsonl
```

### 6. Qué Evidencia Subir a Skillnest
1. **Captura de Pantalla:** Ejecución exitosa de `preflight.py` demostrando persistencia en disco y reglas de `.gitignore`.
2. **Captura de Pantalla:** Terminal con la comparativa de latencias y tokens entre $k=3$ y $k=6$ generada por `registro_rag.py`.
3. **Archivo a Adjuntar:** `Gate 2/registros_latencia_costo.jsonl`.

### 7. Checklist de Aprobación
- [x] Corpus de al menos 5 documentos indexados y persistidos en disco (`indice_gate2/`).
- [x] Desglose explícito de latencias (`embed_y_busqueda` y `generacion`).
- [x] Comparativa de hiperparámetros $k=3$ vs $k=6$ evidenciando crecimiento de tokens.
- [x] Script `preflight.py` ejecutado y aprobado con código de salida 0.

---

## ACTIVIDAD CORE 6 (BLOQUE 30 · U2.6): DECISIÓN FUNDAMENTADA DE PERSONALIZACIÓN

### 1. Ficha Curricular
- **Unidad:** U2.6 - Personalización: RAG vs PEFT vs Fine-Tuning.
- **Lección / Bloque:** Bloque 30 — *Redacta tu decisión de personalización fundamentada*.
- **Tipo de Actividad:** Actividad Core Sumativa Obligatoria.

### 2. Contexto de Negocio CENABAST
Un error frecuente en proyectos de IA es intentar resolver la actualización de precios mediante re-entrenamiento (fine-tuning). Para CENABAST, donde los catálogos farmacéuticos se actualizan mensualmente, reentrenar modelos es técnica y económicamente inviable, y propenso a alucinaciones. La solución debe respaldarse mediante un Registro de Decisión de Arquitectura (ADR) formal y cuantitativo.

### 3. Entregables
- `Gate 2/dataset_tuning.py` (dataset de 10 ejemplos balanceados con función de validación).
- `Gate 2/decision.py` (algoritmo cuantitativo ponderado de recomendación de técnica).
- `Gate 2/docs/decision_personalizacion.md` (ADR formal en 4 secciones justificando RAG).

### 4. Comando de Ejecución
```powershell
cd "Gate 2"
..\.venv\Scripts\python.exe dataset_tuning.py
..\.venv\Scripts\python.exe decision.py
```

### 5. Salida Esperada en Terminal
```text
======================================================================
  VALIDACIÓN DEL DATASET DE PERSONALIZACIÓN (BLOQUE 29)
======================================================================
Estado de Validación: APROBADO (Válido)
Total ejemplos:       10
Distribución por Categoría:
  - catalogo_precios: 4 ejemplos
  - analisis_sobreprecio: 3 ejemplos
  - gobernanza_y_riesgo: 3 ejemplos
✓ Todos los ejemplos cumplen con los estándares de instrucción/salida para tuning.

===========================================================================
  MATRIZ CUANTITATIVA DE DECISIÓN DE ARQUITECTURA (BLOQUE 30)
===========================================================================
RESUMEN PONDERADO DE TÉCNICAS (Escala 1.0 - 5.0):
  • RAG             : 4.900 puntos
  • PEFT_LoRA       : 2.775 puntos
  • Full_FineTuning : 1.775 puntos

RECOMENDACIÓN FINAL FUNDAMENTADA:
  Estrategia Seleccionada: RAG
  Dictamen: La arquitectura óptima para CENABAST es RAG con un puntaje de 4.9/5.000...
```

### 6. Qué Evidencia Subir a Skillnest
1. **Captura de Pantalla:** Ejecución de `decision.py` mostrando la matriz ponderada donde RAG obtiene 4.900 puntos.
2. **Archivo a Adjuntar:** Documento formal ADR `Gate 2/docs/decision_personalizacion.md`.

### 7. Checklist de Aprobación
- [x] Dataset de tuning validado sintácticamente (`dataset_tuning.py`).
- [x] Algoritmo cuantitativo implementado evaluando al menos 5 dimensiones (`decision.py`).
- [x] Documento ADR con las 4 secciones estándar (Contexto, Opciones, Matriz, Decisión final).
- [x] Justificación técnica fundada en el dinamismo mensual de precios de catálogo y necesidad de citas.

---

## ACTIVIDAD CORE 7 (BLOQUE 32 · U2.7): MATRIZ DE RIESGOS Y VERSIONADO DE PROMPTS

### 1. Ficha Curricular
- **Unidad:** U2.7 - Observabilidad, Seguridad y Gobernanza.
- **Lección / Bloque:** Bloque 32 — *Completa tu matriz de riesgos y el versionado de prompts*.
- **Tipo de Actividad:** Actividad Core Sumativa Obligatoria.

### 2. Contexto de Negocio CENABAST
El uso de IA en contratación pública exige altos estándares de seguridad y observabilidad:
1. Versionar inmutablemente las plantillas de prompts con huellas SHA-256 para auditorías de la Contraloría.
2. Contar con un punto de interrupción interactivo (`interrupt()`) de LangGraph para pausar adjudicaciones con sobreprecio crítico (> 15%).
3. Mapear los 5 riesgos prioritarios (alucinación de precios, inyección en ofertas, auto-adjudicación, fuga de PII y error de multas) vinculados a sus mitigaciones técnicas.

### 3. Entregables
- `Gate 2/registro_prompts.py` (gestor de versiones con huellas SHA-256 inmutables).
- `Gate 2/grafo_supervision.py` (grafo LangGraph con `interrupt()` y checkpointer `InMemorySaver`).
- `Gate 2/matriz_riesgos.py` (evaluador cuantitativo de riesgos P x I).
- `Gate 2/docs/matriz_riesgos.md` (matriz formal de gobernanza y riesgos).

### 4. Comando de Ejecución
```powershell
cd "Gate 2"
..\.venv\Scripts\python.exe registro_prompts.py
..\.venv\Scripts\python.exe grafo_supervision.py
..\.venv\Scripts\python.exe matriz_riesgos.py
```

### 5. Salida Esperada en Terminal
```text
[VERSIÓN v1.0] Huella SHA-256: 8ae1fb1b4a020b3822adc6336d5d5b8bfe49e31c95141df5d5df2da668f4e5e5
[VERSIÓN v2.0] Huella SHA-256: ae0361027152f27833cbd876b500e3fbc9615edb2f04dcc6f0f0b6daaf8f168c

===========================================================================
  DEMOSTRACIÓN DEL GRAFO DE SUPERVISIÓN HUMANA LANGGRAPH (BLOQUE 32)
===========================================================================
[PASO 1] Iniciando evaluación algorítmica de la oferta:
  Eventos procesados antes de la pausa: 2
  ¿El grafo se encuentra en pausa por interrupción? True
  Datos emitidos por interrupt():
    {'alerta': 'SOBREPRECIO_CRITICO_CENABAST', 'medicamento': 'Paracetamol 500 mg', 'precio_ofertado': 33.6, 'desviacion_pct': 50.0}

[PASO 2] Reanudando ejecución con autorización humana (Command(resume=True)):
  Estado Final Aprobado: True
  Orden Emitida:         True

===========================================================================
  EVALUACIÓN DE MATRIZ DE RIESGOS DE IA PARA CENABAST (BLOQUE 32)
===========================================================================
Total riesgos evaluados: 5
Distribución por severidad: {'CRÍTICO': 1, 'ALTO': 2, 'MEDIO': 2, 'BAJO': 0}
✓ Documento formal de matriz de riesgos generado en: Gate 2\docs\matriz_riesgos.md
```

### 6. Qué Evidencia Subir a Skillnest
1. **Captura de Pantalla:** Ejecución de `grafo_supervision.py` demostrando la interrupción interactiva con `interrupt()` y reanudación con `Command(resume=True)`.
2. **Archivos a Adjuntar:** Documento formal `Gate 2/docs/matriz_riesgos.md` y enlaces a `registro_prompts.py` y `grafo_supervision.py`.

### 7. Checklist de Aprobación
- [x] Registro inmutable de plantillas de prompts con huellas criptográficas SHA-256.
- [x] Grafo de estados ejecutable con LangGraph que interrumpe y reanuda con checkpointer.
- [x] Matriz de al menos 5 riesgos propios evaluados cuantitativamente (P x I).
- [x] Conexión explícita entre cada riesgo y su mitigación técnica en código.

---

## HITO FINAL GATE 2 (BLOQUE S1 · U2.8): SERVICIO RAG MODULAR E INTEGRADO

### 1. Ficha Curricular
- **Unidad:** U2.8 - Gate 2: Integración y Orquestación.
- **Lección / Bloque:** Bloque S1 — *Gate 2 - Entrega del servicio IA modular con RAG*.
- **Tipo de Actividad:** Evaluación Sumativa de Término de Módulo (35% de la ponderación global).

### 2. Criterios de Aprobación Oficiales
Para aprobar el Gate 2 se requiere:
1. **Promedio Ponderado de Dimensiones >= 80%:**
   - Pipeline RAG funcional (25%).
   - Seguridad, versionado y gobernanza (20%).
   - Calidad de recuperación y citación de fuentes (15%).
   - Personalización justificada (15%).
   - Observabilidad y trazabilidad (15%).
   - Costo, latencia y checklist operativo (10%).
2. **Cumplimiento Obligatorio de los 4 Criterios No Compensables (Mandatorios 4/4):**
   - **C1:** El pipeline corre de punta a punta sin excepciones no capturadas.
   - **C2:** Cada respuesta devuelta cita explícitamente el documento fuente que la respalda (`[fuente: ...].md`).
   - **C3:** Los logs estructurados no exponen PII ni consultas crudas en texto plano.
   - **C4:** Existe al menos un punto de supervisión humana interactiva real con LangGraph (`interrupt()` y `Command(resume=True)`).

### 3. Procedimiento de Verificación Global para el Alumno
Antes de enviar el Gate 2 en Skillnest, ejecute la siguiente secuencia en su terminal:
```powershell
cd "Gate 2"
# 1. Pruebas Unitarias U2.1
..\.venv\Scripts\python.exe -m pytest test_cliente.py -v

# 2. Pruebas de Pipeline de Texto U2.2
..\.venv\Scripts\python.exe -m pytest test_pipeline_texto.py -v

# 3. Pruebas de Orquestación y Enrutamiento U2.3
..\.venv\Scripts\python.exe -m pytest test_orquestacion.py -v

# 4. Verificación de Autonomía de Agentes U2.4
..\.venv\Scripts\python.exe mi_agente.py

# 5. Verificación Preflight del Almacén Vectorial U2.5
..\.venv\Scripts\python.exe preflight.py

# 6. Instrumentación de Latencia y Costos U2.5
..\.venv\Scripts\python.exe registro_rag.py

# 7. Decisión Cuantitativa de Personalización U2.6
..\.venv\Scripts\python.exe decision.py

# 8. Supervisión Humana LangGraph y Matriz de Riesgos U2.7
..\.venv\Scripts\python.exe grafo_supervision.py
..\.venv\Scripts\python.exe matriz_riesgos.py
```

### 4. Checklist Definitivo de Entrega Gate 2
- [x] Repositorio limpio y estructurado con macro carpetas `Gate 1` y `Gate 2`.
- [x] Corpus CENABAST completo en `Gate 2/data/` (5 documentos markdown).
- [x] Índice vectorial persistido en disco (`Gate 2/indice_gate2/`) excluido en `.gitignore`.
- [x] 100% de las pruebas unitarias pasando en verde en milisegundos.
- [x] Todos los documentos técnicos de arquitectura en `Gate 2/docs/`:
  - `limites_metrica.md`
  - `limites_autonomia.md`
  - `decision_personalizacion.md`
  - `matriz_riesgos.md`
- [x] Evidencias y capturas listas para carga en la plataforma Skillnest.
