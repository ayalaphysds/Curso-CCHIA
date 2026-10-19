"""
Pruebas unitarias para el módulo consumir_gemini.py
Especialización en IA Accenture - Curso CCHIA
Unidad U1.3 · Bloque 7: Rúbrica de Calidad y Manejo de Errores
"""

import unittest
from src.consumir_gemini import armar_peticion, enviar_peticion, extraer_texto, obtener_dato_de_prueba


class TestConsumirGemini(unittest.TestCase):

    def test_validacion_pregunta_vacia(self):
        """Verifica que armar_peticion lance ValueError si la pregunta está vacía."""
        with self.assertRaises(ValueError) as ctx:
            armar_peticion("")
        self.assertIn("no puede estar vacía", str(ctx.exception))

        with self.assertRaises(ValueError):
            armar_peticion("   ")

    def test_armar_peticion_valida(self):
        """Verifica que armar_peticion construya la URL y el body correctamente."""
        url, body = armar_peticion("Hola")
        self.assertIn("gemini-3.5-flash", url)
        self.assertEqual(body["contents"][0]["parts"][0]["text"], "Hola")

    def test_error_conexion_red(self):
        """Verifica que enviar_peticion capture ConnectionError y lance RuntimeError descriptivo."""
        url_invalida = "https://esta-direccion-no-existe-para-nada.test/error"
        with self.assertRaises(RuntimeError) as ctx:
            enviar_peticion(url_invalida, {})
        self.assertIn("No se pudo conectar", str(ctx.exception))

    def test_error_dato_faltante(self):
        """Verifica que extraer_texto capture KeyError/IndexError y lance RuntimeError descriptivo."""
        respuesta_incompleta = {"candidatos_mal_escrito": []}
        with self.assertRaises(RuntimeError) as ctx:
            extraer_texto(respuesta_incompleta)
        self.assertIn("La respuesta no trae el texto generado", str(ctx.exception))

    def test_extraer_texto_valido(self):
        """Verifica la extracción exitosa desde un payload mock válido."""
        datos_mock = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": "Respuesta simulada exitosa"}
                        ]
                    }
                }
            ]
        }
        texto = extraer_texto(datos_mock)
        self.assertEqual(texto, "Respuesta simulada exitosa")

    def test_flujo_completo_api_real(self):
        """Verifica el flujo de punta a punta con la API real (Happy path)."""
        resultado = obtener_dato_de_prueba("Di 'OK' en una palabra.")
        self.assertIsInstance(resultado, str)
        self.assertGreater(len(resultado), 0)


if __name__ == "__main__":
    unittest.main()
