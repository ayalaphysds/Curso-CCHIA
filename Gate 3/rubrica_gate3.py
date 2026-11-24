"""Rubrica oficial del Gate 3 / Capstone codificada como datos (Bloque S2.3)."""

UMBRAL = 60

CRITERIOS = [
    {
        "id": "C1",
        "nombre": "Problema, requerimientos y arquitectura",
        "peso": 10,
        "fuentes": ["ficha", "decisiones"],
    },
    {
        "id": "C2",
        "nombre": "Funcionamiento end-to-end",
        "peso": 25,
        "fuentes": ["frio", "demo", "stack", "ejecucion"],
    },
    {
        "id": "C3",
        "nombre": "Integracion IA, orquestacion y RAG",
        "peso": 15,
        "fuentes": ["mitigaciones", "ia"],
    },
    {
        "id": "C4",
        "nombre": "Backend FastAPI y Docker",
        "peso": 15,
        "fuentes": ["servicio", "api_md", "dockerfile", "compose"],
    },
    {
        "id": "C5",
        "nombre": "QA, pruebas y evaluacion de calidad",
        "peso": 10,
        "fuentes": ["pytest", "matriz", "parciales"],
    },
    {
        "id": "C6",
        "nombre": "Seguridad, riesgos y trazabilidad",
        "peso": 10,
        "fuentes": ["riesgos", "secretos", "registro"],
    },
    {
        "id": "C7",
        "nombre": "Documentacion tecnica",
        "peso": 5,
        "fuentes": ["readme", "transferencia"],
    },
    {
        "id": "C8",
        "nombre": "Demo y defensa tecnica",
        "peso": 10,
        "fuentes": ["guion", "demo", "respaldo"],
    },
]

NO_COMPENSABLES = [
    {
        "id": "NC-1",
        "nombre": "La solucion se ejecuta de punta a punta en el entorno contenerizado",
        "fuentes": ["frio", "demo", "stack", "ejecucion"],
    },
    {
        "id": "NC-2",
        "nombre": "El servicio expone endpoints funcionales y validados",
        "fuentes": ["servicio"],
    },
    {
        "id": "NC-3",
        "nombre": "La demo se ejecuta en vivo sobre la solucion construida, no sobre material grabado",
        "fuentes": [],
        "evaluador": "Que la demostracion corra en vivo, en la defensa.",
    },
    {
        "id": "NC-4",
        "nombre": "Sin credenciales ni datos reales en el repositorio ni en el corpus",
        "fuentes": ["secretos"],
        "evaluador": "Que los datos del corpus sean simulados.",
    },
]

ENTREGABLES = [
    ("Codigo y contenedor", ["Dockerfile", "compose.yaml", "servicio/main.py"]),
    ("README tecnico", ["README.md"]),
    ("Matrices de prueba y riesgo", ["docs/matriz_pruebas.md", "docs/matriz_riesgos.md"]),
    ("Demo en vivo", ["ensayo_demo.py", "docs/demo_respaldo.md"]),
    ("Presentacion ejecutiva", ["docs/defensa.md"]),
]
