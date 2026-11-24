# Revisión del alcance

Revisor: Sebastián Eduardo Ayala Vásquez (autorrevisión técnica diferida con pauta oficial de 6 criterios)
Fecha: 2026-11-24

- Hallazgo 1 (criterio 2): El requerimiento inicial de evaluación de ofertas (RF-02) no especificaba el formato de entrada ni las 4 categorías exactas de desvío porcentual según las bases BAS-CENABAST-2026-MED.
  Decisión: aceptado. Cambio: se precisó en RF-02 el identificador `codigo_onu`, el precio en CLP, las 4 categorías (`COMPETITIVO`, `NEGOCIACION`, `SOBREPRECIO_CRITICO`, `TEMERARIO`) y el umbral de supervisión humana (> 15%).

- Hallazgo 2 (criterio 4): Faltaba un criterio de aceptación negativo verificable para consultas fuera del corpus CENABAST que garantizara ausencia de alucinaciones cuando no existe respaldo documental.
  Decisión: aceptado. Cambio: se incorporó CA-02 exigiendo respuesta explícita `"No encuentro esa informacion"` y lista `fuentes` vacía ante consultas ajenas al dominio.

- Hallazgo 3 (criterio 5): Se evaluó incluir la integración directa con el portal Mercado Público (RF-05) dentro del alcance del MVP para el Gate 3.
  Decisión: rechazado. Motivo: excede las 20 horas netas del plan por hitos y depende de credenciales institucionales y firma digital avanzada de ChileCompra no disponibles en el programa; permanece documentado como deseable y fuera del alcance del MVP.

- Hallazgo 4 (criterio 6): Se detectó un posible riesgo de acoplamiento entre el servicio RAG y la interfaz de consulta si ambos compartían el mismo proceso HTTP.
  Decisión: aplazado. Se resuelve en el Hito H3 separando `API FastAPI` (puerto 8000) e `Interfaz Web` (puerto 8080) en dos contenedores independientes dentro de `compose.yaml`.
