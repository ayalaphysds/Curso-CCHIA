"""Registro estructurado de la prueba cruzada de transferencia (Bloque 45.2)."""

META_MINUTOS = 15.0

SESIONES = [
    {"ronda": 1, "minutos": 18.5, "exito": True, "observador": "Par técnico (simulación en frío)"},
    {"ronda": 2, "minutos": 9.2, "exito": True, "observador": "Par técnico (tras correcciones de documentación)"},
]

OBSERVACIONES = [
    {
        "id": "T-01",
        "ronda": 1,
        "sintoma": "Al instalar solo requirements.txt faltaba pytest para correr la suite local",
        "causa": "documento",
        "accion": "Se agrego explicacion explicita de requirements-dev.txt en la seccion Instalacion de README.md",
        "estado": "resuelta",
    },
    {
        "id": "T-02",
        "ronda": 1,
        "sintoma": "El evaluador dudo que comando usar para regenerar docs/api.md tras editar un endpoint",
        "causa": "documento",
        "accion": "Se documento python generar_api_md.py --comprobar en README.md",
        "estado": "resuelta",
    },
    {
        "id": "T-03",
        "ronda": 1,
        "sintoma": "No quedaba claro que formato de codigo ONU acepta POST /precios/evaluar sin abrir /docs",
        "causa": "documento",
        "accion": "Se incorporo ejemplo ejecutable API-04 con codigo_onu 51181504 en docs/api.md",
        "estado": "resuelta",
    },
    {
        "id": "T-04",
        "ronda": 2,
        "sintoma": "Arranque, verificacion de salud y pruebas unitarias completados sin intervencion en 9.2 minutos",
        "causa": "ninguna",
        "accion": "Se confirmo cumplimiento de la meta operativa <= 15 minutos",
        "estado": "resuelta",
    },
    {
        "id": "T-05",
        "ronda": 2,
        "sintoma": "Al consultar en ingles ('What is the reference price of acetaminophen?') el servicio devolvio abstencion sin fuentes",
        "causa": "producto",
        "ref": "LIM-02",
        "accion": "Declarada formalmente como limitacion LIM-02 en docs/limitaciones.md y riesgo aceptado R-09",
        "estado": "declarada",
    },
    {
        "id": "T-06",
        "ronda": 2,
        "sintoma": "Al usar sinonimo informal ('remedio para bajar la fiebre') en lugar de Paracetamol el recuperador devolvio abstencion",
        "causa": "producto",
        "ref": "LIM-02",
        "accion": "Declarada junto a T-05 en LIM-02 y fijada mediante prueba de regresion en test_recuperar.py",
        "estado": "declarada",
    },
]
