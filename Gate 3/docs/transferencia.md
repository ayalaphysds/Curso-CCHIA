# Registro de Prueba Cruzada de Transferencia

**Meta operativa:** poner en marcha y probar la solución usando únicamente `README.md` y `docs/api.md` en `<= 15.0` minutos.

## Sesiones registradas

| Ronda | Tiempo (min) | Resultado | Observador |
|---:|---:|---|---|
| 1 | 18.5 | Éxito con fricciones de documentación | Par técnico (simulación en frío) |
| 2 | 9.2 | Éxito bajo meta operativa (`<= 15 min`) | Par técnico (tras ajustes en `README.md` y `docs/api.md`) |

## Observaciones clasificadas

| ID | Ronda | Síntoma observado | Causa | Referencia / Acción | Estado |
|---|---:|---|---|---|---|
| T-01 | 1 | Faltaba `pytest` al instalar solo `requirements.txt` | documento | Se documentó `requirements-dev.txt` en `README.md` | resuelta |
| T-02 | 1 | Comando para comprobar vigencia de `docs/api.md` no era visible | documento | Se agregó `python generar_api_md.py --comprobar` a `README.md` | resuelta |
| T-03 | 1 | Formato exacto de `codigo_onu` en `POST /precios/evaluar` requería abrir `/docs` | documento | Se agregó ejemplo ejecutable `API-04` (`51181504`) a `docs/api.md` | resuelta |
| T-04 | 2 | Instalación, pruebas y consulta completadas en 9.2 min sin asistencia | ninguna | Meta de transferencia (`<= 15 min`) cumplida | resuelta |
| T-05 | 2 | Consulta en inglés devolvió abstención sin fuentes | producto | Declarada en `LIM-02` (`docs/limitaciones.md`) y riesgo `R-09` | declarada |
| T-06 | 2 | Sinónimo coloquial (*"remedio para bajar la fiebre"*) devolvió abstención | producto | Declarada en `LIM-02` y fijada por prueba de regresión en `test_recuperar.py` | declarada |
