# GUÍA INTEGRAL DE ENTREGAS Y ENLACES GITHUB — MÓDULO 3 Y GATE 3 CAPSTONE
**Especialización en Inteligencia Artificial Generativa — Accenture / CCHIA**  
**Proyecto Aplicado:** Plataforma End-to-End de Auditoría de Precios y Licitaciones CENABAST  
**Alumno:** Sebastián Eduardo Ayala Vásquez  
**Carpeta de Entregables:** `Curso-CCHIA/Gate 3`  
**Repositorio Remoto:** `https://github.com/ayalaphysds/Curso-CCHIA`

---

## 📌 Índice Rápido de Enlaces Directos para Skillnest

Cuando Skillnest solicite un único enlace en la pestaña **Enlace (Drive, etc.)**, pega directamente la URL correspondiente a cada actividad Core para que el evaluador aterrice sin buscar:

| # | Actividad Core en Skillnest | Enlace Directo en GitHub | Verificador Local |
|---:|---|---|---|
| **1** | **Bloque 34 · U3.1** — Define tus criterios de aceptación y plan por hitos `[Core]` | `https://github.com/ayalaphysds/Curso-CCHIA/blob/main/Gate%203/docs/ficha_diseno_funcional.md` | `python verificar_ficha_completa.py` (5/5) |
| **2** | **Bloque 36 · U3.2** — Prueba tus endpoints con casos válidos e inválidos `[Core]` | `https://github.com/ayalaphysds/Curso-CCHIA/blob/main/Gate%203/docs/registro_pruebas.md` | `python -m pytest tests/test_api.py -q` y `python cliente_externo.py` (12/12) |
| **3** | **Bloque 38 · U3.3** — Compón tus servicios y documenta el procedimiento `[Core]` | `https://github.com/ayalaphysds/Curso-CCHIA/blob/main/Gate%203/compose.yaml` | `python verificar_entrega.py` (7/7) y `python verificar_dockerfile.py` (7/7) |
| **4** | **Bloque 41 · U3.4** — Registra la evidencia de tu ejecución completa `[Core]` | `https://github.com/ayalaphysds/Curso-CCHIA/blob/main/Gate%203/docs/registro_ejecucion.md` | `python verificar_ejecucion.py` (5/5) y `python verificar_registro.py` (6/6) |
| **5** | **Bloque 43 · U3.5** — Completa tu Matriz de Riesgos con mitigaciones verificadas `[Core]` | `https://github.com/ayalaphysds/Curso-CCHIA/blob/main/Gate%203/docs/matriz_riesgos.md` | `python verificar_mitigaciones.py` (17/17) y `python verificar_riesgos.py` (6/6) |
| **6** | **Bloque 45 · U3.6** — Registra tus decisiones de arquitectura y limitaciones `[Core]` | `https://github.com/ayalaphysds/Curso-CCHIA/blob/main/Gate%203/docs/decisiones.md` | `python verificar_decisiones.py` (7/7) y `python verificar_readme.py` (8/8) |
| **7** | **Bloque S2 · U3.7** — Gate 3 / Capstone - Aplicación end-to-end `[Core]` | `https://github.com/ayalaphysds/Curso-CCHIA/tree/main/Gate%203` | `python verificar_gate3.py` (19/19 locales; `--con-docker --escribir` para 22/22) |

---

## Detalle por Actividad Core

### 1. Bloque 34 (U3.1) — Criterios de aceptación y plan por hitos `[Core]`
- **Enlace principal:** `https://github.com/ayalaphysds/Curso-CCHIA/blob/main/Gate%203/docs/ficha_diseno_funcional.md`
- **Archivos complementarios:** `Gate 3/docs/diagrama_arquitectura.png`, `Gate 3/docs/revision_alcance.md`, `Gate 3/verificar_ficha_completa.py`, `Gate 3/resumen_ficha.py`.
- **Comandos de verificación (desde `Gate 3/`):**
  ```powershell
  ..\.venv\Scripts\python.exe resumen_ficha.py
  ..\.venv\Scripts\python.exe verificar_ficha_completa.py
  ```

### 2. Bloque 36 (U3.2) — Validación de entradas y pruebas desde cliente HTTP `[Core]`
- **Enlace principal:** `https://github.com/ayalaphysds/Curso-CCHIA/blob/main/Gate%203/docs/registro_pruebas.md`
- **Archivos complementarios:** `Gate 3/servicio/main.py`, `Gate 3/servicio/esquemas.py`, `Gate 3/servicio/errores.py`, `Gate 3/casos.py`, `Gate 3/tests/test_api.py`, `Gate 3/cliente_externo.py`.
- **Comandos de verificación (desde `Gate 3/`):**
  ```powershell
  ..\.venv\Scripts\python.exe verificar_servicio.py
  ..\.venv\Scripts\python.exe -m pytest tests/test_api.py -v
  ```

### 3. Bloque 38 (U3.3) — Composición de servicios y procedimiento `[Core]`
- **Enlace principal:** `https://github.com/ayalaphysds/Curso-CCHIA/blob/main/Gate%203/compose.yaml`
- **Archivos complementarios:** `Gate 3/Dockerfile`, `Gate 3/interfaz/Dockerfile`, `Gate 3/interfaz/main.py`, `Gate 3/.env.example`, `Gate 3/docs/verificacion_cruzada.md`, `Gate 3/verificar_entrega.py`, `Gate 3/buscar_secretos.py`.
- **Comandos de verificación (desde `Gate 3/`):**
  ```powershell
  ..\.venv\Scripts\python.exe verificar_dockerfile.py
  ..\.venv\Scripts\python.exe verificar_dockerfile.py interfaz/Dockerfile
  ..\.venv\Scripts\python.exe buscar_secretos.py
  ..\.venv\Scripts\python.exe verificar_entrega.py
  ```

### 4. Bloque 41 (U3.4) — Evidencia de ejecución completa `[Core]`
- **Enlace principal:** `https://github.com/ayalaphysds/Curso-CCHIA/blob/main/Gate%203/docs/registro_ejecucion.md`
- **Archivos complementarios:** `Gate 3/escenarios.py`, `Gate 3/docs/bitacora_ajustes.md`, `Gate 3/docs/pruebas_parciales.md`, `Gate 3/docs/respaldos.md`, `Gate 3/verificar_ejecucion.py`, `Gate 3/verificar_registro.py`.
- **Comandos de verificación (desde `Gate 3/`):**
  ```powershell
  ..\.venv\Scripts\python.exe verificar_parciales.py
  ..\.venv\Scripts\python.exe verificar_registro.py
  ```

### 5. Bloque 43 (U3.5) — Matriz de Riesgos con mitigaciones verificadas `[Core]`
- **Enlace principal:** `https://github.com/ayalaphysds/Curso-CCHIA/blob/main/Gate%203/docs/matriz_riesgos.md`
- **Archivos complementarios:** `Gate 3/riesgos.py`, `Gate 3/verificar_riesgos.py`, `Gate 3/verificar_mitigaciones.py`, `Gate 3/docs/matriz_pruebas.md`, `Gate 3/docs/registro_alucinaciones.md`.
- **Comandos de verificación (desde `Gate 3/`):**
  ```powershell
  ..\.venv\Scripts\python.exe verificar_matriz.py
  ..\.venv\Scripts\python.exe verificar_mitigaciones.py
  ..\.venv\Scripts\python.exe verificar_riesgos.py
  ```

### 6. Bloque 45 (U3.6) — Decisiones de arquitectura y limitaciones `[Core]`
- **Enlace principal:** `https://github.com/ayalaphysds/Curso-CCHIA/blob/main/Gate%203/docs/decisiones.md`
- **Archivos complementarios:** `Gate 3/docs/limitaciones.md`, `Gate 3/docs/api.md`, `Gate 3/docs/transferencia.md`, `Gate 3/README.md`, `Gate 3/verificar_decisiones.py`, `Gate 3/verificar_readme.py`.
- **Comandos de verificación (desde `Gate 3/`):**
  ```powershell
  ..\.venv\Scripts\python.exe generar_api_md.py --comprobar
  ..\.venv\Scripts\python.exe verificar_transferencia.py
  ..\.venv\Scripts\python.exe verificar_decisiones.py
  ..\.venv\Scripts\python.exe verificar_readme.py
  ```

### 7. Gate 3 / Capstone (Bloque S2 · U3.7) — Aplicación end-to-end `[Core]`
- **Enlace principal:** `https://github.com/ayalaphysds/Curso-CCHIA/tree/main/Gate%203`
- **Evidencia consolidada del verificador maestro:** `https://github.com/ayalaphysds/Curso-CCHIA/blob/main/Gate%203/docs/gate3.md`
- **Guion de defensa (8 min + 7 diapositivas) y plan B de demo:**
  - `https://github.com/ayalaphysds/Curso-CCHIA/blob/main/Gate%203/docs/defensa.md`
  - `https://github.com/ayalaphysds/Curso-CCHIA/blob/main/Gate%203/docs/demo_respaldo.md`
- **Comandos previos a la defensa en vivo (desde `Gate 3/`):**
  ```powershell
  ..\.venv\Scripts\python.exe ensayo_demo.py --comprobar
  ..\.venv\Scripts\python.exe medir_guion.py
  ..\.venv\Scripts\python.exe verificar_gate3.py --escribir
  # En entorno con Docker Desktop activo para cerrar las 3 fuentes de contenedores (APRUEBA):
  ..\.venv\Scripts\python.exe verificar_gate3.py --con-docker --escribir
  ```
