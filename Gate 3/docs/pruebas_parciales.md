# Plan de pruebas parciales

| Componente | Entrada | Salida | Doble | Archivo | Defecto introducido | Detectado |
|---|---|---|---|---|---|---|
| recuperar | pregunta en espanol y limite k | lista ordenada de Fragmento con fuente oficial | ninguno (corpus local en disco) | tests/parciales/test_recuperar.py | subir UMBRAL_MINIMO a 99.0 para devolver lista vacia | sí |
| construir_prompt | pregunta y fragmentos validos | cadena de prompt versionado con contexto | Fragmento sintetico en memoria | tests/parciales/test_prompt.py | omitir el nombre de fuente en el contexto armado | sí |
| generar (modelo) | prompt y fragmentos CENABAST | respuesta fundamentada con cita [fuente: ...] | Fragmento sintetico de Paracetamol | tests/parciales/test_modelo.py | remover el marcador [fuente: ...] de ModeloSimulado | sí |
| empaquetar | respuesta, fuentes, trace_id, modo | diccionario normalizado sin fuentes duplicadas | datos sinteticos de contrato | tests/parciales/test_empaquetar.py | eliminar deduplicacion de fuentes en empaquetar_respuesta | sí |
| configuracion | variables de entorno via monkeypatch | valores de entorno, modo modelo y clave diferida | monkeypatch de pytest | tests/parciales/test_config.py | cambiar default de ENTORNO a cadena vacia | sí |
| catalogo de precios y licitaciones | codigo ONU + precio CLP / ID LIC-NNN | categoria, desviacion porcentual y dictamen | monkeypatch para UMBRAL_SOBREPRECIO_PCT | tests/parciales/test_catalogo.py | invertir comparacion del umbral critico (>15%) | sí |
