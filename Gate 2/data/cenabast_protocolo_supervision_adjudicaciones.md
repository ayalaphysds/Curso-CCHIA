# PROTOCOLO DE SUPERVISIÓN HUMANA Y GOBERNANZA DE IA EN ADJUDICACIONES CENABAST
**Comité de Ética, Probidad y Transformación Digital - CENABAST**
**Código de Gobernanza:** PROT-GOB-IA-CENABAST-2026

---

## 1. PRINCIPIO DE CONTROL HUMANO SIGNIFICATIVO (HUMAN-IN-THE-LOOP)
De conformidad con las directrices de la Contraloría General de la República y la Política Nacional de Inteligencia Artificial de Chile, ningún sistema algorítmico o de IA generativa operará con autonomía plena en decisiones que comprometan el erario fiscal, la probidad administrativa o el acceso de la población a medicamentos esenciales.

---

## 2. CLASIFICACIÓN DE OPERACIONES SEGÚN NIVEL DE RIESGO

### 2.1 Operaciones de Riesgo Bajo (Autonomía Algorítmica Permitida)
- **Consultas de catálogo de precios de referencia:** Lectura indexada de valores históricos.
- **Cálculo de desviaciones porcentuales:** Ejecución de operaciones aritméticas objetivas.
- **Búsqueda y extracción semántica de bases administrativas:** Resúmenes y citación de antecedentes.
*Acción del sistema:* Ejecución directa sin requerir confirmación humana.

### 2.2 Operaciones de Riesgo Medio (Autonomía con Registro de Trazabilidad)
- **Redacción de minutas técnicas de evaluación:** Elaboración de borradores de pre-adjudicación.
- **Recomendación de contraofertas en mesas de negociación (desvío 5% a 15%):**
*Acción del sistema:* Generación del dictamen y volcado a bitácora estructurada de auditoría.

### 2.3 Operaciones de Riesgo Alto (Supervisión Humana Obligatoria - Interrupción Crítica)
- **Adjudicación formal de órdenes de compra:** Compromiso presupuestario directo.
- **Aprobación de compras con sobreprecio crítico (> 15%):** Excepción presupuestaria.
- **Descalificación de proveedores o aplicación de multas por atraso:** Actos administrativos sancionatorios.
- **Autorización de compras directas de emergencia:** Excepción a la licitación pública.
*Acción del sistema:* **Interrupción inmediata de la ejecución mediante punto de control `interrupt()`**. El estado del flujo queda congelado en el checkpointer a la espera de un comando formal de aprobación o rechazo emitido por un funcionario habilitado (Jefe de Adquisiciones o Auditor Responsable).

---

## 3. ARQUITECTURA DE INTERRUPCIÓN Y REANUDACIÓN (LANGGRAPH)
Para garantizar el cumplimiento técnico del criterio no compensable de supervisión:
1. El grafo de decisión evalúa la condición de riesgo de la acción requerida.
2. Si detecta una acción clasificada como riesgo alto (ej. `adjudicar_orden_compra` o sobreprecio superior al 15%), emite un evento de interrupción:
   ```python
   interrupt({
       "alerta": "ADJUDICACION_ALTO_RIESGO",
       "medicamento": estado["medicamento"],
       "precio_ofertado": estado["precio_ofertado"],
       "desviacion_pct": estado["desviacion_pct"],
       "mensaje": "Requiere autorizacion formal de Jefatura de Adquisiciones para proceder."
   })
   ```
3. El motor de orquestación detiene el procesamiento y devuelve el control al supervisor humano.
4. Para continuar, el supervisor debe enviar un comando explícito y tipado:
   - `Command(resume=True)`: Autoriza la emisión de la orden de compra y reanuda el nodo de persistencia.
   - `Command(resume=False)`: Cancela la adjudicación, archiva el expediente en estado "RECHAZADO_POR_AUDITORIA" y activa alerta de integridad.
