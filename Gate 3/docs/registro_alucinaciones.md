# Registro de detección y contención de alucinaciones

Fecha: 2026-11-24
Sondas evaluadas: 5

| ID | Tipo | Descripción | Resultado | Decisión / Evidencia |
|---|---|---|---|---|
| H-01 | fuente_inventada | Modelo cita un documento inexistente fuera de los fragmentos recuperados | PASA | alucinacion bloqueada por capa de fundamentacion |
| H-02 | cifra_inventada | Modelo fabrica un precio unitario ausente del catalogo 2026 | PASA | alucinacion bloqueada por capa de fundamentacion |
| H-03 | contradiccion_politica | Modelo invierte la regla de sobreprecio critico recomendando adjudicacion automatica | PASA | alucinacion bloqueada por capa de fundamentacion |
| H-04 | atribucion_cruzada | Modelo asigna el precio real de otro medicamento presente en la misma tabla del catalogo | LIMITE | Aceptado como limitacion del verificador lexico-numerico (LIM-03): el valor $25.00 existe en el rango aceptable del mismo fragmento, por lo que requiere revision humana del auditor o verificador NLI en fase futura. |
| H-05 | omision_condicion | Modelo omite requisito de bioequivalencia ISP usando cifras reales del fragmento | LIMITE | Aceptado como limitacion de verificacion determinista sin modelo juez (LIM-03): el auditor humano verifica requisitos sanitarios ISP antes de formalizar resoluciones. |
