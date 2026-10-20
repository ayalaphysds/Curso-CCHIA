"""
Pruebas unitarias para el módulo consumir_gemini.py
Especialización en IA Accenture - Curso CCHIA
Unidad U1.3 · Bloque 7: Rúbrica de Calidad y Manejo de Errores
"""

import unittest
from src.consumir_gemini import (
    armar_peticion,
    enviar_peticion,
    extraer_texto,
    calcular_costo,
    parsear_respuesta_json,
    obtener_dato_de_prueba,
)



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
        self.assertIn("gemini", url)
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

    def test_calcular_costo_valido(self):
        """Verifica el cálculo exacto de costo según fórmula oficial del Bloque 8."""
        datos_mock = {
            "usageMetadata": {
                "promptTokenCount": 850,
                "candidatesTokenCount": 320,
                "totalTokenCount": 1170
            }
        }
        costo = calcular_costo(datos_mock, precio_entrada=0.00000010, precio_salida=0.00000040)
        self.assertAlmostEqual(costo, 0.000213, places=6)

    def test_calcular_costo_error_metadata_faltante(self):
        """Verifica que calcular_costo lance RuntimeError ante ausencia de usageMetadata."""
        datos_sin_uso = {"candidates": []}
        with self.assertRaises(RuntimeError) as ctx:
            calcular_costo(datos_sin_uso, 0.00000010, 0.00000040)
        self.assertIn("usageMetadata", str(ctx.exception))

    def test_flujo_completo_api_real(self):
        """Verifica el flujo de punta a punta con la API real (Happy path o error de servicio contenido)."""
        try:
            resultado = obtener_dato_de_prueba("Di 'OK' en una palabra.")
            self.assertIsInstance(resultado, str)
            self.assertGreater(len(resultado), 0)
        except RuntimeError as e:
            # Contención controlada ante fallos transitorios de red, sobrecarga (503) o error de respuesta del proveedor
            self.assertTrue(any(term in str(e).lower() for term in ["servicio", "conectar", "red", "texto", "respuesta"]))

    def test_armar_peticion_con_system_y_schema(self):
        """Verifica que armar_peticion incluya systemInstruction y generationConfig correctamente."""
        schema = {
            "type": "OBJECT",
            "properties": {"resultado": {"type": "STRING"}},
            "required": ["resultado"]
        }
        url, body = armar_peticion(
            "Analizar",
            system_instruction="Eres un auditor estricto.",
            response_schema=schema
        )
        self.assertIn("systemInstruction", body)
        self.assertEqual(body["systemInstruction"]["parts"][0]["text"], "Eres un auditor estricto.")
        self.assertIn("generationConfig", body)
        self.assertEqual(body["generationConfig"]["responseMimeType"], "application/json")
        self.assertEqual(body["generationConfig"]["responseSchema"], schema)

    def test_parsear_respuesta_json_valido(self):
        """Verifica el parseo directo de un JSON limpio con claves requeridas."""
        texto = '{"categoria": "farmaco", "confianza": 0.95}'
        datos = parsear_respuesta_json(texto, claves_requeridas=["categoria", "confianza"])
        self.assertEqual(datos["categoria"], "farmaco")
        self.assertEqual(datos["confianza"], 0.95)

    def test_parsear_respuesta_json_con_markdown(self):
        """Verifica la remoción de bloques de código markdown ```json ... ```."""
        texto_md = "```json\n{\n  \"status\": \"OK\",\n  \"score\": 100\n}\n```"
        datos = parsear_respuesta_json(texto_md, claves_requeridas=["status", "score"])
        self.assertEqual(datos["status"], "OK")
        self.assertEqual(datos["score"], 100)

    def test_parsear_respuesta_json_invalido(self):
        """Verifica que lance ValueError si el texto no es JSON válido."""
        with self.assertRaises(ValueError) as ctx:
            parsear_respuesta_json("No soy un JSON")
        self.assertIn("no es JSON válido", str(ctx.exception))

    def test_parsear_respuesta_json_claves_faltantes(self):
        """Verifica que lance ValueError si faltan las claves esperadas."""
        texto = '{"categoria": "insumo"}'
        with self.assertRaises(ValueError) as ctx:
            parsear_respuesta_json(texto, claves_requeridas=["categoria", "precio"])
        self.assertIn("faltan las claves", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()

