# Ficha de Diseño Funcional

**Proyecto:** Plataforma End-to-End de Auditoría Inteligente de Precios y Licitaciones CENABAST
**Autor:** Sebastián Eduardo Ayala Vásquez
**Programa:** Especialización en Inteligencia Artificial — Accenture / CCHIA (Módulo 3 — Gate 3 Capstone)

---

## 1. Problema de negocio

Los analistas de adquisiciones de CENABAST revisan diariamente ofertas de medicamentos esenciales, bases administrativas y antecedentes históricos dispersos en múltiples documentos normativos antes de emitir recomendaciones de adjudicación. Hoy esa verificación se realiza de forma manual cruzando planillas y textos regulatorios, lo que consume en promedio 35 minutos por renglón licitado (estimación operativa basada en 40 líneas por licitación) y expone al organismo a adjudicar ofertas con sobreprecio superior al 15% o a omitir reglas de cadena de frío y cupos máximos. El resultado esperado es reducir el tiempo de pre-auditoría a menos de 2 minutos por consulta, con trazabilidad documental exacta hacia las bases oficiales y detección automática de desvíos críticos de precio antes de comprometer presupuesto público.

---

## 2. Requerimientos y alcance (MVP)

### Requerimientos funcionales

- RF-01: Consultar normativa, catálogo de precios de referencia 2026 y políticas de abastecimiento CENABAST en lenguaje natural, devolviendo una respuesta fundamentada que cite explícitamente el archivo fuente oficial (`[fuente: <documento>.md]`) o declare ausencia de información cuando el corpus no la contenga.
- RF-02: Evaluar una oferta unitaria de medicamento mediante su código ONU y precio ofertado en CLP, calculando la desviación porcentual respecto a la mediana histórica 2026, clasificando el umbral (`COMPETITIVO`, `NEGOCIACION`, `SOBREPRECIO_CRITICO`, `TEMERARIO`) e indicando si exige supervisión humana obligatoria.
- RF-03: Consultar precedentes de licitaciones hospitalarias históricas mediante su identificador (`LIC-NNN`), retornando fármaco, proveedor, desviación registrada y dictamen de auditoría, o respondiendo con error uniforme `404` cuando el identificador no existe.
- RF-04: Exponer una interfaz web liviana y un gateway HTTP desacoplado de la API principal que permita a un evaluador enviar consultas y revisar precedentes sin invocar código Python directamente.
- RF-05: Exportar minutas de pre-auditoría y resultados de comparación de ofertas en formato PDF/Excel descargable para el expediente electrónico.
- RF-06: Integrar emisión directa de órdenes de compra hacia Mercado Público con firma electrónica avanzada y pronóstico macroeconómico de fletes internacionales 2027.

### Requerimientos no funcionales

- RNF-01: Latencia de respuesta inferior a 2000 ms (p95) por petición HTTP sobre el conjunto de 14 escenarios simulados ejecutados contra la API en local o en contenedor.
- RNF-02: Tasa de contención de 100% ante entradas con formato inválido (`422`), rutas/recursos inexistentes (`404`) y métodos no permitidos (`405`), devolviendo siempre el contrato de error uniforme sin exponer trazas internas ni secretos en los 11 casos de la suite `casos.py`.
- RNF-03: Cero exposición de credenciales (`GEMINI_API_KEY`) o datos personales (PII) en el repositorio Git, imágenes Docker ni registros de auditoría, verificado mediante `buscar_secretos.py` y la batería de 3 pruebas de fuga en `verificar_mitigaciones.py`.

### Alcance

Imprescindible: RF-01, RF-02, RF-03, RF-04
Deseable: RF-05
Fuera de alcance: RF-06 (la emisión legal de órdenes de compra con firma digital avanzada y el pronóstico macroeconómico 2027 dependen de integraciones externas de ChileCompra y series financieras fuera del alcance del programa)

---

## 3. Arquitectura de la solución

Diagrama: docs/diagrama_arquitectura.png

La solución sigue una arquitectura de dos servicios contenerizados orquestados con Docker Compose y separados por una red interna:

- **Modelo:** Adaptador dual (`ModeloSimulado` determinista para ejecución reproducible y pruebas sin red, y `ModeloGemini` vía API REST cuando `MODELO=real` con clave inyectada por entorno), con modo de respaldo explícito y trazable.
- **Vector store:** Recuperador híbrido determinista en `servicio/recuperador.py` sobre el corpus oficial `data/` (5 documentos normativos CENABAST en Markdown), complementando la experiencia con ChromaDB del Gate 2 sin requerir descargas externas al levantar contenedores.
- **Orquestación:** Pipeline modular de 4 capas en `servicio/cadena.py` (filtro de seguridad de entrada, recuperación de fragmentos, construcción de prompt versionado + generación y verificador de fundamentación contra alucinaciones).
- **Exposición:** API HTTP en FastAPI (`API FastAPI` en puerto `8000`) con validación Pydantic v2 y contrato uniforme de errores, consumida por el servicio `Interfaz Web` (FastAPI en puerto `8080`) a través de `http://api:8000`.
- **Empaquetado:** Dos imágenes Docker independientes basadas en `python:3.12-slim` sin usuario `root`, con `HEALTHCHECK`, exclusión estricta de secretos mediante `.dockerignore` y `.env` montado solo en tiempo de ejecución vía `compose.yaml`.

---

## 4. Criterios de aceptación

- CA-01 (RF-01): Una petición `POST /consultas` con `"Cual es el precio de referencia del Paracetamol 500 mg?"` retorna HTTP `200`, incluye `"22.40"` en la respuesta y cita `"cenabast_catalogo_precios_referencia_2026.md"` en `fuentes`.
- CA-02 (RF-01): Una petición `POST /consultas` sobre un tema ausente del corpus (`"Cual es la temperatura en Marte hoy?"`) retorna HTTP `200`, contiene `"No encuentro esa informacion"` y devuelve una lista `fuentes` vacía (`0` elementos).
- CA-03 (RF-02): Una petición `POST /precios/evaluar` con `codigo_onu="51181504"` y `precio_ofertado=33.6` retorna HTTP `200` con `desviacion_pct=50.0`, `categoria="SOBREPRECIO_CRITICO"` y `requiere_supervision=true`.
- CA-04 (RF-03): Una petición `GET /licitaciones/LIC-723` retorna HTTP `200` con `"Paracetamol"` y `"RECHAZAR"`, mientras que `GET /licitaciones/LIC-999` retorna HTTP `404` con `"codigo": "no_encontrado"`.
- CA-05 (RF-04): Una petición `GET /preguntar?texto=precio+Paracetamol` sobre la `Interfaz Web` (puerto `8080`) devuelve HTTP `200` e incluye `"fuentes"` obtenidas desde la `API FastAPI`.
- CA-06 (RNF-01): El 100% de los 7 pasos de `ensayo_demo.py` responden en menos de `2.0` segundos por petición y completan la demostración completa en menos de `120` segundos.
- CA-07 (RNF-02): Los 11 casos de `casos.py` (4 válidos y 7 inválidos cubriendo `404`, `405` y `422`) pasan al `100%` tanto en `pytest` como mediante cliente HTTP externo, devolviendo siempre el esquema `ErrorRespuesta`.
- CA-08 (RNF-03): La ejecución de `buscar_secretos.py` completa `5` de `5` comprobaciones sin fugas y `verificar_mitigaciones.py` verifica las `3` pruebas de no-fuga (`F-01`, `F-02`, `F-03`) y la contención de ataques de inyección (`A-01` a `A-06`).

---

## 5. Plan de construcción por hitos

Horas disponibles: 24 h
Margen de imprevistos: 4 h

- H1 (4 h): Diseño funcional completo, arquitectura y criterios verificables de CENABAST. Cubre: RF-01, RF-02, RF-03. Se comprueba con: CA-01, CA-02, CA-03, CA-04.
- H2 (5 h): Servicio backend FastAPI de tres capas, validación Pydantic, contrato uniforme de errores y pruebas HTTP externas. Cubre: RF-01, RF-02, RF-03, RNF-02. Se comprueba con: CA-01, CA-02, CA-03, CA-04, CA-07.
- H3 (4 h): Contenerización con Docker, interfaz web en puerto 8080, higiene de secretos y composición con Docker Compose. Cubre: RF-04, RNF-03. Se comprueba con: CA-05, CA-08.
- H4 (4 h): Pruebas parciales por componente, ejecución end-to-end con 14 escenarios simulados, bitácora de ajustes y registro auditable. Cubre: RF-01, RF-02, RF-03, RF-04, RNF-01. Se comprueba con: CA-01, CA-02, CA-05, CA-06.
- H5 (3 h): QA adversarial, detección de alucinaciones, matriz de riesgos con evidencia ejecutable, documentación técnica, defensa y ensayo Gate 3. Cubre: RNF-01, RNF-02, RNF-03. Se comprueba con: CA-06, CA-07, CA-08.
