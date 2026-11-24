# Registro de pruebas de la API

Fecha: 2026-11-24
Servicio probado: http://127.0.0.1:8000 (cliente: httpx)
Resultado: 12 de 12 casos cumplidos

| Caso | Descripción | Petición | Esperado | Obtenido | Resultado |
|---|---|---|---|---|---|
| V-01 | Healthcheck operativo sin exposicion de claves | GET /salud | 200 | 200 | PASA |
| V-02 | Consulta RAG de precio de referencia Paracetamol (CA-01) | POST /consultas {"pregunta": "Cual es el precio de referencia del Paracetamol 500 mg?"} | 200 | 200 | PASA |
| V-03 | Consulta fuera del corpus CENABAST sin fuentes (CA-02) | POST /consultas {"pregunta": "Cual es la temperatura en Marte hoy?"} | 200 | 200 | PASA |
| V-04 | Auditoria de sobreprecio critico Paracetamol +50% (CA-03) | POST /precios/evaluar {"codigo_onu": "51181504", "precio_ofertado": 33.6} | 200 | 200 | PASA |
| V-05 | Consulta de expediente historico LIC-723 (CA-04) | GET /licitaciones/LIC-723 | 200 | 200 | PASA |
| I-01 | Pregunta vacia o solo espacios rechazada con 422 | POST /consultas {"pregunta": "   "} | 422 | 422 | PASA |
| I-02 | Cuerpo JSON malformado rechazado con 422 uniforme | POST /consultas `{pregunta: sin comillas` | 422 | 422 | PASA |
| I-03 | Precio ofertado negativo rechazado con 422 | POST /precios/evaluar {"codigo_onu": "51181504", "precio_ofertado": -10.0} | 422 | 422 | PASA |
| I-04 | Formato invalido de identificador de licitacion (422) | GET /licitaciones/INVALIDO-1 | 422 | 422 | PASA |
| I-05 | Licitacion inexistente con formato valido retorna 404 uniforme (CA-04) | GET /licitaciones/LIC-999 | 404 | 404 | PASA |
| I-06 | Medicamento inexistente en catalogo 2026 retorna 404 uniforme | POST /precios/evaluar {"codigo_onu": "51999999", "precio_ofertado": 100.0} | 404 | 404 | PASA |
| I-07 | Metodo HTTP no permitido sobre /consultas retorna 405 uniforme | DELETE /consultas | 405 | 405 | PASA |
