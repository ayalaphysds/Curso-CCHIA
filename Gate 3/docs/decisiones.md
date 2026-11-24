# Decisiones de arquitectura

## D-01 Recuperador híbrido léxico determinista sobre corpus Markdown

- **Estado:** vigente
- **Contexto:** El servicio RAG CENABAST debe indexar 5 documentos oficiales (precios 2026, bases, historial, políticas y protocolo de supervisión) y arrancar en menos de 2 segundos en pruebas locales, clones en frío y contenedores Docker sin descargar pesos neuronales de red.
- **Decisión:** Implementar un recuperador léxico ponderado por dominio farmacéutico con partición por secciones y filas de catálogo en `servicio/recuperador.py`, manteniendo la compatibilidad arquitectónica con RAG vectorial del Gate 2.
- **Alternativas descartadas:** Desplegar ChromaDB con modelos de embeddings descargados de HuggingFace en arranque (añade cientos de MB a la imagen Docker y falla sin internet) o utilizar búsqueda literal exacta por subcadenas (no tolera tildes ni orden distinto de palabras).
- **Costo:** No resuelve sinónimos coloquiales ni consultas en otros idiomas (limitación registrada explícitamente como `LIM-02` y cubierta por `R-09`).

## D-02 Falla honesta HTTP 503 cuando falta clave del modelo real

- **Estado:** vigente
- **Contexto:** Cuando un despliegue configura `MODELO=real` sin inyectar `GEMINI_API_KEY`, sustituir silenciosamente el LLM por un mock engaña a auditores y evaluadores sobre qué componente generó el dictamen.
- **Decisión:** Lanzar `ModeloNoDisponibleError` traducido a HTTP `503` (`codigo: modelo_no_disponible`) por defecto, permitiendo degradar a respaldo únicamente si el operador declara explícitamente `PERMITIR_RESPALDO=1` con advertencia visible en `/salud` y `/consultas`.
- **Alternativas descartadas:** Degradar silenciosamente al modelo simulado ante cualquier error de credenciales (oculta fallos de configuración en producción) o exigir `GEMINI_API_KEY` al importar la aplicación (rompe el arranque de pruebas unitarias offline).
- **Costo:** Exige configurar explícitamente `MODELO=simulado` o `PERMITIR_RESPALDO=1` en ambientes sin clave de API, y añade una rama adicional de validación en `servicio/respaldo.py`.

## D-03 Contrato uniforme de errores HTTP sin exposición de trazas

- **Estado:** vigente
- **Contexto:** Clientes externos y auditores necesitan respuestas predecibles ante entradas inválidas (`422`), expedientes inexistentes (`404`), métodos incorrectos (`405`) o fallos inesperados (`500`) sin filtrar stack traces ni variables de entorno.
- **Decisión:** Registrar manejadores globales en `servicio/errores.py` que devuelven siempre `ErrorRespuesta` (`codigo`, `mensaje` y `campos` opcional) y registran solo método, ruta y tipo de excepción en errores `500`.
- **Alternativas descartadas:** Mantener el formato heterogéneo por defecto de FastAPI/Starlette (mezcla `detail` como lista y como texto) o devolver mensajes crudos de excepción para depuración rápida (riesgo de fuga de credenciales y estructura interna).
- **Costo:** Requiere mantener sincronizados los códigos de error estables en `servicio/errores.py`, la documentación OpenAPI (`ERRORES`) y las pruebas de contrato en `casos.py`.

## D-04 Separación en dos contenedores con Docker Compose

- **Estado:** vigente
- **Contexto:** Un evaluador externo debe poder probar la solución tanto desde una interfaz web simple como contra la API HTTP sin acoplar la lógica de presentación al motor de auditoría ni depender de `localhost` entre contenedores.
- **Decisión:** Empaquetar `API FastAPI` (`Dockerfile`, puerto `8000`) e `Interfaz Web` (`interfaz/Dockerfile`, puerto `8080`) como imágenes independientes no-root con `HEALTHCHECK`, orquestadas en `compose.yaml` con `depends_on: condition: service_healthy` y comunicación vía `http://api:8000`.
- **Alternativas descartadas:** Servir HTML y API en un único contenedor monolítico (impide demostrar composición real de servicios y tolerancia a indisponibilidad `502`) o levantar dos comandos `docker run` manuales (frágil y no reproducible).
- **Costo:** Duplica la mantención de `Dockerfile`, `.dockerignore` y `requirements.txt` entre la API y la interfaz, e incrementa el tiempo de construcción inicial de imágenes.

## D-05 Capa determinista de verificación de fundamentación en salida

- **Estado:** vigente
- **Contexto:** En compras públicas de medicamentos, una alucinación con precios falsos, fuentes inventadas o inversión de la política de sobreprecio crítico (> 15%) produce daño patrimonial directo aunque tenga redacción convincente.
- **Decisión:** Insertar `servicio/fundamentacion.py` al final de `servicio/cadena.py` para bloquear y sustituir por `SIN_INFORMACION` cualquier respuesta sin cita válida, con fuentes inventadas, cifras ausentes del contexto o contradicción de política crítica.
- **Alternativas descartadas:** Confiar exclusivamente en instrucciones del prompt del sistema (vulnerable ante variaciones del modelo) o añadir una segunda llamada LLM-como-juez en cada consulta (duplica latencia, costo y dependencia externa).
- **Costo:** No detecta atribuciones cruzadas entre cifras reales que coexisten en el mismo fragmento ni omisiones sutiles de requisitos sanitarios (`H-04` y `H-05`, registradas en `LIM-03`).

## D-06 Reglas de sobreprecio deterministas separadas del flujo generativo

- **Estado:** vigente
- **Contexto:** El cálculo de desviación porcentual respecto a la mediana histórica 2026 y la activación de supervisión humana obligatoria sobre el 15% deben ser 100% exactos y auditables por Contraloría sin variabilidad estocástica.
- **Decisión:** Exponer `POST /precios/evaluar` y `GET /licitaciones/{licitacion_id}` respaldados por lógica aritmética determinista en `servicio/catalogo.py`, reservando el flujo generativo RAG exclusivamente para consultas documentales en `POST /consultas`.
- **Alternativas descartadas:** Delegar el cálculo de porcentajes y umbrales al LLM dentro de `/consultas` (riesgo de error aritmético y dificultad para garantizar el umbral configurable `UMBRAL_SOBREPRECIO_PCT`).
- **Costo:** Obliga a mantener actualizado el diccionario estructurado de `CATALOGO_2026` en sincronía con el documento Markdown del catálogo oficial cuando cambian los precios mensuales.
