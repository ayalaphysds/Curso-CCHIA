# Matriz de Pruebas

Fecha: 2026-11-24
Huella de la matriz: f047d4b07c49
Escenarios: 6 de 6 cumplidos

| ID | Tipo | Escenario | Peticion | Esperado | Cubre | Resultado | Hallazgo |
|---|---|---|---|---|---|---|---|
| MP-01 | valido | Consulta normativa de precio de referencia Paracetamol 500 mg con cita | POST /consultas | HTTP 200 | RF-01, CA-01, RNF-01 | PASA | Ninguno |
| MP-02 | valido | Evaluacion de sobreprecio critico (+50%) activa bandera de supervision humana | POST /precios/evaluar | HTTP 200 | RF-02, CA-03 | PASA | Ninguno |
| MP-03 | valido | Consulta de expediente historico LIC-723 y contrato de salud para interfaz | GET /licitaciones/LIC-723 | HTTP 200 | RF-03, RF-04, CA-04, CA-05 | PASA | Ninguno |
| MP-04 | invalido | Pregunta solo con espacios rechazada con 422 y codigo uniforme entrada_invalida | POST /consultas | HTTP 422 | RNF-02, CA-07 | PASA | Ninguno |
| MP-05 | invalido | Expediente con formato valido inexistente devuelve 404 uniforme | GET /licitaciones/LIC-999 | HTTP 404 | RF-03, RNF-02, CA-04 | PASA | Ninguno |
| MP-06 | borde | Consulta fuera del corpus CENABAST se abstiene honestamente sin fuentes | POST /consultas | HTTP 200 | RF-01, CA-02, RNF-03 | PASA | Ninguno |
