# ANÁLISIS DE LÍMITES DE MÉTRICAS LÉXICAS EN AUDITORÍA DE PRECIOS CENABAST
**Módulo 2: Construcción de Componentes IA · U2.2 · Bloque 17**  
**Especialización en IA Accenture - Curso CCHIA**  
**Caso de Estudio:** Central de Abastecimiento del Sistema Nacional de Servicios de Salud (CENABAST)  
**Autor:** Equipo de Auditoría Algorítmica y Control de Gestión

---

## 1. QUÉ MIDE LA MÉTRICA LÉXICA
El cálculo de similitud léxica basado en *Precision*, *Recall* (Cobertura) y *F1-Score* a nivel de n-gramas o bolsa de palabras (*bag of words* unigrama con `collections.Counter`):
- **Precisión Léxica:** Mide qué proporción de los tokens emitidos por el modelo generativo están presentes en la respuesta de referencia humana (*ground truth*). Penaliza la verbosidad irrelevante y la inclusión de términos fuera de contexto.
- **Cobertura Léxica (Recall):** Mide qué proporción de las palabras clave de la referencia fueron efectivamente recuperadas y mencionadas por el modelo. Penaliza la omisión de datos indispensables.
- **F1-Score Léxico:** Es la media armónica entre precisión y cobertura. Otorga una puntuación balanceada de coincidencia textual superficial en el intervalo $[0.0, 1.0]$.

En el contexto de compras públicas hospitalarias de CENABAST, esta métrica resulta útil como filtro sintáctico preliminar rápido y de costo computacional nulo ($O(N)$ en memoria sin llamadas a APIs) para validar si el modelo está incorporando el vocabulario técnico requerido: nombres de principios activos (Paracetamol, Ceftriaxona, Losartán), unidades de medida (comprimidos, frascos ampolla), normas legales (Ley 19.886) y organismos reguladores (ISP).

---

## 2. MODOS DE FALLA OBSERVADOS EN AUDITORÍA DE PRECIOS
La auditoría manual detallada de los 20 casos de precios de CENABAST (documentada en `resultados_metricas.json` y `revision_manual.json`) evidenció limitaciones estructurales severas de las métricas léxicas puras frente a la semántica y veracidad factual en adquisiciones públicas:

### A. Falsos Positivos por F1 Alto con Inversión Factual Crítica
Una respuesta puede reproducir casi todas las palabras de la referencia pero invertir un valor numérico o un operador lógico:
- *Ejemplo:* Referencia: *"Corresponde rechazar la oferta por sobreprecio de 50.0% respecto a 22.40 CLP."*
- *Alucinación simulada:* *"Corresponde adjudicar la oferta por sobreprecio de 50.0% respecto a 22.40 CLP."*
- *Comportamiento de la métrica:* Al compartir 10 de 11 tokens, el F1 resultante es de **0.909**, sugiriendo una respuesta "casi perfecta", cuando en realidad constituye un error catastrófico que adjudicaría una compra ilegal con sobreprecio fiscal.

### B. Falsos Negativos por Sinónimos y Paráfrasis Válidas
El lenguaje jurídico-administrativo chileno cuenta con múltiples expresiones equivalentes:
- Intercambio de términos: *"pesos chilenos"* vs *"CLP"*, *"fármaco"* vs *"principio activo"*, *"retraso"* vs *"atraso"*, *"suspender"* vs *"pausar"*.
- *Comportamiento de la métrica:* Respuestas factualmente impecables y exhaustivas obtuvieron un F1 moderado (en torno a 0.50 - 0.65) únicamente por emplear giros sintácticos distintos a la referencia textual predefinida.

### C. Insensibilidad al Orden y Sintaxis Financiera
La métrica no distingue relaciones sintácticas de atribución numérica. Por ejemplo, en ofertas multidosis o comparaciones de dos oferentes, intercambiar qué laboratorio cotizó qué precio preserva el 100% de los tokens pero altera completamente la adjudicación.

---

## 3. MUESTRA ANALIZADA
Se procesó una muestra de 20 casos representativos del dominio CENABAST que abarcan los siguientes ejes operativos:
1. **Precios de Catálogo y Línea Base 2026:** Paracetamol 500 mg ($22.40 CLP), Ceftriaxona 1 g ($1.250 CLP), Losartán 50 mg ($18.50 CLP), Insulina NPH ($3.800 CLP) y Amoxicilina 500 mg ($45.00 CLP).
2. **Evaluación de Desviaciones y Dictámenes:** Rango competitivo (<= 5%), mesa de negociación obligatoria (5% a 15%), sobreprecio crítico (> 15%) y ofertas temerarias (-44.4%).
3. **Normas de Continuidad y Logística:** Multas por atraso (1% diario, tope 15%), umbral de rescisión contractual (15 días), nivel de cumplimiento logístico (INCL >= 85%), pérdida de cadena de frío y cuotas anti-monopolio (máximo 45%).
4. **Gobernanza y Supervisión de IA:** Restricciones de autonomía en compras públicas y justificación de compras directas bajo la Ley N° 19.886.

**Estadísticas de la Muestra (Fuente: `resultados_metricas.json`):**
- Total de casos evaluados: **20**
- Casos con auditoría manual cualitativa: **10**
- Precisión léxica promedio: **0.5041 (50.4%)**
- Cobertura léxica promedio: **0.5823 (58.2%)**
- F1-Score léxico promedio: **0.5378 (53.8%)**
- Tasa de corrección factual en muestra auditada: **100% (10/10)**
- Tasa de completitud en muestra auditada: **100% (10/10)**
- Tasa de contradicción en muestra auditada: **0% (0/10)**

---

## 4. RECOMENDACIONES OPERATIVAS PARA CENABAST
1. **Prohibición de Decisión Basada Únicamente en F1:** Las métricas léxicas no deben utilizarse como compuerta única para aprobar o validar dictámenes de auditoría farmacéutica.
2. **Implementación de RAG Semántico con Citas Obligatorias:** Para resolver el problema de la variabilidad de precios y la alucinación de valores, el sistema debe anclarse en un vector store con recuperación de fragmentos oficiales y citación explícita del documento fuente (`[cenabast_catalogo_precios_referencia_2026.md]`).
3. **Validación Determinista de Schemas JSON:** Para datos financieros críticos (porcentajes de desviación, precios unitarios y dictámenes de adjudicación), el modelo debe emitir esquemas estructurados validados por Pydantic antes de ser presentados al auditor.
4. **Supervisión Humana Obligatoria (Human-in-the-Loop):** Toda recomendación que involucre sobreprecios superiores al 15% o descalificación de proveedores debe pausar el flujo algorítmico y requerir la firma o autorización de un funcionario responsable de CENABAST.
