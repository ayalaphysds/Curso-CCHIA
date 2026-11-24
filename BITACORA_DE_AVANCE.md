# 📓 Bitácora de Avance — Especialización IA Accenture (CCHIA)

> **Documento vivo de seguimiento, consultas, programas y estado del curso**  
> *Este documento se actualiza progresivamente a lo largo de las sesiones de trabajo con cada nueva consulta, código generado y avance por las unidades y gates del programa.*

---

## 📌 1. Ficha del Estudiante y Entorno del Proyecto

| Parámetro | Detalle |
| :--- | :--- |
| **Estudiante** | Sebastián Ayala (`sayala7` / `ayalaphysds`) |
| **Programa** | Especialización IA Accenture (Skillnest) |
| **Repositorio Remoto** | [`https://github.com/ayalaphysds/Curso-CCHIA.git`](https://github.com/ayalaphysds/Curso-CCHIA.git) |
| **Directorio Local** | `C:\Users\sayal\OneDrive\Desktop\Curso CCHIA\Curso-CCHIA` |
| **Proveedor LLM Recomendado** | Google Gemini API (o proveedor alternativo) |
| **Entorno de Ejecución** | Windows / PowerShell / VS Code / Python 3.12+ |
| **Fecha de Inicio** | Octubre 2026 |
| **Última Actualización** | 24 de Noviembre de 2026 |

---

## 📍 2. ¿Dónde nos encontramos en el curso? (Estado Actual)

```mermaid
flowchart LR
    A["Módulo 1: Habilitación Técnica (20%)"] --> B["Gate 1 (Miniaplicación API)"]
    B --> C["Módulo 2: Componentes IA (35%)"]
    C --> D["Gate 2 (Servicio RAG + LangChain)"]
    D --> E["Módulo 3: Integración Profesional (45%)"]
    E --> F["Gate 3 Capstone (End-to-End)"]

    style A fill:#10b981,stroke:#059669,stroke-width:2px,color:#ffffff
    style B fill:#10b981,stroke:#059669,stroke-width:2px,color:#ffffff
    style C fill:#10b981,stroke:#059669,stroke-width:2px,color:#ffffff
    style D fill:#10b981,stroke:#059669,stroke-width:2px,color:#ffffff
    style E fill:#10b981,stroke:#059669,stroke-width:2px,color:#ffffff
    style F fill:#10b981,stroke:#059669,stroke-width:2px,color:#ffffff
```

> ### 🟢 Estado Actual:
> - **Módulo Completado 1:** **Módulo 1 — Habilitación Técnica** (20% de la nota | 11 Bloques) `[100% COMPLETADO / GATE 1 APROBADO — 7.0/7.0]`
> - **Módulo Completado 2:** **Módulo 2 — Construcción de componentes IA** (35% de la nota | 21 Bloques) `[100% COMPLETADO / GATE 2 APROBADO]` (98.8% rúbrica, 106 tests aprobados).
> - **Módulo Completado 3:** **Módulo 3 — Integración profesional** (45% de la nota | 7 Unidades, Bloques 33 a S2) `[100% COMPLETADO / GATE 3 CAPSTONE IMPLEMENTADO]` (83 tests automatizados en verde, 19/19 fuentes locales de `verificar_gate3.py` en 100%, listo para corrida final `--con-docker` y defensa en vivo).
> - **Punto Exacto en el Programa:**
>   - ✅ *Gate 1 Aprobado (7.0/7.0):* Contrato JSON formal en `Gate 1/README.md` y 13/13 tests pasando.
>   - ✅ *Gate 2 Completado:* Servicio RAG CENABAST modular (`Gate 2/servicio_rag.py`) y 106/106 tests pasando.
>   - ✅ *Módulo 3 y Gate 3 Capstone Completados:* Aplicación end-to-end FastAPI + Interfaz Web + Docker Compose + QA/Seguridad/Alucinaciones + ADRs/Transferencia + Guion de defensa de 8 min, Plan B de demo y verificador maestro en `Gate 3/`.
>   - 📍 *Siguiente paso:* Subida de los enlaces directos en Skillnest (`Gate 3/GUIA_DE_ENTREGAS_MODULO_3.md`), presentación de diapositivas y defensa técnica en vivo.

---

## 🗺️ 3. Mapa de Avance del Programa

### 🛠️ MÓDULO 1: Habilitación Técnica (20% de la nota) — `[100% COMPLETADO / GATE 1 APROBADO]`
*Objetivo: Sentar bases técnicas sólidas (Git, Python modular, variables de entorno, seguridad, prompt estructurado) para la miniaplicación de consumo vía API.*

- [x] **U1.1 Alineación estratégica y perfil de egreso**
  - [x] Diagnóstico técnico y mapa de módulos, gates y cinturones.
  - [x] El punto de llegada: qué vas a tener construido al terminar.
  - [x] *Actividad Core:* Ficha de alineación técnica y elección de ruta.
- [x] **U1.2 Setup técnico: terminal, Git, entorno Python y cliente HTTP**
  - [x] Bloque 2: Entorno completo de cero a API y por qué los secretos no van al repo.
  - [x] Bloque 2: *Actividad práctica:* Inicializa tu repositorio y haz tu primer commit [Completado y commiteado].
  - [x] Bloque 3: Réplica guiada del setup completo (entorno virtual `.venv`, `requirements.txt`) [Completado y validado].
  - [x] Bloque 4: Variables de entorno (`.env`, `.gitignore`) [Completado y protegido].
  - [x] Bloque 4: Disparo a la API desde Postman / Thunder Client / requests [Completado y probado].
  - [x] Bloque 4: *Actividad core:* Ejecuta tu primera petición autenticada de prueba [Completado, evidencia generada en docs/].
- [x] **U1.3 Python aplicado para integración con IA** `[COMPLETADA]`
  - [x] Bloque 5: *Actividad práctica:* Primer módulo Python de consumo de servicios externos (`functions`, `json`).
  - [x] Bloque 5: Manejo de errores de red inducidos a propósito.
  - [x] Bloque 6: Refactorización a funciones modulares y reutilizables en el repo.
  - [x] Bloque 7: Excepciones (`try-except`), validación de entradas y rúbrica de calidad de código.
  - [x] Bloque 7: *Actividad core:* Incorpora excepciones, validación y commit de avance.
- [x] **U1.4 Fundamentos de IA generativa y arquitectura de aplicaciones** `[COMPLETADA]`
  - [x] Bloque 8: Tokens, ciclo request-response y cálculo de costos en vivo.
  - [x] Bloque 8: *Actividad práctica:* Diagrama la arquitectura de tu miniaplicación [Generado en docs/ y commiteado].
  - [x] Bloque 9: Criterios para elegir entre modelos candidatos (costo, latencia, escala).
  - [x] Bloque 9: *Actividad core:* Documentación de la decisión de arquitectura en el repositorio [docs/decision-arquitectura.md].
- [x] **U1.5 Prompt engineering profesional inicial** `[COMPLETADA]`
  - [x] Bloque 10: Prompts de sistema vs conversación y forzado de salida JSON estructurada.
  - [x] Bloque 10: *Actividad core:* Banco de prompts y validación de consistencia [prompts/banco.py, test_consistencia.py, registro_resultados.json].
- [x] **U1.6 Gate 1 — Habilitación técnica** `[APROBADO]`
  - [x] Bloque 11: Repaso de rúbrica del Gate 1 y las tres oportunidades.
  - [x] Bloque 11: Ensayo en vivo: clonar, instalar dependencias y ejecutar sin ayuda [Verificado en carpeta limpia].
  - [x] Bloque 11: *Actividad core / Sumativa:* **Rendición y entrega formal de Gate 1** [Commit oficial subido].


---

### 🤖 MÓDULO 2: Construcción de componentes IA (35% de la nota) — `[100% COMPLETADO / GATE 2 APROBADO]`
*Objetivo: Desarrollar componentes modulares de IA generativa con LangChain, RAG con citación estricta, bases vectoriales Chroma, observabilidad estructurada sin PII, filtrado de inyecciones y orquestación con supervisión humana en LangGraph.*

- [x] **U2.1 Consumo avanzado de APIs de IA generativa** `[COMPLETADA]`
  - [x] Bloque 12: *Cliente modular de consumo de APIs, con reintentos* (`Gate 2/cliente.py`, `Gate 2/cliente_api.py`, `Gate 2/cliente_reintento.py`).
  - [x] Bloque 13: Rate limits, backoff exponencial y cálculo acumulativo de costos por operación.
  - [x] Bloque 14: *Actividad core:* Pruebas unitarias sobre el cliente modular (`Gate 2/test_cliente.py` con 10/10 tests passing).
- [x] **U2.2 Pipeline de texto, NLP básico y evaluación inicial** `[COMPLETADA]`
  - [x] Bloque 15: Pipeline de ingesta, normalización, limpieza y tokenización (`Gate 2/pipeline_texto.py`).
  - [x] Bloque 16: Embeddings locales, similitud coseno y métricas léxicas/semánticas.
  - [x] Bloque 17: *Actividad core:* Evaluación de calidad con métricas automáticas y revisión manual (`Gate 2/revision_manual.py`, `resultados_metricas.json`, `docs/limites_metrica.md`).
- [x] **U2.3 LangChain y orquestación de flujos** `[COMPLETADA]`
  - [x] Bloque 18: Fundamentos de LCEL, PromptTemplates y cadenas secuenciales de 3 pasos (`Gate 2/cadena_tres_pasos.py`).
  - [x] Bloque 19: Composición de cadenas complejas y manejo de fallbacks.
  - [x] Bloque 20: *Actividad core:* Enrutamiento semántico condicional (`Gate 2/enrutamiento.py` con `RunnableBranch` y `Gate 2/test_orquestacion.py`).
- [x] **U2.4 Agentes, herramientas externas y memoria** `[COMPLETADA]`
  - [x] Bloque 21: Conceptos de reactividad, llamadas a herramientas y bucle de razonamiento.
  - [x] Bloque 22: Integración de herramientas personalizadas de consulta y auditoría de precios CENABAST.
  - [x] Bloque 23: *Actividad core:* Agente con 3 herramientas y control de autonomía de alto riesgo (`Gate 2/mi_agente.py`, `trazas_agente.jsonl`, `docs/limites_autonomia.md`).
- [x] **U2.5 RAG y bases de datos vectoriales** `[COMPLETADA]`
  - [x] Bloque 24: Conceptos de arquitectura RAG y generación fundamentada en fuentes.
  - [x] Bloque 25: Fragmentación documental con chunking recursivo optimizado (`Gate 2/data/` con 5 documentos normativos).
  - [x] Bloque 26: Embeddings semánticos y vectorstore Chroma persistente (`Gate 2/indice_gate2/`).
  - [x] Bloque 27: Implementación de indexación y persistencia (`Gate 2/src/indexador.py`, `Gate 2/indexar_corpus.py`).
  - [x] Bloque 28: *Actividad core:* Recuperador con citación y observabilidad de latencia/tokens k=3 vs k=6 (`Gate 2/registro_rag.py`, `registros_latencia_costo.jsonl`, `preflight.py`).
- [x] **U2.6 Personalización de modelos RAG, fine-tuning y soft-prompting** `[COMPLETADA]`
  - [x] Bloque 29: Estrategias de personalización, trade-offs y preparación de dataset de tuning (`Gate 2/dataset_tuning.py`).
  - [x] Bloque 30: *Actividad core:* Decisión cuantitativa de adaptación y registro ADR (`Gate 2/decision.py`, `Gate 2/docs/decision_personalizacion.md`).
- [x] **U2.7 Observabilidad, seguridad y gobernanza técnica** `[COMPLETADA]`
  - [x] Bloque 31: Logging estructurado JSON sin PII y filtro de sanitización ante inyección de prompts (`Gate 2/src/seguridad.py`, `Gate 2/src/observabilidad.py`).
  - [x] Bloque 32: *Actividad core:* Registro de prompts con hash SHA-256 (`Gate 2/registro_prompts.py`), grafo de supervisión humana LangGraph (`Gate 2/grafo_supervision.py`, `Gate 2/src/supervision.py`) y matriz de riesgos (`Gate 2/matriz_riesgos.py`, `Gate 2/docs/matriz_riesgos.md`).
- [x] **Gate 2: Integración y orquestación de servicios IA (Entrega modular completa)** `[APROBADO]`
  - [x] Servicio RAG CENABAST ejecutable de punta a punta (`Gate 2/servicio_rag.py`).
  - [x] Citación explícita obligatoria en respuestas (`[fuente: <doc>]`).
  - [x] Observabilidad JSON estructurada sin contenido crudo ni PII.
  - [x] Supervisión interactiva humana vía LangGraph (`interrupt` y reanudación con `Command(resume=True)`).
  - [x] Guía exhaustiva de entregas para el alumno (`Gate 2/GUIA_DE_ENTREGAS_MODULO_2.md`).
  - [x] Suite oficial y pruebas adversarias superadas (106/106 tests OK, 98.8% autoevaluación rúbrica).

---

### 🚀 MÓDULO 3: Integración profesional (45% de la nota) — `[100% COMPLETADO / GATE 3 LISTO]`
- [x] **U3.1 Diseño funcional del proyecto según perfil de salida** (`Gate 3/docs/ficha_diseno_funcional.md`, `Gate 3/docs/diagrama_arquitectura.png`, `Gate 3/docs/revision_alcance.md`, `Gate 3/verificar_ficha_completa.py` — 5/5)
- [x] **U3.2 FastAPI para exposición de servicios** (`Gate 3/servicio/`, `Gate 3/casos.py`, `Gate 3/cliente_externo.py`, `Gate 3/docs/registro_pruebas.md`, `Gate 3/tests/test_api.py` — 12/12)
- [x] **U3.3 Docker y despliegue controlado** (`Gate 3/Dockerfile`, `Gate 3/interfaz/`, `Gate 3/compose.yaml`, `Gate 3/buscar_secretos.py`, `Gate 3/verificar_dockerfile.py` 7/7, `Gate 3/verificar_entrega.py` 7/7)
- [x] **U3.4 Integración end-to-end de la solución generativa** (`Gate 3/docs/pruebas_parciales.md`, `Gate 3/escenarios.py` 14/14, `Gate 3/docs/bitacora_ajustes.md`, `Gate 3/docs/registro_ejecucion.md`, `Gate 3/verificar_registro.py` 6/6)
- [x] **U3.5 QA, seguridad y validación de la solución** (`Gate 3/docs/matriz_pruebas.md` 6/6, `Gate 3/docs/registro_alucinaciones.md`, `Gate 3/verificar_mitigaciones.py` 17/17, `Gate 3/docs/matriz_riesgos.md` 6/6)
- [x] **U3.6 Documentación técnica y transferencia** (`Gate 3/README.md` 8/8, `Gate 3/docs/api.md` 6/6, `Gate 3/docs/transferencia.md` 5/5, `Gate 3/docs/decisiones.md`, `Gate 3/docs/limitaciones.md`, `Gate 3/verificar_decisiones.py` 7/7, `Gate 3/probar_en_frio.py` 5/5)
- [x] **U3.7 Gate 3: Capstone Project — Aplicación IA End-to-End para Producción** (`Gate 3/docs/defensa.md`, `Gate 3/medir_guion.py` 9/9, `Gate 3/ensayo_demo.py` 8/8, `Gate 3/docs/demo_respaldo.md`, `Gate 3/rubrica_gate3.py`, `Gate 3/verificar_gate3.py`, `Gate 3/docs/gate3.md`, `Gate 3/GUIA_DE_ENTREGAS_MODULO_3.md`)

---

## 🎯 4. Checklist Crítico: Criterios No Compensables

### Gate 1 — Habilitación Técnica `[APROBADO]`
Para aprobar el **Gate 1** (y acceder a la calificación mínima de 80% y optar al Cinturón), es obligatorio cumplir estos 4 puntos críticos:

| Criterio Crítico | Requisito | Estado | Evidencia / Verificación |
| :--- | :--- | :---: | :--- |
| **1. Código ejecutable** | La aplicación corre de punta a punta sin excepciones no capturadas. | ✅ Cumplido | Módulo `Gate 1/src/consumir_gemini.py` blindado con validaciones y captura de excepciones; suite `Gate 1/tests/test_consumir_gemini.py` pasando 13/13 tests sin caídas abruptas |
| **2. Entorno reproducible** | `requirements.txt` documentado y ejecutable en cualquier máquina con `pip install -r requirements.txt`. | ✅ Cumplido | Entorno `.venv` creado; dependencias fijadas en `Gate 1/requirements.txt` |
| **3. Credenciales protegidas** | El archivo `.env` está en `.gitignore`. Nunca se commitea la API key real. | ✅ Cumplido | `.env` excluido en `.gitignore`; validado con `git status` y `git check-ignore` |
| **4. Consumo exitoso de API** | La petición recibe respuesta HTTP 200 con payload válido del modelo. | ✅ Cumplido | Petición ejecutada con `gemini-3.5-flash`; evidencia guardada en `Gate 1/docs/evidencia_peticion_autenticada.json` |

---

### Gate 2 — Integración y Orquestación de Servicios IA `[APROBADO]`
Para aprobar el **Gate 2** (calificación mínima 80% en rúbrica ponderada y pase directo en Oportunidad 1), es mandatario cumplir sin excepción los 4 criterios no compensables:

| Criterio Crítico No Compensable | Requisito Oficial de Rúbrica | Estado | Evidencia / Verificación en el Repositorio |
| :--- | :--- | :---: | :--- |
| **1. Pipeline corre de punta a punta** | El pipeline completo (recuperación + generación) se ejecuta de inicio a fin sin excepciones no capturadas ante consultas válidas. | ✅ Cumplido | `Gate 2/servicio_rag.py` orquesta indexación, seguridad, recuperación y síntesis sin errores; fallback ante contexto vacío (`Gate 2/test_gate2.py::test_criterio_no_compensable_pipeline_completo`). |
| **2. Respuestas citan fuentes explícitas** | La respuesta generada incluye la referencia textual verificable al documento fuente recuperado. | ✅ Cumplido | Formato obligatorio `[fuente: <doc>]` validado en toda consulta (`Gate 2/src/recuperador.py` y `Gate 2/test_gate2.py::test_criterio_no_compensable_cita_fuentes`). |
| **3. Logs sin contenido crudo / Cero PII** | Los registros de auditoría/observabilidad contienen metadatos operativos (latencia, tokens, longitudes) sin volcar texto sensible ni datos personales. | ✅ Cumplido | Logger estructurado JSON en `Gate 2/src/observabilidad.py`; test oficial valida ausencia de consultas crudas o correos en logs (`Gate 2/test_gate2.py::test_criterio_no_compensable_cero_pii_en_logs`). |
| **4. Supervisión humana interactiva funciona** | El sistema detecta desviaciones críticas o acciones de alto impacto, pausa el flujo esperando aprobación y reanuda correctamente. | ✅ Cumplido | Grafo interactivo en `Gate 2/src/supervision.py` con punto de interrupción `interrupt` y reanudación vía `Command(resume=True)` (`Gate 2/test_gate2.py::test_criterio_no_compensable_supervision_humana`). |

---

## 💬 5. Registro Cronológico de Consultas y Preguntas

| ID | Fecha | Módulo / Tema | Consulta / Pregunta del Usuario | Respuesta / Solución Brindada | Estado |
| :---: | :---: | :---: | :--- | :--- | :---: |
| **C-001** | 19-10-2026 | Gestión del Curso | Creación de una bitácora de avance viva para registrar consultas, preguntas, programas y ubicación del curso. | Se analizó el repositorio git y plan de estudios (Skillnest - Accenture), se diseñó la estructura de la bitácora con mapa de unidades, gates, rúbrica, tablas de programas y registro de sesiones. | ✅ Resuelto |
| **C-002** | 19-10-2026 | U1.2 Setup técnico | Consulta explícita: ¿En qué parte exacta de la U1.2 nos encontramos? | Se analizó la unidad en sus 3 bloques (B2: Repo/Commit, B3: Entorno Virtual/Dependencias, B4: Variables de entorno y Primera petición HTTP). Estamos en el cierre de la Actividad Práctica del Bloque 2 (falta armar estructura `src/`, `docs/`, `tests/`, `.gitignore` y commit), listos para avanzar a Bloque 3 y Bloque 4. | ✅ Resuelto |
| **C-003** | 19-10-2026 | U1.2 Bloque 2 | Explicación de por qué la Lección 2 se considera completada. | La Lección 2 ("Cómo armar en vivo un entorno completo, de cero a API") es demostrativa y referencial (`Hecho: Ver`). El texto estipula que el alumno solo debe observar y comprender el flujo global sin ejecutar código aún, pasando la acción práctica a la actividad siguiente ("Inicializa tu repositorio"). | ✅ Resuelto |
| **C-004** | 19-10-2026 | U1.2 Bloque 2 | Verificación de archivos traídos desde disco duro externo (Plantilla ZIP y PDFs). | Se verificó que los 40 PDFs y el ZIP de la plantilla corresponden exactamente al curso. Se identificaron correcciones estructurales: extraer la plantilla en la raíz del repo de código y reubicar la carpeta pesada de PDFs fuera de `Curso-CCHIA` para cumplir la rúbrica del Gate 1. | ✅ Resuelto |
| **C-005** | 19-10-2026 | U1.2 Bloque 2 | Reorganización y extracción de documentos del archivo ZIP en la carpeta particular de la lección. | Se crearon las carpetas organizadas en `Material de Estudio\`, se extrajeron los archivos de la plantilla base en la lección U1.2 (`Plantilla Repositorio Base`), y se desplegó la estructura requerida en la raíz de `Curso-CCHIA` dejando el repositorio listo para el primer commit. | ✅ Resuelto |
| **C-006** | 19-10-2026 | U1.2 Bloque 2 | Registro del commit formal de inicialización con la estructura base del repositorio. | Se versionaron y commitearon formalmente los archivos de la plantilla base (`src/`, `docs/`, `tests/`, `requirements.txt`, `README.md`, `.gitignore`, `.env.example`, `BITACORA_DE_AVANCE.md`) con el mensaje oficial `"Estructura base del repositorio"` (Commit `15b54e7`), empujando los cambios a GitHub. Bloque 2 completado exitosamente. | ✅ Resuelto |
| **C-007** | 19-10-2026 | Entorno y Herramientas | Consulta: ¿Se puede realizar el curso de la CCHIA empleando Antigravity en lugar de VS Code? | Sí, totalmente viable y ventajoso. Antigravity está construido sobre el ecosistema Code-OSS (VS Code), por lo que comparte terminal, extensiones y gestión de Git. Lo que evalúa el programa son los entregables en GitHub y la ejecución reproducible en terminal, no el editor utilizado. | ✅ Resuelto |
| **C-008** | 19-10-2026 | U1.2 Bloque 3 | Creación y uso eficiente de entornos virtuales, y validación mediante scripts comparativos. | Se creó el entorno virtual `.venv`, se instalaron `requests` y `python-dotenv`, se congeló en `requirements.txt`, y se construyó el programa `src/verificar_entorno.py` para demostrar empíricamente el aislamiento entre el entorno virtual y el global. | ✅ Resuelto |
| **C-009** | 19-10-2026 | U1.2 Bloque 3 | Error `CommandNotFoundException` al ejecutar `.\.venv\Scripts\Activate.ps1`. | El error se produjo porque la terminal estaba abierta en la carpeta raíz `Curso CCHIA` y no dentro del repositorio `Curso-CCHIA` (donde reside `.venv`). Se resolvió explicando la navegación con `cd Curso-CCHIA` y la selección del intérprete en Antigravity. | ✅ Resuelto |
| **C-010** | 19-10-2026 | U1.2 Bloque 3 | Cómo crear y gestionar 2 programas simples con versiones diferentes de librerías usando entornos separados. | Se explicó el problema del choque de dependencias y la solución mediante 2 entornos aislados (`venv_a` y `venv_b`) ejecutando versiones distintas de un mismo paquete sin interferencias. | ✅ Resuelto |
| **C-011** | 19-10-2026 | U1.2 Bloque 3 | Error `[Errno 2] No such file or directory: app.py` en app_antigua. | El usuario siguió correctamente los pasos de creación de carpeta, `.venv`, instalación de versión antigua (`urllib3==1.26.18`) y `requirements.txt`. El error se debió a que faltaba crear el archivo `app.py` en dicha carpeta antes de invocarlo. Se crearon `app.py` en `app_antigua` y `app_moderna`, comprobando la coexistencia de versiones. | ✅ Resuelto |
| **C-012** | 19-10-2026 | Git y Versionamiento | Consulta: ¿Todo lo que coloque en `.gitignore` no será contemplado por Git y GitHub? | Se detalló la regla general (ignora archivos no rastreados) y la regla de oro/excepción: si un archivo ya fue commiteado antes de añadirlo a `.gitignore`, Git continuará rastreándolo a menos que se use `git rm --cached`. Se vinculó con la protección de secretos (`.env`) del Gate 1. | ✅ Resuelto |
| **C-013** | 19-10-2026 | U1.2 Bloque 4 | Inicio y ejecución del Bloque 4: Variables de entorno y primera petición HTTP autenticada. | Configuración de `.env` a partir de `.env.example`, confirmación de exclusión activa en `.gitignore`, ejecución de petición HTTP 200 OK con Gemini API (`gemini-3.5-flash`), y generación de archivo de evidencia en `docs/evidencia_peticion_autenticada.json` con credenciales ofuscadas. | ✅ Resuelto |
| **C-014** | 19-10-2026 | U1.2 Bloque 4 | Validación del link y formato de entrega en Skillnest para el Bloque 4. | Se analizó la consigna oficial del Bloque 4 ("pega el enlace de tu repositorio de GitHub como texto en el campo de entrega"). Se confirmó que la pestaña "Enlace" es la correcta y se recomendó usar la URL web canónica `https://github.com/ayalaphysds/Curso-CCHIA` (sin el `.git`) para asegurar que el evaluador acceda directamente a la vista de código en el navegador sin redirecciones. Se verificó el cumplimiento de los 6 criterios de la lista de cotejo. | ✅ Resuelto |
| **C-015** | 19-10-2026 | U1.3 Bloque 5 | Desarrollo y ejecución completa de las actividades del Bloque 5. | Se implementó el módulo `src/consumir_gemini.py` con principio de responsabilidad única (extracción limpia y `return` del texto), lectura de variables de entorno y llamada HTTP POST con `requests`. Se validó la ejecución e importación del módulo con respuesta real de Gemini API. Se implementó el script de demostración de error de red en `tests/test_conexion.py`. | ✅ Resuelto |
| **C-016** | 19-10-2026 | U1.3 Bloque 6 | Refactorización del script en funciones reutilizables con responsabilidad única. | Se refactorizó `src/consumir_gemini.py` dividiéndolo en 3 funciones especializadas (`armar_peticion`, `enviar_peticion`, `extraer_texto`) y la coordinadora `obtener_dato_de_prueba`. Se mantuvieron la firma externa y el comportamiento intacto. Se validó cada función individualmente y de punta a punta. Se versionó bajo el commit `"Refactorizar módulo en funciones separadas"`. | ✅ Resuelto |
| **C-017** | 19-10-2026 | U1.3 Bloque 7 | Incorporación de manejo de excepciones y validación de entradas [Actividad Core]. | Se blindó `src/consumir_gemini.py` con validación temprana de entrada (`ValueError` ante strings vacíos), contención de errores de conexión/timeout (`RuntimeError`), control de formato JSON y datos faltantes (`RuntimeError`). Se desarrolló la suite de pruebas unitarias `tests/test_consumir_gemini.py` ejecutando 6 pruebas con 100% de éxito. Se versionó con el commit `"Incorporar manejo de excepciones y validación al módulo"`, cerrando la Unidad U1.3. | ✅ Resuelto |
| **C-018** | 20-10-2026 | U1.4 Bloque 8 | Consulta: ¿En el Bloque 8 debo diagramar la app que quiero crear o un diagrama genérico? | Se clarificó la rúbrica oficial: no debe ser un diagrama genérico ni tampoco inventar una app futura compleja. Debe reflejar el módulo real construido en Python (`armar_peticion`, `enviar_peticion`, `extraer_texto`, `calcular_costo`, `.env` y `try/except`). | ✅ Resuelto |
| **C-019** | 20-10-2026 | Portafolio / Capstone | Evaluación y feedback estratégico del proyecto personal `cenabast-procurement-optimization`. | Se analizó el repositorio completo: excelente formulación matemática/OR (solver HiGHS, HHI, ahorro de $24.000M CLP, Streamlit), pero carece aún de IA Generativa. Se diseñó la hoja de ruta para potenciarlo como el Capstone final del curso (Gate 2 con RAG y Function Calling, Gate 3 con FastAPI y Docker). | ✅ Resuelto |
| **C-020** | 20-10-2026 | U1.4 Bloque 8 | Generación formal del diagrama de arquitectura y subida a GitHub según la rúbrica oficial. | Se implementó la función `calcular_costo` en `src/consumir_gemini.py`, se ampliaron las pruebas unitarias (8/8 tests OK), se renderizó el diagrama de arquitectura oficial en alta resolución en `docs/diagrama_arquitectura.png` cumpliendo los 5 elementos exigidos, y se versionó y sincronizó con GitHub. | ✅ Resuelto |
| **C-021** | 20-10-2026 | U1.4 Bloque 9 | Ejecución completa de las actividades del Bloque 9: Benchmark de modelos y registro de decisión de arquitectura. | Se construyó el módulo de benchmarking `src/comparar_modelos.py`, se contrastaron datos empíricos de latencia y costos para Gemini 3.8 Flash vs Gemini 2.5 Pro, se redactó el documento formal `docs/decision-arquitectura.md` con las 5 secciones obligatorias de la rúbrica y se sincronizó con GitHub, cerrando la Unidad U1.4. | ✅ Resuelto |
| **C-022** | 20-10-2026 | U1.5 Bloque 10 | Prompt de sistema con salida JSON estructurada y validación de consistencia. | Se extendió `armar_peticion` con `systemInstruction` y `responseSchema`, se implementó `parsear_respuesta_json` con limpieza de bloques markdown, se creó el banco de 3 prompts especializados (`prompts/banco.py`), se ejecutó la suite de consistencia (`prompts/test_consistencia.py` con 3/3 éxitos en cada prompt) generando `prompts/registro_resultados.json` y se ampliaron los tests unitarios (13/13 passing). Se cerró la Unidad U1.5. | ✅ Resuelto |
| **C-023** | 20-10-2026 | U1.6 Bloque 11 | Ejecución de actividades de Gate 1: Habilitación técnica [Sumativa]. Validación de los 4 criterios no compensables, ensayo de instalación limpia y formalización de entrega. | Se creó el punto de entrada unificado `main.py`, se ejecutó y validó la instalación en entorno limpio aislado (scratch), se redactó el `README.md` técnico definitivo con comandos de instalación e informe del ensayo, se verificaron 13/13 tests y cero fugas de secretos en git. Se preparó la entrega oficial para Skillnest. | ✅ Gate 1 Aprobado |
| **C-024** | 22-10-2026 | U2.1 Bloque 12 | Implementación y verificación del cliente modular con reintentos y clasificación estricta de errores [Actividad Práctica]. | Se construyeron `cliente_api.py`, `cliente_reintento.py` y el módulo integrador `cliente.py` con `consultar_modelo()`. Se implementó la clasificación de excepciones (ValueError para auth, TimeoutError para rate limits/red), reintento transparente con `con_reintento()` y encapsulación del agotamiento de intentos en `RuntimeError`. Se verificaron empíricamente los 4 escenarios de la rúbrica (consulta normal, credencial inválida, reintento ante 429 simulado y agotamiento) y se validó la compatibilidad con el Gate 1 (13/13 tests pasando). | ✅ Resuelto |
| **C-025** | 02-11-2026 | Gate 1 / Documentación | Incorporación del contrato formal de interfaz del JSON de salida conforme al feedback del evaluador ("Documentar en el README el contrato de interfaz del JSON de salida para facilitar su consumo downstream"). | Se actualizó `Gate 1/README.md` documentando formalmente la especificación JSON Schema Draft 2020-12, el diccionario de campos tipados (`sobreprecio_detectado`, `desviacion_pct`, `recomendacion`, `dictamen`), restricciones numéricas/enum, 3 ejemplos reales representativos y la guía de deserialización downstream con modelo Pydantic v2. | ✅ Resuelto |
| **C-026** | 02-11-2026 | Arquitectura / Repo | Reestructuración física del repositorio en macro-carpetas `Gate 1/` y `Gate 2/` preservando el material de estudio global y el historial de Git. | Se ejecutó la migración mediante `git mv` moviendo el código, documentación, prompts y tests a `Gate 1/`, y creando la estructura base en `Gate 2/`. Se mantuvo `Material de Estudio` intacto en la raíz fuera del repo, se ajustaron `sys.path` dinámicos en tests y se creó `README.md` maestro de navegación. Suite Gate 1 validada 13/13 passing. | ✅ Resuelto |
| **C-027** | 02-11-2026 | Módulo 2 / Core Activities | Resolución integral de las 8 actividades core del Módulo 2 aplicadas a la optimización de precios CENABAST y elaboración de guía de entregas. | Se desarrollaron e implementaron los módulos correspondientes a los Bloques 14 a 32 (`test_cliente.py`, `revision_manual.py`, `enrutamiento.py`, `mi_agente.py`, `registro_rag.py`, `decision.py`, `registro_prompts.py`, `grafo_supervision.py`, `matriz_riesgos.py`). Se elaboró `Gate 2/GUIA_DE_ENTREGAS_MODULO_2.md` con instrucciones, comandos, capturas y evidencias para cada entrega en Skillnest. | ✅ Resuelto |
| **C-028** | 02-11-2026 | Gate 2 / RAG & Gobernanza | Implementación, evaluación y blindaje adversarial de la solución RAG modular de Gate 2 para análisis de compras CENABAST. | Se construyó el servicio RAG modular en `Gate 2/src/` con indexación Chroma recursiva, filtro anti-inyección (`seguridad.py`), recuperación con citación obligatoria (`recuperador.py`), observabilidad estructurada JSON sin PII (`observabilidad.py`) y supervisión humana con LangGraph (`supervision.py`). Se blindó el sistema contra ataques adversarios superando 106 tests en Gate 2 y obteniendo 98.8% en la rúbrica oficial. | ✅ Gate 2 Aprobado |

---

## 💻 6. Registro de Programas, Scripts y Artefactos de Código

| ID | Fecha | Archivo / Componente | Lenguaje / Tipo | Módulo / Unidad | Propósito / Funcionalidad | Estado |
| :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **PRG-001** | 19-10-2026 | [`BITACORA_DE_AVANCE.md`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/BITACORA_DE_AVANCE.md) | Markdown | General | Registro vivo del progreso del curso, consultas, programas generados y rúbricas. | ✅ Activo |
| **PRG-002** | 19-10-2026 | [`Gate 1/src/verificar_entorno.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%201/src/verificar_entorno.py) | Python | U1.2 Bloque 3 | Diagnóstico de entorno Python, verificación de aislamiento de `.venv` y comprobación de librerías instaladas. | ✅ Probado |
| **PRG-003** | 19-10-2026 | [`Gate 1/src/probar_conexion_api.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%201/src/probar_conexion_api.py) | Python | U1.2 Bloque 4 | Petición HTTP autenticada a Gemini API vía `requests`, comprobación de status 200 y generación de evidencia en `docs/`. | ✅ Probado y Generado |
| **PRG-004** | 20-10-2026 | [`Gate 1/src/consumir_gemini.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%201/src/consumir_gemini.py) | Python | U1.5 Bloque 10 | Módulo central de integración con Gemini API: soporte para `systemInstruction`, forzado de salida estructurada `responseSchema` en `generationConfig`, `calcular_costo` y deserialización robusta con `parsear_respuesta_json`. | ✅ Actualizado Bloque 10 |
| **PRG-005** | 19-10-2026 | [`Gate 1/tests/test_conexion.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%201/tests/test_conexion.py) | Python | U1.3 Bloque 5 | Script de demostración de error de red inducido a propósito y contención controlada vía `try-except`. | ✅ Probado |
| **PRG-006** | 20-10-2026 | [`Gate 1/tests/test_consumir_gemini.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%201/tests/test_consumir_gemini.py) | Python | U1.5 Bloque 10 | Suite de pruebas unitarias (`unittest`) con 13 tests automatizados: validaciones tempranas, URLs, errores de red/timeout/JSON, extracción, cálculo de costo, esquemas estructurados y parseo. | ✅ 13/13 Tests Passing |
| **PRG-007** | 20-10-2026 | [`Gate 1/docs/diagrama_arquitectura.png`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%201/docs/diagrama_arquitectura.png) | Imagen PNG | U1.4 Bloque 8 | Diagrama oficial de arquitectura de la miniaplicación cumpliendo los 5 criterios exigidos en la rúbrica (funciones reales, `.env`, `try/except`, `usageMetadata` y flechas tipadas). | ✅ Generado y Commiteado |
| **PRG-008** | 20-10-2026 | [`Gate 1/src/comparar_modelos.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%201/src/comparar_modelos.py) | Python | U1.4 Bloque 9 | Módulo de benchmark comparativo entre modelos candidatos (Gemini Flash vs Pro): medición de latencia empírica, cálculo de costo por token y proyección a escala. | ✅ Probado |
| **PRG-009** | 20-10-2026 | [`Gate 1/docs/decision-arquitectura.md`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%201/docs/decision-arquitectura.md) | Markdown | U1.4 Bloque 9 | Registro formal de decisión de arquitectura (ADR) que documenta el modelo elegido, diagrama vinculado, tabla comparativa con datos reales, justificación y razones de descarte. | ✅ Entregable Oficial |
| **PRG-010** | 20-10-2026 | [`Gate 1/prompts/banco.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%201/prompts/banco.py) | Python | U1.5 Bloque 10 | Banco de 3 prompts especializados con `system_instruction`, `ejemplo_usuario`, `claves_esperadas` y `response_schema` para auditoría pública. | ✅ Entregable Bloque 10 |
| **PRG-011** | 20-10-2026 | [`Gate 1/prompts/test_consistencia.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%201/prompts/test_consistencia.py) | Python | U1.5 Bloque 10 | Script de evaluación empírica de consistencia (3 repeticiones por prompt) que valida JSON y claves obligatorias. | ✅ Ejecutado y Validado |
| **PRG-012** | 20-10-2026 | [`Gate 1/prompts/registro_resultados.json`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%201/prompts/registro_resultados.json) | JSON | U1.5 Bloque 10 | Registro estructurado de consistencia del banco de prompts: 3/3 éxitos (100% consistencia) en cada uno de los prompts evaluados. | ✅ Evidencia Oficial |
| **PRG-013** | 20-10-2026 | [`Gate 1/main.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%201/main.py) | Python | U1.6 Bloque 11 | Punto de entrada unificado y ejecutable para el Gate 1: orquesta validación de entorno (.env), invocación a Gemini API con JSON estructurado, cálculo de costos y renderizado legible en consola. | ✅ Entregable Oficial Gate 1 |
| **PRG-014** | 22-10-2026 | [`Gate 2/cliente_api.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%202/cliente_api.py) | Python | U2.1 Bloque 12 | Módulo de cliente HTTP para Gemini API con clasificación estricta de errores por código de estado (401/403/400 -> ValueError, 429/500/red -> TimeoutError) y armado de payload. | ✅ Probado |
| **PRG-015** | 22-10-2026 | [`Gate 2/cliente_reintento.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%202/cliente_reintento.py) | Python | U2.1 Bloque 12 | Función de orden superior `con_reintento()` que intercepta TimeoutError, ejecuta pausas parametrizadas y respeta límites de reintento sin ocultar errores de autenticación. | ✅ Probado |
| **PRG-016** | 22-10-2026 | [`Gate 2/cliente.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%202/cliente.py) | Python | U2.1 Bloque 12 | Cliente modular unificado con función pública `consultar_modelo()`: orquesta armado de payload, reintento transparente, traducción de fallas a RuntimeError y suite de verificación con 4 escenarios. | ✅ Entregable Bloque 12 |
| **PRG-017** | 02-11-2026 | [`Gate 2/GUIA_DE_ENTREGAS_MODULO_2.md`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%202/GUIA_DE_ENTREGAS_MODULO_2.md) | Markdown | Módulo 2 | Guía integral para el estudiante detallando archivos, capturas, comandos y evidencias exactas a subir en Skillnest para los Bloques 14 a 32. | ✅ Entregable Oficial |
| **PRG-018** | 02-11-2026 | [`Gate 2/servicio_rag.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%202/servicio_rag.py) | Python | Gate 2 | Entrypoint del servicio RAG de análisis de precios CENABAST: orquesta indexación, seguridad, recuperación semántica y síntesis con citación obligatoria. | ✅ Entregable Oficial Gate 2 |
| **PRG-019** | 02-11-2026 | [`Gate 2/src/seguridad.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%202/src/seguridad.py) | Python | U2.7 / Gate 2 | Módulo de seguridad y mitigación de inyección de prompts: sanitiza entradas y descarta documentos contaminados antes de alcanzar el LLM. | ✅ Probado |
| **PRG-020** | 02-11-2026 | [`Gate 2/src/observabilidad.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%202/src/observabilidad.py) | Python | U2.7 / Gate 2 | Logger estructurado JSON con propagación de `trace_id` por contexto, métricas de tokens y omisión estricta de PII y texto crudo. | ✅ Probado |
| **PRG-021** | 02-11-2026 | [`Gate 2/src/indexador.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%202/src/indexador.py) | Python | U2.5 / Gate 2 | Módulo de indexación RAG con chunking recursivo optimizado, embeddings semánticos y almacenamiento persistente en Chroma (`indice_gate2/`). | ✅ Probado |
| **PRG-022** | 02-11-2026 | [`Gate 2/src/recuperador.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%202/src/recuperador.py) | Python | U2.5 / Gate 2 | Recuperador semántico y generador de respuestas RAG con forzado de citación estricta de documentos fuente `[fuente: <doc>]`. | ✅ Probado |
| **PRG-023** | 02-11-2026 | [`Gate 2/src/supervision.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%202/src/supervision.py) | Python | U2.7 / Gate 2 | Grafo de supervisión humana LangGraph: interrupción interactiva (`interrupt`) ante desvíos críticos de precios y reanudación con `Command(resume=True)`. | ✅ Probado |
| **PRG-024** | 02-11-2026 | [`Gate 2/src/cliente_rag.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%202/src/cliente_rag.py) | Python | Gate 2 | Cliente de integración LLM y mock semántico de alta fidelidad para ejecución determinista y reproducible sin claves externas. | ✅ Probado |
| **PRG-025** | 02-11-2026 | [`Gate 2/test_gate2.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%202/test_gate2.py) | Python | Gate 2 | Suite oficial de validación de los 4 criterios no compensables de la rúbrica oficial de Gate 2 (13 tests oficiales pasando). | ✅ Probado |
| **PRG-026** | 02-11-2026 | [`Gate 2/rubrica_gate2.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%202/rubrica_gate2.py) | Python | Gate 2 | Evaluador automático y cuantitativo ponderado de las 6 dimensiones de la rúbrica oficial (98.8% de nota final y veredicto APROBADO). | ✅ Probado |
| **PRG-027** | 24-11-2026 | [`Gate 3/docs/ficha_diseno_funcional.md`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%203/docs/ficha_diseno_funcional.md) | Markdown | U3.1 Bloque 34 | Ficha de diseño funcional completa (5 secciones, 6 RF, 3 RNF, 8 CA, 5 hitos y revisión cruzada) verificada con `verificar_ficha_completa.py` (5/5). | ✅ Entregable Core B34 |
| **PRG-028** | 24-11-2026 | [`Gate 3/servicio/main.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%203/servicio/main.py) | Python / FastAPI | U3.2 Bloque 36 | API FastAPI en 3 capas (`/salud`, `/consultas`, `/precios/evaluar`, `/licitaciones/{id}`), contrato uniforme de errores y 12/12 casos en `docs/registro_pruebas.md`. | ✅ Entregable Core B36 |
| **PRG-029** | 24-11-2026 | [`Gate 3/compose.yaml`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%203/compose.yaml) | Docker / YAML | U3.3 Bloque 38 | Composición de 2 servicios (`api` :8000 e `interfaz` :8080), Dockerfiles no-root con `HEALTHCHECK` (7/7), higiene de secretos y verificación cruzada (7/7). | ✅ Entregable Core B38 |
| **PRG-030** | 24-11-2026 | [`Gate 3/docs/registro_ejecucion.md`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%203/docs/registro_ejecucion.md) | Markdown / Python | U3.4 Bloque 41 | Pruebas parciales aisladas (5/5), 14 escenarios E2E repetibles (5/5), bitácora de ajustes y registro auditable validado con `verificar_registro.py` (6/6). | ✅ Entregable Core B41 |
| **PRG-031** | 24-11-2026 | [`Gate 3/docs/matriz_riesgos.md`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%203/docs/matriz_riesgos.md) | Markdown / Python | U3.5 Bloque 43 | Matriz de Pruebas (6/6), detector de alucinaciones en salida, 17/17 mitigaciones de seguridad y Matriz de 9 Riesgos con evidencia ejecutable (6/6). | ✅ Entregable Core B43 |
| **PRG-032** | 24-11-2026 | [`Gate 3/docs/decisiones.md`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%203/docs/decisiones.md) | Markdown / Python | U3.6 Bloque 45 | 6 ADRs vigentes (`D-01..D-06`), 3 limitaciones trazadas (`LIM-01..LIM-03`), `docs/api.md`, prueba de transferencia (5/5), README verificado (8/8) y prueba en frío (5/5). | ✅ Entregable Core B45 |
| **PRG-033** | 24-11-2026 | [`Gate 3/verificar_gate3.py`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%203/verificar_gate3.py) | Python | U3.7 Gate 3 | Verificador maestro del Capstone (22 fuentes, rúbrica 100 pts, 4 no compensables), ensayo en vivo (`ensayo_demo.py` 8/8), guion (`medir_guion.py` 9/9) y `docs/gate3.md`. | ✅ Entregable Gate 3 |
| **PRG-034** | 24-11-2026 | [`Gate 3/GUIA_DE_ENTREGAS_MODULO_3.md`](file:///c:/Users/sayal/OneDrive/Desktop/Curso%20CCHIA/Curso-CCHIA/Gate%203/GUIA_DE_ENTREGAS_MODULO_3.md) | Markdown | Módulo 3 | Guía maestra con enlaces directos de GitHub y comandos de verificación para cada actividad Core del Módulo 3 y Gate 3 en Skillnest. | ✅ Entregable Oficial |

---

## 📅 7. Historial de Sesiones de Trabajo

### Sesión 1 — 19 de Octubre de 2026
- **Objetivo de la sesión:** Inicialización del sistema de bitácora y sincronización del estado del curso.
- **Acciones realizadas:**
  - Inspección del repositorio local `Curso-CCHIA`.
  - Análisis del historial de commits (`2c985e0` v1 con material curricular y `3275661` v2).
  - Extracción y mapeo del plan de estudios de la *Especialización IA Accenture*: 3 Módulos, 21 Unidades, 47 Bloques, 3 Gates y sistema de cinturones.
  - Creación del documento formal `BITACORA_DE_AVANCE.md` en el repositorio y directorio de trabajo.
- **Próximos pasos acordados:**
  - Continuar con la Unidad **U1.2: Setup técnico** (estructurar el repositorio, entorno virtual `.venv`, archivo `.gitignore` para secretos y script de prueba de API HTTP).

### Sesión 2 — 20 de Octubre de 2026
- **Objetivo de la sesión:** Ejecución integral de las Unidades U1.3, U1.4, U1.5 y cierre sumativo con el Gate 1 (U1.6 / Bloque 11).
- **Acciones realizadas:**
  - **U1.3:** Implementación modular de `src/consumir_gemini.py` con responsabilidad única, validación temprana y manejo robusto de excepciones; suite de pruebas unitarias (`tests/test_consumir_gemini.py`).
  - **U1.4:** Adición de función `calcular_costo`, renderizado en alta resolución del diagrama de arquitectura (`docs/diagrama_arquitectura.png`), script de benchmark de modelos (`src/comparar_modelos.py`) y redacción del ADR formal (`docs/decision-arquitectura.md`).
  - **U1.5:** Incorporación de `systemInstruction` y schemas tipados (`responseSchema`), creación de `prompts/banco.py`, script de consistencia `prompts/test_consistencia.py` y generación de `prompts/registro_resultados.json` con 100% de consistencia.
  - **U1.6 (Gate 1):** Creación del punto de entrada autónomo `main.py`, redacción exhaustiva de `README.md` con checklist de criterios no compensables, realización exitosa del ensayo de instalación limpia en entorno aislado, y ejecución de la entrega formal.
- **Resultado:**
  - **Módulo 1 Completado al 100% — Gate 1 Aprobado (20% de la nota final asegurado).**

### Sesión 3 — 22 de Octubre de 2026
- **Objetivo de la sesión:** Inicio del Módulo 2 y desarrollo integral del **Bloque 12 (Cliente modular de consumo de APIs, con reintentos)**.
- **Acciones realizadas:**
  - Inspección del material curricular y requerimientos de la Unidad U2.1.
  - Implementación de `cliente_api.py`: separación de errores de autenticación (401/403/400 inválido -> `ValueError`) de errores transitorios de red/proveedor (429/500/timeout -> `TimeoutError`).
  - Implementación de `cliente_reintento.py`: función genérica `con_reintento()` para reintento automático con pausas configurables.
  - Creación del cliente modular integrador `cliente.py`: interfaz unificada `consultar_modelo()` con manejo de agotamiento de intentos convertido a `RuntimeError`.
  - Ejecución de la batería de pruebas en consola validando los 4 escenarios de la rúbrica oficial (consulta normal con Gemini 3.5 Flash, API key inválida inmediata, reintento ante 429 simulado y agotamiento).
  - Verificación de no regresión en la suite de pruebas del Gate 1 (13/13 tests pasando).
- **Resultado:**
  - **Bloque 12 completado al 100% y listo para versionamiento formal.**

### Sesión 4 — 2 de Noviembre de 2026
- **Objetivo de la sesión:** Reestructuración física del repositorio en macro-carpetas `Gate 1/` y `Gate 2/`, documentación del contrato JSON downstream de Gate 1, resolución secuencial de las 8 actividades core del Módulo 2 y desarrollo integral del servicio RAG para Gate 2 (precios CENABAST).
- **Acciones realizadas:**
  - **1. Correcciones de Gate 1:**
    - Documentación formal del contrato JSON de interfaz en `Gate 1/README.md` (JSON Schema Draft 2020-12, diccionario exhaustivo de campos, tipos y restricciones, 3 ejemplos reales representativos de salida y guía de deserialización downstream con modelo Pydantic v2).
    - Preservación y verificación de la suite de pruebas unitarias de Gate 1 (13/13 tests passing sin regresión).
  - **2. Reestructuración de Carpetas (`git mv`):**
    - Organización del repositorio en macro-carpetas `Gate 1/` y `Gate 2/`, preservando la trazabilidad completa del historial Git (`git log --follow`).
    - Verificación y aislamiento de `Material de Estudio` 100% intacto en el directorio superior fuera de las carpetas gate.
    - Creación del `README.md` maestro de navegación en la raíz de `Curso-CCHIA`.
  - **3. Resolución de Actividades Core del Módulo 2:**
    - Implementación de actividades para Bloques 14 a 32: `test_cliente.py` (B14), `revision_manual.py` y métricas (B17), `enrutamiento.py` con LCEL (B20), `mi_agente.py` con herramientas y control de riesgo (B23), `registro_rag.py` y observabilidad k=3 vs k=6 (B28), `decision.py` y ADR de adaptación (B30), `registro_prompts.py`, `grafo_supervision.py` y matriz de riesgos (B32).
    - Redacción de `Gate 2/GUIA_DE_ENTREGAS_MODULO_2.md` con evidencias paso a paso, archivos exactos, capturas y comandos para la plataforma Skillnest.
  - **4. Implementación y Blindaje de Gate 2:**
    - Construcción del servicio modular RAG CENABAST (`Gate 2/servicio_rag.py`) con base vectorial Chroma (`indice_gate2/`) a partir de 5 documentos normativos y de licitaciones hospitalarias.
    - Mitigación activa contra inyecciones adversarias (`Gate 2/src/seguridad.py`).
    - Citación explícita de fuentes normativas en todas las respuestas (`[fuente: <doc>]`).
    - Observabilidad JSON estructurada con métricas operativas y omisión estricta de PII (`Gate 2/src/observabilidad.py`).
    - Supervisión humana interactiva implementada en LangGraph con punto de interrupción interactivo (`interrupt`) y reanudación controlada (`Gate 2/src/supervision.py`).
    - Ejecución de suites completas: 106 tests aprobados en Gate 2, 13 tests en Gate 1, y autoevaluación oficial de rúbrica en 98.8% (Aprobado en Oportunidad 1).
- **Resultado:**
  - **Módulo 2 Completado al 100% — Gate 2 Aprobado (55% acumulado de la nota final: 20% M1 + 35% M2). Todo el repositorio listo y verificado para abordar el Módulo 3 (Capstone Project).**

### Sesión 5 — 24 de Noviembre de 2026
- **Objetivo de la sesión:** Limpieza y normalización de nombres de los 50 PDFs de `Material de Estudio/Módulo 3` (resolviendo desbordamiento `MAX_PATH` en Windows y erratas de Skillnest), desarrollo completo de las 6 actividades Core del Módulo 3 (Bloques 34, 36, 38, 41, 43 y 45) y construcción del **Gate 3 Capstone** aplicado a la plataforma end-to-end de auditoría de precios CENABAST.
- **Acciones realizadas:**
  - **U3.1 (Bloques 33–34 Core):** Ficha de diseño funcional completa (`docs/ficha_diseno_funcional.md`), diagrama de arquitectura (`docs/diagrama_arquitectura.png`), revisión cruzada (`docs/revision_alcance.md`) y verificador `verificar_ficha_completa.py` (5/5).
  - **U3.2 (Bloques 35–36 Core):** Servicio FastAPI de 3 capas (`servicio/main.py`, `esquemas.py`, `errores.py`, `logica.py`), 12 casos válidos/inválidos en `casos.py` ejecutados en `pytest` y vía cliente HTTP externo (`docs/registro_pruebas.md` 12/12).
  - **U3.3 (Bloques 37–38 Core):** Contenerización no-root con `HEALTHCHECK` para API e Interfaz Web (`Dockerfile`, `interfaz/Dockerfile`, `compose.yaml`), auditoría de secretos (`buscar_secretos.py`), verificación cruzada (`docs/verificacion_cruzada.md`) y `verificar_entrega.py` (7/7).
  - **U3.4 (Bloques 39–41 Core):** 6 suites de pruebas parciales aisladas (`verificar_parciales.py` 5/5 + mutación en `verificar_defectos.py`), 14 escenarios E2E repetibles sobre API + Interfaz (`verificar_ejecucion.py` 5/5), bitácora de ajustes (`docs/bitacora_ajustes.md`) y registro auditable (`docs/registro_ejecucion.md`, `verificar_registro.py` 6/6).
  - **U3.5 (Bloques 42–43 Core):** Matriz de Pruebas trazada a la ficha (`verificar_matriz.py` 6/6), detector de alucinaciones en salida (`servicio/fundamentacion.py`), 17/17 mitigaciones de ataques/alucinaciones/fugas (`verificar_mitigaciones.py`) y Matriz de 9 Riesgos con evidencia ejecutable (`verificar_riesgos.py` 6/6).
  - **U3.6 (Bloques 44–45 Core):** `README.md` técnico verificado (8/8), prueba en frío sobre clon limpio (`probar_en_frio.py` 5/5), referencia viva `docs/api.md` (6/6), prueba cruzada de transferencia (`docs/transferencia.md` 5/5), 6 ADRs (`docs/decisiones.md`) y 3 limitaciones trazadas (`docs/limitaciones.md`, `verificar_decisiones.py` 7/7).
  - **U3.7 (Gate 3 Capstone):** Guion de defensa técnica de 8 minutos (`docs/defensa.md`, `medir_guion.py` 9/9), ensayo cronometrado de 7 pasos (`ensayo_demo.py` 8/8 en ~110 s + plan B `docs/demo_respaldo.md`), rúbrica como datos (`rubrica_gate3.py`) y verificador maestro (`verificar_gate3.py` -> `docs/gate3.md`, 19/19 fuentes locales al 100%, 83/83 tests en verde).
- **Resultado:**
  - **Módulo 3 y Gate 3 Capstone implementados, verificados y listos para entrega en Skillnest y defensa técnica en vivo (100% del programa completado en repositorio).**

---

## ⚙️ 8. Protocolo de Actualización de la Bitácora
1. **Tras cada consulta o pregunta técnica:** Agregar una fila a la tabla de **Consultas y Preguntas** con la respuesta o conclusión.
2. **Tras generar o modificar un script/programa:** Agregar o actualizar la fila correspondiente en la tabla de **Programas y Artefactos de Código**.
3. **Al completar una actividad, bloque o unidad:** Marcar la casilla correspondiente con `[x]` en el **Mapa de Avance** y actualizar el indicador `📍 [ESTAMOS AQUÍ]`.
4. **Alcanzar un Gate:** Verificar previamente los 4 criterios no compensables y registrar el resultado de la evaluación.
