<!-- AUTO:INICIO -->
# Registro de ejecución completa

| Campo | Valor |
|---|---|
| Fecha | 2026-11-24 11:19 |
| Commit del código | e81898e1cea3 (sin cambios) |
| Resumen escenarios | Escenarios: 14 de 14 cumplidos |
| Resumen pruebas | Pruebas automáticas: 82 pasan, 1 fallan |

## Componentes ejecutados

| Componente | Modo | Detalle |
|---|---|---|
| API FastAPI | real | `servicio/main.py` en `http://127.0.0.1:8000` |
| Interfaz Web | real | `interfaz/main.py` en `http://127.0.0.1:8080` |
| Corpus CENABAST | real | 5 documentos normativos en `data/` |
| Modelo | simulado | Adaptador dual (`servicio/respaldo.py`) |

## Detalle de escenarios

| ID | Escenario | Resultado |
|---|---|---|
| E-01 | control (api) | pasa |
| E-02 | control (interfaz) | pasa |
| E-03 | consulta normativa (api) | pasa |
| E-04 | consulta normativa (api) | pasa |
| E-05 | consulta normativa (api) | pasa |
| E-06 | consulta normativa (api) | pasa |
| E-07 | consulta normativa (interfaz) | pasa |
| E-08 | auditoria precios (api) | pasa |
| E-09 | auditoria precios (api) | pasa |
| E-10 | auditoria precios (interfaz) | pasa |
| E-11 | fuera de alcance (api) | pasa |
| E-12 | fuera de alcance (api) | pasa |
| E-13 | error esperado (api) | pasa |
| E-14 | error esperado (api) | pasa |
<!-- AUTO:FIN -->

## Qué se observó

Se ejecutaron los 14 escenarios end-to-end contra la API FastAPI (puerto 8000) y la Interfaz Web (puerto 8080), confirmando respuestas fundamentadas con citas documentales del catalogo CENABAST 2026, deteccion determinista de sobreprecio critico (+50%), contencion de prompt injection y errores uniformes 404/422.

## Qué no se probó

No se ejecuto consumo real contra el endpoint remoto de Google Gemini ni carga concurrente multi-usuario en contenedores productivos; la corrida se efectuo con el componente Modelo en modo simulado determinista para garantizar repetibilidad sin costo de API ni exposicion de credenciales.

## Siguiente paso

Completar la Matriz de Pruebas de la Unidad 3.5 con escenarios validos, invalidos y de borde, incorporar el detector determinista de alucinaciones en la capa de salida y validar las mitigaciones en la Matriz de Riesgos ejecutable.
