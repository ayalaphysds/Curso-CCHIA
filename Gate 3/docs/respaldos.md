# Política y Registro de Componentes de Respaldo (Bloque 41)

## Pieza respaldada
- **Componente:** `Modelo` (`servicio/modelo.py` — adaptador `ModeloGemini` hacia Google Gemini API).
- **Respaldo declarado:** `ModeloSimulado` (`servicio/modelo.py`), activable únicamente de manera explícita mediante `MODELO=simulado` (entorno de pruebas/demo offline) o `MODELO=real` junto con `PERMITIR_RESPALDO=1`.

## Cómo se activa y cómo resulta visible
- Si `MODELO=real` y `GEMINI_API_KEY` está ausente:
  - Con `PERMITIR_RESPALDO=0` (valor por defecto): el servicio **falla honestamente** con HTTP `503` y código `modelo_no_disponible`.
  - Con `PERMITIR_RESPALDO=1`: el servicio degrada explícitamente a `ModeloSimulado`, expone `"modelo_activo": "respaldo"` y `"respaldo_activo": true` en `GET /salud`, e incluye `"modo_modelo": "respaldo"` más `"advertencia_respaldo"` en cada respuesta de `POST /consultas`.

## Condición de retiro del respaldo
- Inyección de una credencial institucional válida (`GEMINI_API_KEY`) mediante variable de entorno en tiempo de ejecución con cuotas habilitadas para el ambiente productivo de CENABAST, manteniendo `PERMITIR_RESPALDO=0`.
