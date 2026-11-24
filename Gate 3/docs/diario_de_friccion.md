# Diario de fricción — Ejecución en frío del proyecto

| # | Qué ocurrió al intentar ejecutar | Qué faltaba documentar | Sección del README que lo resuelve |
|---|---|---|---|
| 1 | Se desconocía la versión mínima de Python y si se requería Docker para pruebas unitarias | Version exacta de Python (`3.12`) y requisito opcional de Docker | Requisitos |
| 2 | `pip install -r requirements.txt` no instalaba `pytest` | Diferencia entre `requirements.txt` y `requirements-dev.txt` con entorno virtual | Instalación |
| 3 | Duda sobre si `GEMINI_API_KEY` era obligatoria al arrancar localmente | Tabla completa de variables con etiqueta `(secreto)` vs `(configuración)` | Configuración |
| 4 | No estaba explícito el comando `uvicorn` ni los puertos de ambos servicios | Comandos exactos de arranque local (`uvicorn`) y con `docker compose` | Cómo arrancar |
| 5 | Sin petición de ejemplo verificada para validar el servicio vivo | Ejemplos `curl`/HTTP en `127.0.0.1:8000` y `127.0.0.1:8080` | Cómo comprobar que funciona |
| 6 | No era evidente cómo ejecutar la suite completa de pruebas | Comando literal `python -m pytest -q` y scripts verificadores | Pruebas |
| 7 | No se entendía por qué el modelo por defecto es simulado ni por qué existe un recuperador léxico | Resumen de decisiones `D-01`..`D-06` enlazado a `docs/decisiones.md` | Decisiones técnicas |
| 8 | Al preguntar en inglés el sistema devolvió abstención y pareció un bug | Tabla de limitaciones conocidas `LIM-01`..`LIM-03` enlazada a `docs/limitaciones.md` | Limitaciones conocidas |
| 9 | Costaba distinguir qué carpeta contiene la API, la interfaz y las evidencias | Árbol de carpetas del repositorio con descripción de cada archivo | Estructura del repositorio |
| 10 | Puerto `8000` ocupado o falta de `GEMINI_API_KEY` con `MODELO=real` causaban confusión | Guía de diagnóstico rápido con causas y soluciones | Problemas frecuentes |
