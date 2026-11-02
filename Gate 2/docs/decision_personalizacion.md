# REGISTRO DE DECISIÓN DE ARQUITECTURA (ADR 002): ESTRATEGIA DE PERSONALIZACIÓN PARA AUDITORÍA CENABAST
**Módulo 2: Construcción de Componentes IA · U2.6 · Bloque 30**  
**Especialización en IA Accenture - Curso CCHIA**  
**Estado:** APROBADO Y ADOPTADO  
**Fecha:** Noviembre 2026  
**Decisores:** Arquitecto de Soluciones IA, Auditor Líder de Adquisiciones CENABAST  

---

## 1. CONTEXTO Y PROBLEMA DE DECISIÓN
La Central de Abastecimiento del Sistema Nacional de Servicios de Salud (CENABAST) requiere implementar un componente inteligente para la auditoría continua de procesos de licitación pública, compras coordinadas y convenios marco de medicamentos esenciales (ej. Paracetamol, Ceftriaxona, Losartán, Amoxicilina, Insulina NPH).

El sistema debe resolver los siguientes desafíos críticos de negocio:
1. **Alta Volatilidad y Dinamismo de Precios:** Los precios de referencia de catálogo, valores de importación y condiciones de mercado varían mensual o trimestralmente conforme al IPC de la salud y aranceles farmacéuticos.
2. **Exigencia Legal de Trazabilidad y Citas:** El dictamen de auditoría emitido debe fundamentar fehacientemente el número de licitación, el artículo de las bases administrativas o la página del catálogo oficial donde se estipula el valor base.
3. **Cero Tolerancia a Alucinaciones Numéricas:** Confundir un precio de referencia de $22.40 CLP con $33.60 CLP induce a errores de adjudicación lesivos para el patrimonio fiscal o a declarar desiertas licitaciones viables.
4. **Presupuesto y Sostenibilidad Operativa:** El costo de operación y actualización de la solución debe ser compatible con la infraestructura tecnológica del sector público.

**Pregunta Arquitectónica Central:** ¿Qué técnica de personalización de modelos generativos (RAG, PEFT/LoRA o Full Fine-Tuning) satisface con mayor eficacia y menor costo operacional los requerimientos de auditoría de compras públicas de CENABAST?

---

## 2. OPCIONES CONSIDERADAS

### Opción A: Retrieval-Augmented Generation (RAG)
- **Mecanismo:** La información de catálogo y normativa se segmenta e indexa en un almacén vectorial persistente (`Gate 2/indice_gate2/`). Al recibir una consulta, se recuperan semánticamente los $k$ fragmentos más relevantes y se inyectan dinámicamente en el contexto del modelo fundacional, instruyéndolo a citar las fuentes identificadas.
- **Ventajas:** Actualización instantánea sin cómputo de re-entrenamiento (basta con actualizar el archivo markdown en disco y correr `indexar_corpus.py` en milisegundos). Trazabilidad nativa y citas explícitas `[fuente: archivo.md]`.
- **Desventajas:** Dependencia de la calidad del chunking y de la ventana de contexto del LLM.

### Opción B: Parameter-Efficient Fine-Tuning (PEFT / LoRA / QLoRA)
- **Mecanismo:** Congelar los pesos del modelo base e insertar adaptadores de bajo rango entrenables para especializar la sintaxis y estilo de los dictámenes de auditoría.
- **Ventajas:** Adapta el vocabulario institucional y la estructura formal de los dictámenes de CENABAST sin requerir entrenamiento completo.
- **Desventajas:** No resuelve el dinamismo de los precios numéricos; actualizar los valores de medicamentos exigiría re-entrenar los adaptadores periódicamente, corriendo el riesgo de memorización distorsionada y alucinaciones en cifras decimales.

### Opción C: Fine-Tuning Completo (Full Fine-Tuning)
- **Mecanismo:** Reentrenamiento integral de todos los parámetros de un modelo base con miles de pares instrucción-respuesta de licitaciones públicas.
- **Ventajas:** Máxima asimilación estilística del dominio.
- **Desventajas:** Prohibitivo en costos de hardware (múltiples GPUs A100/H100), inviable para actualización recurrente de precios volátiles, alto riesgo de olvido catastrófico (*catastrophic forgetting*) y naturaleza de caja negra sin capacidad de citar el párrafo oficial de origen.

---

## 3. MATRIZ DE EVALUACIÓN CUANTITATIVA
Con base en el algoritmo de evaluación implementado en `Gate 2/decision.py`, se ponderaron las 5 dimensiones clave en escala de 1.0 a 5.0 (5 = Óptimo, 1 = Inviable):

| Criterio de Decisión | Peso Relativo | RAG (Opción A) | PEFT / LoRA (Opción B) | Full Fine-Tuning (Opción C) |
|---|:---:|:---:|:---:|:---:|
| **1. Dinamismo de la Información** (Precios mensuales) | 25% | **5.0** (1.250) | 2.0 (0.500) | 1.0 (0.250) |
| **2. Auditabilidad y Citación Estricta de Fuentes** | 25% | **5.0** (1.250) | 2.5 (0.625) | 2.0 (0.500) |
| **3. Control de Alucinaciones en Cifras Numéricas** | 20% | **4.5** (0.900) | 3.0 (0.600) | 2.5 (0.500) |
| **4. Eficiencia de Costo y Mantenimiento** | 15% | **5.0** (0.750) | 4.0 (0.600) | 1.5 (0.225) |
| **5. Volumen de Datos de Entrenamiento Requeridos** | 15% | **5.0** (0.750) | 3.0 (0.450) | 2.0 (0.300) |
| **PUNTAJE PONDERADO TOTAL** | **100%** | **4.900 / 5.0** | **2.775 / 5.0** | **1.775 / 5.0** |

---

## 4. DECISIÓN FINAL Y CONSECUENCIAS OPERATIVAS

### Decisión Adoptada
Se adopta **Retrieval-Augmented Generation (RAG)** como la arquitectura principal de personalización para el servicio de auditoría de adquisiciones farmacéuticas de CENABAST.

### Consecuencias Operativas Positivas
1. **Actualización Ágil de Precios:** Cuando CENABAST emite un nuevo catálogo mensual de precios o una adenda a las bases de licitación, el equipo técnico únicamente deposita el nuevo documento en `Gate 2/data/` y corre el script `indexar_corpus.py`. El nuevo conocimiento queda disponible de inmediato para el auditor sin requerir entrenamiento.
2. **Defensa Jurídica Incontrovertible:** Cada dictamen emitido por el modelo acompaña la cita explícita del documento normativo (`[cenabast_catalogo_precios_referencia_2026.md]`), permitiendo a los abogados y auditores de la institución defender las decisiones ante el Tribunal de Contratación Pública o la Contraloría.
3. **Costo Marginal Mínimo:** La solución opera con vector store persistido localmente en disco (`indice_gate2/`), requiriendo consumo de tokens únicamente durante la fase de inferencia.

### Mitigaciones Implementadas
- Para compensar la sensibilidad de RAG al tamaño de fragmentos, se adoptó `RecursiveCharacterTextSplitter` con `chunk_size=500` y `chunk_overlap=100`, asegurando que tablas de precios y cláusulas de multas no queden truncadas entre bloques contiguos.
- Se implementó un filtro de seguridad anti-inyección de prompts previo a la inyección del contexto en el prompt final.
