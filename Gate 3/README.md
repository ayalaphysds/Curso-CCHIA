# Gate 3 / Capstone — Plataforma End-to-End de Auditoría de Precios CENABAST

Aplicación generativa end-to-end para pre-auditoría de precios, consultas normativas con citas verificadas y control de riesgos en licitaciones públicas de **CENABAST** (Chile). Expone los endpoints `GET /salud`, `POST /consultas`, `POST /precios/evaluar` y `GET /licitaciones/{licitacion_id}` mediante FastAPI, empaquetados junto a una interfaz web desacoplada con Docker Compose.

---

## Requisitos

- **Python 3.12** (coincidente con la imagen base `python:3.12-slim` de `Dockerfile`).
- Git para trazabilidad y prueba en frío (`probar_en_frio.py`).
- Docker Desktop / Docker Engine con `docker compose` *(necesario únicamente para ejecutar la pila en contenedores y `verificar_gate3.py --con-docker`)*.

---

## Instalación

Crea un entorno virtual limpio e instala las dependencias de desarrollo y pruebas desde la carpeta raíz de Gate 3:

```bash
python -m venv .venv
pip install -r requirements-dev.txt
```

Para instalar solo las dependencias mínimas de ejecución del servicio API sin herramientas de test, usa `requirements.txt`.

---

## Configuración

Copia la plantilla `.env.example` a `.env` antes de ejecutar en local (`.env` está excluido en `.gitignore` y `.dockerignore`):

```bash
cp .env.example .env
```

| Variable | Tipo | Descripción | Valor por defecto |
|---|---|---|---|
| `GEMINI_API_KEY` | (secreto) | Clave de API de Google Gemini; requerida solo si `MODELO=real` y sin respaldo. | *(vacío)* |
| `ENTORNO` | (configuración) | Etiqueta del ambiente de ejecución (`desarrollo`, `pruebas` o `produccion`). | `desarrollo` |
| `MODELO` | (configuración) | Motor generativo activo: `simulado` (determinista offline) o `real` (Gemini API). | `simulado` |
| `PERMITIR_RESPALDO` | (configuración) | Si vale `1` y falta `GEMINI_API_KEY` con `MODELO=real`, activa respaldo declarado. | `0` |
| `UMBRAL_SOBREPRECIO_PCT` | (configuración) | Porcentaje de desvío sobre el cual se exige supervisión humana obligatoria. | `15.0` |

---

## Cómo arrancar

### Opción 1: Arranque local de la API (sin Docker)

```bash
python -m uvicorn servicio.main:app --host 127.0.0.1 --port 8000
```

Para levantar la interfaz web en paralelo en otra terminal:

```bash
python -m uvicorn main:app --app-dir interfaz --host 127.0.0.1 --port 8080
```

### Opción 2: Arranque de la pila completa con Docker Compose

```bash
docker compose up -d --build --wait --wait-timeout 120
```

---

## Cómo comprobar que funciona

1. **Salud de ambos servicios:**
   - API FastAPI: `http://127.0.0.1:8000/salud` y documentación interactiva en `http://127.0.0.1:8000/docs`.
   - Interfaz Web: `http://127.0.0.1:8080/salud` y gateway en `http://127.0.0.1:8080/preguntar?texto=precio+Paracetamol`.
2. **Consulta normativa y casos HTTP externos:**
   - Ejecuta `python cliente_externo.py` y revisa los ejemplos reproducibles en `docs/api.md` (verificados con `python generar_api_md.py --comprobar`).
   - Revisa el reporte de registro de pruebas HTTP en `docs/registro_pruebas.md` y la evidencia de ejecución completa en `docs/registro_ejecucion.md`.

---

## Cómo detener

- Si arrancaste en local con `uvicorn`, presiona `Ctrl+C` en cada terminal.
- Si arrancaste con Docker Compose, detén y elimina los contenedores con:

```bash
docker compose down
```

---

## Pruebas

Suite automatizada completa (API, componentes aislados, seguridad, matriz, documentación, guion, ensayo y rúbrica):

```bash
python -m pytest -q
```

Verificadores especializados del proyecto:

```bash
python verificar_ficha_completa.py
python verificar_servicio.py
python verificar_dockerfile.py
python verificar_entrega.py
python verificar_parciales.py
python verificar_matriz.py
python verificar_mitigaciones.py
python verificar_riesgos.py
python verificar_readme.py
python verificar_decisiones.py
python verificar_transferencia.py
python medir_guion.py
python ensayo_demo.py
python ensayo_demo.py --comprobar
python verificar_gate3.py
```

Para ejecutar la evaluación completa incluyendo las 3 comprobaciones de contenedores Docker y actualizar el informe oficial en `docs/gate3.md`:

```bash
python verificar_gate3.py --con-docker --escribir
```

---

## Decisiones técnicas

Las 6 decisiones vigentes están documentadas con contexto, alternativas descartadas y costos en `docs/decisiones.md`:

- **D-01:** Recuperador híbrido léxico determinista sobre el corpus Markdown CENABAST.
- **D-02:** Falla honesta HTTP `503` (`modelo_no_disponible`) cuando falta `GEMINI_API_KEY` con `MODELO=real`.
- **D-03:** Contrato uniforme de errores HTTP (`ErrorRespuesta`) sin exposición de trazas ni secretos.
- **D-04:** Separación en dos contenedores Docker (`api` e `interfaz`) orquestados con `compose.yaml`.
- **D-05:** Capa determinista de verificación de fundamentación contra alucinaciones en salida.
- **D-06:** Cálculo determinista de sobreprecio y precedentes separado del motor generativo RAG.

---

## Limitaciones conocidas

Las 3 limitaciones descubiertas y verificadas mediante pruebas y transferencia se detallan en `docs/limitaciones.md` y se enlazan con `docs/matriz_riesgos.md`:

- **LIM-01** (`R-02`): Escenarios hipotéticos sin patrones explícitos de override superan el filtro regex de entrada (`ataques:A-07`).
- **LIM-02** (`R-09`): Consultas en inglés o con sinónimos coloquiales ausentes del glosario CENABAST devuelven abstención segura (`matriz_modelo:MP-08`, `transferencia:T-05`, `transferencia:T-06`).
- **LIM-03** (`R-01`): Atribuciones cruzadas entre cifras reales del mismo fragmento y omisiones sanitarias sutiles requieren revisión humana (`alucinaciones:H-04`, `alucinaciones:H-05`).

---

## Estructura del repositorio

- `servicio/main.py`, `servicio/logica.py`, `servicio/esquemas.py`, `servicio/errores.py`, `servicio/config.py`, `servicio/contratos.py`: API FastAPI en 3 capas y contratos.
- `servicio/cadena.py`, `servicio/recuperador.py`, `servicio/prompt.py`, `servicio/modelo.py`, `servicio/respaldo.py`, `servicio/seguridad.py`, `servicio/fundamentacion.py`, `servicio/catalogo.py`: Pipeline RAG de 4 capas, seguridad, fundamentación y catálogo 2026.
- `interfaz/main.py`, `interfaz/Dockerfile`, `interfaz/requirements.txt`: Servicio web desacoplado.
- `Dockerfile`, `compose.yaml`, `requirements.txt`, `requirements-dev.txt`, `.env.example`, `.dockerignore`: Empaquetado y composición.
- `data/cenabast_catalogo_precios_referencia_2026.md`: Corpus documental oficial CENABAST (5 archivos Markdown).
- `docs/ficha_diseno_funcional.md`, `docs/diagrama_arquitectura.png`, `docs/revision_alcance.md`: Diseño funcional (U3.1).
- `docs/registro_pruebas.md`, `docs/verificacion_cruzada.md`, `docs/pruebas_parciales.md`, `docs/bitacora_ajustes.md`, `docs/registro_ejecucion.md`, `docs/respaldos.md`: Evidencias de API, despliegue e integración (U3.2–U3.4).
- `docs/matriz_pruebas.md`, `docs/registro_alucinaciones.md`, `docs/matriz_riesgos.md`: QA, seguridad y riesgos (U3.5).
- `docs/diario_de_friccion.md`, `docs/api.md`, `docs/transferencia.md`, `docs/decisiones.md`, `docs/limitaciones.md`: Documentación y transferencia (U3.6).
- `docs/defensa.md`, `docs/demo_respaldo.md`, `docs/gate3.md`: Defensa técnica, plan B y reporte Gate 3 (U3.7).
- `ensayo_demo.py`, `medir_guion.py`, `rubrica_gate3.py`, `verificar_gate3.py`: Automatización de ensayo y verificación integral del Capstone.
- `tests/test_api.py` y `tests/parciales/test_gate3.py`: Suites de pruebas unitarias, parciales y de contrato.

---

## Problemas frecuentes

- **Error `503 modelo_no_disponible` al consultar `/consultas`:** Ocurre cuando `MODELO=real` está activo sin `GEMINI_API_KEY` y con `PERMITIR_RESPALDO=0`. Solución: usa `MODELO=simulado`, inyecta una clave válida en `.env` o habilita explícitamente `PERMITIR_RESPALDO=1`.
- **Puerto `8000` o `8080` ocupado al correr `ensayo_demo.py` o `probar_en_frio.py`:** Detén instancias previas de `uvicorn` o ejecuta `docker compose down` antes de lanzar los verificadores.
- **Error `No module named pytest`:** Ejecuta `pip install -r requirements-dev.txt` con el entorno virtual `.venv` activado.
- **Falta Docker en la máquina local:** Ejecuta `python verificar_gate3.py` para correr las 19 comprobaciones locales (modo `PROVISIONAL`); la certificación completa (`APRUEBA`) requiere un entorno con Docker para `--con-docker`.
