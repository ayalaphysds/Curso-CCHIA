# Informe de Verificación — Gate 3 / Capstone

- **Fecha:** 2026-11-24T11:40:55
- **Modo:** sin Docker
- **Huella de la evidencia:** `052fa74f0248`
- **Puntaje:** `100.00 / 100`
- **Nota:** `7.00` (escala 1.0 a 7.0, exigencia 60%)
- **Resultado:** **PROVISIONAL** (faltan las comprobaciones con Docker: stack, ejecucion, registro)

## Criterios

| ID | Dimensión | Peso | Puntos | Cobertura |
|---|---|---:|---:|---|
| C1 | Problema, requerimientos y arquitectura | 10 | 10.00 | 2/2 fuentes |
| C2 | Funcionamiento end-to-end | 25 | 25.00 | 2/4 fuentes |
| C3 | Integracion IA, orquestacion y RAG | 15 | 15.00 | 2/2 fuentes |
| C4 | Backend FastAPI y Docker | 15 | 15.00 | 4/4 fuentes |
| C5 | QA, pruebas y evaluacion de calidad | 10 | 10.00 | 3/3 fuentes |
| C6 | Seguridad, riesgos y trazabilidad | 10 | 10.00 | 2/3 fuentes |
| C7 | Documentacion tecnica | 5 | 5.00 | 2/2 fuentes |
| C8 | Demo y defensa tecnica | 10 | 10.00 | 3/3 fuentes |

## No compensables

| ID | Criterio | Estado automatizado |
|---|---|---|
| NC-1 | La solucion se ejecuta de punta a punta en el entorno contenerizado | PASA |
| NC-2 | El servicio expone endpoints funcionales y validados | PASA |
| NC-3 | La demo se ejecuta en vivo sobre la solucion construida, no sobre material grabado | Confirmación manual del evaluador |
| NC-4 | Sin credenciales ni datos reales en el repositorio ni en el corpus | PASA |

## Lo que confirma el evaluador

- **NC-3:** Que la demostracion corra en vivo, en la defensa.
- **NC-4:** Que los datos del corpus sean simulados.

## Entregables

- **Codigo y contenedor:** `Dockerfile`, `compose.yaml`, `servicio/main.py`
- **README tecnico:** `README.md`
- **Matrices de prueba y riesgo:** `docs/matriz_pruebas.md`, `docs/matriz_riesgos.md`
- **Demo en vivo:** `ensayo_demo.py`, `docs/demo_respaldo.md`
- **Presentacion ejecutiva:** `docs/defensa.md`

## Fuentes ejecutadas

| Fuente | Resultado | Cumplidas | Detalle |
|---|---|---:|---|
| `ficha` | PASA | 5/5 | ok |
| `decisiones` | PASA | 7/7 | ok |
| `frio` | PASA | 5/5 | ok |
| `demo` | PASA | 8/8 | ok |
| `respaldo` | PASA | 8/8 | ok |
| `mitigaciones` | PASA | 17/17 | ok |
| `ia` | PASA | 20/20 | ok |
| `servicio` | PASA | 6/6 | ok |
| `api_md` | PASA | 6/6 | ok |
| `dockerfile` | PASA | 7/7 | ok |
| `compose` | PASA | 7/7 | ok |
| `pytest` | PASA | 83/83 | ok |
| `matriz` | PASA | 6/6 | ok |
| `parciales` | PASA | 5/5 | ok |
| `riesgos` | PASA | 6/6 | ok |
| `secretos` | PASA | 4/4 | ok |
| `readme` | PASA | 8/8 | ok |
| `transferencia` | PASA | 5/5 | ok |
| `guion` | PASA | 9/9 | ok |
| `stack` | OMITIDA | 0/0 | Requiere `--con-docker` |
| `ejecucion` | OMITIDA | 0/0 | Requiere `--con-docker` |
| `registro` | OMITIDA | 0/0 | Requiere `--con-docker` |

## Lo que este informe no demuestra

- No verifica la ejecucion en vivo de la demo frente al jurado (confirmado manualmente por el evaluador en NC-3).
- No garantiza que las diapositivas visuales de la presentacion ejecutiva esten construidas aparte de docs/defensa.md.
- En modo sin Docker omite las 3 comprobaciones de contenedores (stack, ejecucion, registro) y emite veredicto PROVISIONAL.
- No prueba la calidad semantica de un modelo LLM externo con cuota activa (usa el modo determinista configurado).
- No reemplaza la revision humana de probidad y pertinencia clinica sobre las bases administrativas de CENABAST.
