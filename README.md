# 🏥 Miniaplicación de Consumo de IA — Especialización en IA Accenture (CCHIA)

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Gate 1: Habilitación Técnica](https://img.shields.io/badge/Gate%201-Aprobado-success.svg)](docs/decision-arquitectura.md)
[![Tests: 13/13 Passing](https://img.shields.io/badge/Unit%20Tests-13%2F13%20OK-brightgreen.svg)](tests/)

> **Proyecto Oficial de Habilitación Técnica (Gate 1)**  
> **Estudiante:** Sebastián Eduardo Ayala Vásquez (`sayala7` / `ayalaphysds`)  
> **Repositorio Remoto:** [`https://github.com/ayalaphysds/Curso-CCHIA.git`](https://github.com/ayalaphysds/Curso-CCHIA.git)

---

## 📌 1. Descripción del Proyecto

Esta miniaplicación implementa un **módulo modular y blindado para el consumo de modelos generativos vía API REST (Google Gemini API)**, aplicado al caso de uso de **auditoría de compras públicas y adquisiciones farmacéuticas (CENABAST / ChileCompra)**.

El sistema resuelve la evaluación de ofertas de medicamentos mediante prompts de sistema estructurados, contención integral de fallos de red/timeout/JSON, cálculo de costos monetarios en vivo a partir de metadatos de tokens (`usageMetadata`) y validación estricta de esquemas JSON con tipos (`responseSchema`).

---

## 🏗️ 2. Arquitectura de la Solución

El flujo técnico completo se ilustra en el siguiente diagrama de arquitectura (elaborado en el Bloque 8):

![Diagrama de Arquitectura de la Miniaplicación](docs/diagrama_arquitectura.png)

### Componentes Clave:
1. **`armar_peticion`:** Valida entradas, lee credenciales desde `.env` y construye URL + payload con `systemInstruction` y `generationConfig`.
2. **`enviar_peticion`:** Despacha la llamada HTTP POST vía `requests` con timeout controlado y contención `try/except`.
3. **`extraer_texto`:** Extrae el contenido textual limpio desde la estructura jerárquica de `candidates`.
4. **`calcular_costo`:** Calcula el costo exacto en dólares según los tokens de entrada y salida reportados en `usageMetadata`.
5. **`parsear_respuesta_json`:** Remueve bloques markdown y valida la presencia obligatoria de las claves requeridas.

---

## 📂 3. Estructura del Repositorio

```bash
Curso-CCHIA/
├── docs/                                  # Documentación técnica y evidencias
│   ├── diagrama_arquitectura.png          # Diagrama oficial del flujo técnico (Bloque 8)
│   ├── decision-arquitectura.md           # Registro formal de decisión de modelo (Bloque 9)
│   └── evidencia_peticion_autenticada.json# Evidencia de respuesta HTTP 200 OK (Bloque 4)
├── prompts/                               # Banco de prompts y validación (Bloque 10)
│   ├── banco.py                           # 3 prompts con systemInstruction y responseSchema
│   ├── test_consistencia.py               # Script de prueba de consistencia (3 repeticiones)
│   └── registro_resultados.json           # Registro de 100% de consistencia en salida JSON
├── src/                                   # Código fuente modular
│   ├── consumir_gemini.py                 # Módulo de integración principal blindado
│   ├── comparar_modelos.py                # Benchmark empírico de latencia y costos (Flash vs Pro)
│   ├── probar_conexion_api.py             # Script de validación de conexión inicial
│   └── verificar_entorno.py               # Diagnóstico de aislamiento de entorno virtual
├── tests/                                 # Suite de pruebas automatizadas
│   ├── test_consumir_gemini.py            # 13 pruebas unitarias exhaustivas (100% passing)
│   └── test_conexion.py                   # Prueba de contención de errores de red inducidos
├── .env.example                           # Plantilla de variables de entorno (sin secretos)
├── .gitignore                             # Protección estricta de .env y entornos virtuales
├── main.py                                # Punto de entrada ejecutable de la miniaplicación
├── requirements.txt                       # Dependencias fijadas y reproducibles
├── BITACORA_DE_AVANCE.md                  # Registro vivo del curso y trazabilidad de hitos
└── README.md                              # Documentación general y guía de ejecución
```

---

## 💻 4. Instalación y Ejecución Limpia (Reproducibilidad)

Sigue estos pasos para clonar, configurar y ejecutar la aplicación desde cero en cualquier máquina:

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/ayalaphysds/Curso-CCHIA.git
cd Curso-CCHIA
```

### Paso 2: Crear y Activar el Entorno Virtual

**En Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**En Linux / macOS / WSL:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno
Copia la plantilla `.env.example` y crea tu archivo `.env`:

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# Linux / macOS
cp .env.example .env
```

Edita `.env` e introduce tu clave de API:
```env
GEMINI_API_KEY=tu_clave_real_aqui
```

> 🔒 **Seguridad garantizada:** El archivo `.env` está expresamente excluido del repositorio mediante `.gitignore` y nunca ha sido commiteado al historial de Git.

### Paso 5: Ejecutar la Miniaplicación
```bash
python main.py
```

**Salida esperada:**
```text
======================================================================
  ACCENTURE / CCHIA — MINIAPLICACIÓN IA (GATE 1: HABILITACIÓN TÉCNICA)
======================================================================

[1/4] Entorno y credenciales verificados correctamente (.env cargado).
[2/4] Construyendo petición con prompt de sistema y responseSchema...
[3/4] Enviando petición HTTP POST a Google Gemini API...
[4/4] Respuesta recibida y estructurada exitosamente:
----------------------------------------------------------------------
Respuesta del modelo: {"sobreprecio_detectado": true, ...}
----------------------------------------------------------------------
Datos JSON parseados e indexados:
  • sobreprecio_detectado: True
  • desviacion_pct: 50.0
  • recomendacion: negociar
  • dictamen: El precio ofertado excede en 50% la mediana histórica...

Costo real calculado en vivo: $0.000159 USD
----------------------------------------------------------------------
Proceso terminado sin errores.
```

---

## 🧪 5. Ejecución de la Suite de Pruebas Unitarias

Para validar automáticamente todos los componentes, validaciones tempranas, control de excepciones de red, esquemas y parseo de JSON:

```bash
python -m unittest discover tests
```

**Resultado:**
```text
.............
----------------------------------------------------------------------
Ran 13 tests in 1.250s

OK
```

---

## 📊 6. Banco de Prompts y Consistencia (Bloque 10)

Para verificar la consistencia del banco de prompts estructurados:
```bash
python prompts/test_consistencia.py
```
*Tasa de éxito:* **100% de consistencia** (3/3 respuestas válidas en los 3 prompts) documentado en [`prompts/registro_resultados.json`](prompts/registro_resultados.json).

---

## 📋 7. Registro del Ensayo de Instalación Limpia (Bloque 11)

Conforme a la rúbrica del Gate 1, se ejecutó un ensayo completo de clonado e instalación desde cero en un directorio aislado:

- **Fecha de realización:** 20 de Octubre de 2026.
- **Entorno de prueba:** Carpeta aislada temporal (`prueba-gate1`), Windows 11 / PowerShell, Python 3.12.
- **Procedimiento probado:** `git clone` &rarr; `python -m venv` &rarr; `pip install -r requirements.txt` &rarr; `Copy-Item .env.example .env` &rarr; `python main.py`.
- **Hallazgos encontrados:** Ninguno. Todas las dependencias declaradas en `requirements.txt` se instalaron limpiamente sin requerir paquetes manuales.
- **Verificación de secretos:** Se ejecutó `git status` y `git log --all --oneline -- .env` confirmando que `.env` no aparece listado ni existe en ningún commit del historial.
- **Resultado del ensayo:** **Aprobado sin observaciones.** El proyecto corre de punta a punta de forma 100% autónoma y reproducible.

---

## 🎯 8. Checklist de Criterios No Compensables (Gate 1)

| Criterio Crítico No Compensable | Estado | Verificación / Evidencia |
| :--- | :---: | :--- |
| **1. Código ejecutable** | ✅ Cumplido | `main.py` corre de punta a punta sin tracebacks no capturados; suite con 13/13 tests OK. |
| **2. Entorno reproducible** | ✅ Cumplido | `requirements.txt` documentado y ejecutable con `pip install -r requirements.txt`. |
| **3. Credenciales protegidas** | ✅ Cumplido | `.env` protegido por `.gitignore`; historial limpio (`git log` sin rastros de secretos). |
| **4. Consumo exitoso de API** | ✅ Cumplido | Peticiones HTTP 200 recibiendo payloads válidos de Gemini API (`usageMetadata` y `candidates`). |

---
*Desarrollado para la Especialización en Inteligencia Artificial de Accenture.*
