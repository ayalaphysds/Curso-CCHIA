"""Dobles de prueba controlados para verificacion de alucinaciones (Bloque 43.3)."""


class ModeloAlucinador:
    """Modelo doble que siempre devuelve una respuesta predefinida para probar contencion."""

    nombre = "alucinador"

    def __init__(self, respuesta: str) -> None:
        self.respuesta = respuesta

    def generar(self, prompt: str, pregunta: str = "", fragmentos=None) -> str:
        return self.respuesta
