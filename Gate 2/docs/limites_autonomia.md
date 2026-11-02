# POLÍTICA DE LÍMITES DE AUTONOMÍA Y SUPERVISIÓN HUMANA DE AGENTES IA EN CENABAST
**Módulo 2: Construcción de Componentes IA · U2.4 · Bloque 23**  
**Especialización en IA Accenture - Curso CCHIA**  
**Institución:** Central de Abastecimiento del Sistema Nacional de Servicios de Salud (CENABAST)  
**Entregable:** Documento de Límites de Autonomía de Agentes

---

## 1. PRINCIPIO GENERAL DE CONTROL HUMANO SIGNIFICATIVO
En cumplimiento de la Ley N° 19.886 de Bases sobre Contratos Administrativos y las directrices de probidad y transparencia del Estado de Chile, los agentes basados en modelos generativos de IA operan bajo el principio de **Control Humano Significativo (Human-in-the-Loop)**.

Bajo ninguna circunstancia un agente autónomo está facultado para comprometer fondos fiscales, autorizar excepciones presupuestarias o adjudicar órdenes de compra sin la intervención explícita y auditable de un funcionario competente.

---

## 2. TAXONOMÍA Y CLASIFICACIÓN DE HERRAMIENTAS POR NIVEL DE RIESGO

| Nivel de Riesgo | Herramienta | Tipo de Operación | Nivel de Autonomía Permitido | Justificación y Medidas de Control |
|---|---|---|---|---|
| **BAJO** | `consultar_catalogo_cenabast` | Lectura indexada | **Autonomía Total** | Operación de sólo lectura sin impacto presupuestario. Consulta bases oficiales de referencia 2026. |
| **BAJO** | `calcular_sobreprecio_oferta` | Aritmética determinista | **Autonomía Total** | Cálculo matemático de desvío respecto a la línea base. No genera actos administrativos vinculantes. |
| **MEDIO** | `generar_borrador_dictamen` | Síntesis documental | **Autonomía Asistida** | Elabora minutas de recomendación técnica. Requiere revisión previa antes de difusión a la comisión evaluadora. |
| **ALTO** | `adjudicar_orden_compra` | Transaccional financiera | **PROHIBIDA AUTONOMÍA** | Compromiso patrimonial directo del Estado. Exige punto de interrupción obligatorio (`esperar_aprobacion`) y firma del Jefe de Adquisiciones. |
| **ALTO** | `descalificar_oferente` | Jurídico-sancionatoria | **PROHIBIDA AUTONOMÍA** | Afecta derechos de oferentes y genera responsabilidad administrativa. Exige resolución jurídica fundada. |

---

## 3. PROTOCOLO DE INTERVENCIÓN Y PUNTOS DE PAUSA (CHECKPOINTS)
Para las herramientas clasificadas como de **Riesgo Alto**:
1. **Detección del Disparador:** El agente identifica la necesidad de emitir una orden de compra o cuando la oferta analizada supera el 15.0% de sobreprecio sobre la mediana histórica.
2. **Pausa Obligatoria:** La ejecución se detiene automáticamente invocando la función `esperar_aprobacion(accion)`.
3. **Presentación de Evidencia:** Se expone al funcionario responsable:
   - Identificador de la licitación en Mercado Público (ej. `723-14-LP24`).
   - Principio activo, forma farmacéutica y cantidad programada.
   - Proveedor evaluado y monto total comprometido en CLP.
   - Desviación porcentual calculada y justificación técnica.
4. **Reanudación Controlada:**
   - Si el auditor humano autoriza: La orden de compra se emite registrando la identidad del supervisor y la huella temporal.
   - Si el auditor rechaza: El expediente se archiva en estado "DETENIDO_POR_SUPERVISION" y no se genera afectación patrimonial.

---

## 4. REGISTRO Y AUDITORÍA ESTRUCTURADA
Todas las decisiones del agente, tanto autónomas como supervisadas, quedan registradas en el archivo inmutable `Gate 2/trazas_agente.jsonl`, conteniendo:
- Marca temporal UTC (`timestamp`).
- Nombre de la herramienta y nivel de riesgo asignado.
- Parámetros de entrada de la consulta.
- Indicador booleano `supervision_humana_requerida` y `aprobado_por_humano`.
- Resultado de la ejecución o motivo de bloqueo.

Este esquema garantiza que cualquier auditoría de la Contraloría General de la República pueda reconstruir la cadena causal de cada adjudicación pública.
