# 🏥 Especialización en Inteligencia Artificial (Accenture — CCHIA)
## Sistema de Optimización y Auditoría de Compras Públicas (CENABAST)

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Gate 1: Habilitación Técnica](https://img.shields.io/badge/Gate%201-Completado-success.svg)](Gate%201/README.md)
[![Gate 2: Componentes IA & RAG](https://img.shields.io/badge/Gate%202-En%20Desarrollo-orange.svg)](Gate%202/README.md)

> **Repositorio Oficial de Entregables y Actividades Prácticas**  
> **Estudiante:** Sebastián Eduardo Ayala Vásquez (`sayala7` / `ayalaphysds`)  
> **Programa:** Especialización en Inteligencia Artificial — Accenture & CCHIA  
> **Repositorio Remoto:** [`https://github.com/ayalaphysds/Curso-CCHIA.git`](https://github.com/ayalaphysds/Curso-CCHIA.git)

---

## 📌 1. Visión General del Proyecto

Este repositorio concentra el desarrollo incremental de las soluciones de Inteligencia Artificial aplicadas al caso de negocio de **auditoría, contención de sobreprecios y análisis documental en adquisiciones públicas farmacéuticas para CENABAST** (Central de Abastecimiento del Sistema Nacional de Servicios de Salud de Chile / Mercado Público).

El repositorio está estructurado en macro-carpetas correspondientes a los hitos evaluativos del programa formativo (*Gates*), garantizando aislamiento modular, trazabilidad histórica en Git y reproducibilidad autónoma de cada componente.

---

## 🏗️ 2. Arquitectura y Estructura del Repositorio

```bash
Curso-CCHIA/
├── .env.example                     # Plantilla transversal de variables de entorno
├── .gitignore                       # Reglas globales de exclusión (protección estricta de .env y .venv)
├── BITACORA_DE_AVANCE.md            # Registro vivo transversal de actividades, evidencias y reflexiones
├── requirements.txt                 # Dependencias base del proyecto (requests, python-dotenv, etc.)
├── README.md                        # Índice maestro y guía de navegación (este archivo)
│
├── Gate 1/                          # ── HITO 1: HABILITACIÓN TÉCNICA Y CLIENTE BASE ──
│   ├── .env.example                 # Variables de entorno específicas para Gate 1
│   ├── requirements.txt             # Dependencias fijadas y reproducibles de Gate 1
│   ├── README.md                    # Documentación técnica y Contrato de Interfaz Downstream JSON
│   ├── main.py                      # Punto de entrada ejecutable de la miniaplicación
│   ├── docs/                        # Diagrama de arquitectura, ADR de modelo y evidencia HTTP 200
│   │   ├── decision-arquitectura.md
│   │   ├── diagrama_arquitectura.png
│   │   └── evidencia_peticion_autenticada.json
│   ├── prompts/                     # Banco de prompts estructurados y validación de consistencia
│   │   ├── banco.py
│   │   ├── registro_resultados.json
│   │   └── test_consistencia.py
│   ├── src/                         # Módulos de consumo de Gemini API, cálculo de costos y benchmarks
│   │   ├── comparar_modelos.py
│   │   ├── consumir_gemini.py
│   │   ├── probar_conexion_api.py
│   │   └── verificar_entorno.py
│   └── tests/                       # Suite de pruebas automatizadas (13/13 passing)
│       ├── test_conexion.py
│       └── test_consumir_gemini.py
│
└── Gate 2/                          # ── HITO 2: CONSTRUCCIÓN DE COMPONENTES IA & RAG ──
    ├── .env.example                 # Variables de entorno para Gate 2
    ├── cliente.py                   # Cliente modular con política de reintento (Bloque 12)
    ├── cliente_api.py               # Capa de transporte HTTP y clasificación de errores (Bloque 12)
    ├── cliente_reintento.py         # Mecanismo de reintentos ante fallas transitorias (Bloque 12)
    └── [Actividades Core & RAG]     # Módulos de indexación, seguridad, observabilidad y supervisión
```

---

## 🚀 3. Guía de Inicio Rápido (Quickstart)

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

### Paso 4: Configurar Credenciales
Copia la plantilla `.env.example` en la raíz (y/o dentro de `Gate 1/`):
```powershell
Copy-Item .env.example .env
```
Edita `.env` e incorpora tu clave de API de Google Gemini:
```env
GEMINI_API_KEY=tu_clave_real_aqui
```

---

## 🚦 4. Ejecución por Hito (Gates)

### Gate 1: Habilitación Técnica
Para consultar la especificación completa, diagramas y el **Contrato Formal de Interfaz Downstream (JSON Schema Draft 2020-12 / OpenAPI 3.1)**, consulta el [README de Gate 1](Gate%201/README.md).

- **Ejecutar la miniaplicación CLI:**
  ```bash
  python "Gate 1/main.py"
  # O bien:
  cd "Gate 1"; python main.py; cd ..
  ```

- **Ejecutar la suite de pruebas unitarias (13 tests):**
  ```bash
  python -m unittest discover -s "Gate 1/tests"
  # O bien:
  cd "Gate 1"; python -m unittest discover tests; cd ..
  ```

- **Ejecutar prueba de consistencia de prompts (Bloque 10):**
  ```bash
  python "Gate 1/prompts/test_consistencia.py"
  ```

### Gate 2: Componentes IA y Pipeline RAG
Para consultar el desarrollo de las actividades core del Módulo 2 y la solución modular RAG para CENABAST:
- [Ver documentación de Gate 2](Gate%202/README.md) *(en desarrollo)*.

---

## 📋 5. Trazabilidad Curricular

Todo el progreso, bitácora de lecciones, decisiones de arquitectura y reflexiones pedagógicas se encuentran documentados de forma centralizada en:
- 📖 [`BITACORA_DE_AVANCE.md`](BITACORA_DE_AVANCE.md)

---
*Desarrollado para la Especialización en Inteligencia Artificial de Accenture.*
