# Verificación cruzada del despliegue

Revisor: Sebastián Eduardo Ayala Vásquez (autorrevisión diferida en clon limpio)
Repositorio revisado: https://github.com/ayalaphysds/Curso-CCHIA (rama main, carpeta Gate 3)
Fecha: 2026-11-24
Se siguió únicamente: README.md

## Resultado por criterio

- VC-1 (clon limpio): PASA - clon limpio ejecutado en directorio temporal con `git clone`, sin archivos `.env` ni artefactos locales rastreados.
- VC-2 (configuración documentada): PASA - `.env.example` documenta las 5 variables (`GEMINI_API_KEY` vacia, `ENTORNO`, `MODELO`, `PERMITIR_RESPALDO`, `UMBRAL_SOBREPRECIO_PCT`) en correspondencia exacta con `README.md`.
- VC-3 (arranque con un comando): PASA - `compose.yaml` declara los servicios `api` e `interfaz` con versiones fijas (`:1.0`) y `depends_on: condition: service_healthy`; verificado arranque de ambos servicios en puertos `8000` y `8080`.
- VC-4 (servicios sanos y alcanzables): PASA - `GET http://127.0.0.1:8000/salud` y `GET http://127.0.0.1:8080/salud` responden HTTP `200` con estado `ok`.
- VC-5 (comportamiento verificable): PASA - `GET http://127.0.0.1:8080/preguntar` enruta hacia `http://api:8000/consultas` y devuelve la respuesta fundamentada con `fuentes` CENABAST; los 12 casos de `casos.py` pasan al 100%.
- VC-6 (sin secretos y apagado limpio): PASA - `buscar_secretos.py` reporta 0 fugas y ambos `Dockerfile` cumplen 7/7 reglas (usuario no-root, `.dockerignore` y `HEALTHCHECK`).

## Hallazgos

- Hallazgo 1 (VC-2): Inicialmente la variable `UMBRAL_SOBREPRECIO_PCT` se usaba en `servicio/config.py` pero faltaba en `.env.example` y en `compose.yaml`.
  Decisión: aceptado - se incorporó `UMBRAL_SOBREPRECIO_PCT=15.0` en `.env.example`, `compose.yaml` y la tabla de `README.md`.

- Hallazgo 2 (VC-5): Una consulta fuera de dominio sobre `"temperatura en Marte"` coincidía con la palabra `"temperatura"` de cadena de frío en el recuperador léxico.
  Decisión: aceptado - se ajustó el peso de `"temperatura"` en `servicio/recuperador.py` para exigir contexto farmacéutico adicional antes de superar el umbral mínimo.
