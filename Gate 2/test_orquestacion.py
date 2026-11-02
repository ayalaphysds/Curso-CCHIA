"""
Pruebas Unitarias para Enrutamiento Condicional y Manejo de Errores (Bloque 20, U2.3).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Orquestación de Consultas

Criterios Verificados:
1. Enrutamiento correcto hacia las 3 ramas especializadas (catálogo, sobreprecio, abastecimiento) y la rama general.
2. Activación comprobada del fallback ante fallas simuladas en una rama especializada (with_fallbacks).
3. Contención total de excepciones en el envoltorio procesar_mensaje_seguro (cero caídas ante inputs anómalos).
"""

import unittest
from unittest.mock import patch, MagicMock
from langchain_core.runnables import RunnableLambda

from enrutamiento import (
    construir_enrutador_con_fallbacks,
    procesar_mensaje_seguro,
    ruta_catalogo,
    ruta_sobreprecio,
    ruta_abastecimiento,
    ruta_general,
    fallback_seguridad,
)


class TestOrquestacionCENABAST(unittest.TestCase):
    """Suite de validación de orquestación, bifurcación condicional y resiliencia de fallbacks."""

    def setUp(self):
        self.enrutador = construir_enrutador_con_fallbacks()

    # -------------------------------------------------------------------------
    # 1. Verificación de Bifurcación y Enrutamiento por Categoría
    # -------------------------------------------------------------------------
    def test_enrutamiento_rama_catalogo(self):
        """Verifica que consultas de catálogo se enruten a la rama 'catalogo'."""
        resultado = self.enrutador.invoke("¿Cuál es el precio de catálogo de Paracetamol?")
        self.assertEqual(resultado["ruta_ejecutada"], "catalogo")
        self.assertTrue(resultado["exito"])
        self.assertIn("22.40", resultado["respuesta"])

    def test_enrutamiento_rama_sobreprecio(self):
        """Verifica que consultas de auditoría de cotizaciones se dirijan a 'sobreprecio'."""
        resultado = self.enrutador.invoke("Auditar oferta de Ceftriaxona con precio 1290 CLP")
        self.assertEqual(resultado["ruta_ejecutada"], "sobreprecio")
        self.assertTrue(resultado["exito"])
        self.assertIn("Ceftriaxona", resultado["respuesta"])
        self.assertIn("3.20%", resultado["respuesta"])

    def test_enrutamiento_rama_abastecimiento(self):
        """Verifica que consultas sobre multas y quiebre de stock se dirijan a 'abastecimiento'."""
        resultado = self.enrutador.invoke("¿Cuál es la política de multas por atraso en abastecimiento?")
        self.assertEqual(resultado["ruta_ejecutada"], "abastecimiento")
        self.assertTrue(resultado["exito"])
        self.assertIn("Multa por atraso es del 1.0%", resultado["respuesta"])

    def test_enrutamiento_rama_general_por_defecto(self):
        """Verifica que consultas no especializadas caigan a la rama 'general'."""
        resultado = self.enrutador.invoke("Hola, buenos días, quisiera información sobre la institución")
        self.assertEqual(resultado["ruta_ejecutada"], "general")
        self.assertTrue(resultado["exito"])

    # -------------------------------------------------------------------------
    # 2. Verificación de Activación de Fallbacks (Manejo de Errores por Paso)
    # -------------------------------------------------------------------------
    def test_activacion_fallback_en_rama_con_falla(self):
        """Verifica que si una rama especializada lanza excepción, se active el fallback_seguridad."""
        def rama_defectuosa(datos):
            raise ConnectionResetError("Fallo simulado de base de datos o servicio externo")

        # Construir rama protegida con with_fallbacks
        rama_protegida = RunnableLambda(rama_defectuosa).with_fallbacks([RunnableLambda(fallback_seguridad)])
        salida = rama_protegida.invoke({"categoria": "catalogo"})

        self.assertEqual(salida["ruta_ejecutada"], "fallback_seguridad")
        self.assertFalse(salida["exito"])
        self.assertIn("CONTINGENCIA ACTIVADA", salida["respuesta"])

    # -------------------------------------------------------------------------
    # 3. Verificación de Contención de Errores en procesar_mensaje_seguro
    # -------------------------------------------------------------------------
    def test_procesar_mensaje_seguro_con_entradas_invalidas(self):
        """Verifica que strings vacíos o None sean contenidos y devuelvan respuesta amigable."""
        res_vacio = procesar_mensaje_seguro("")
        self.assertEqual(res_vacio["estado"], "error_contenido")
        self.assertEqual(res_vacio["ruta_ejecutada"], "validacion_entrada")
        self.assertIn("no puede estar vacía", res_vacio["respuesta"])

        res_none = procesar_mensaje_seguro(None)
        self.assertEqual(res_none["estado"], "error_contenido")

    @patch("enrutamiento.construir_enrutador_con_fallbacks")
    def test_procesar_mensaje_seguro_contiene_excepcion_inesperada(self, mock_construir):
        """Verifica que una falla crítica no controlada en el grafo sea capturada sin tumbar el servicio."""
        mock_orquestador = MagicMock()
        mock_orquestador.invoke.side_effect = RuntimeError("Error inesperado en memoria")
        mock_construir.return_value = mock_orquestador

        res = procesar_mensaje_seguro("Consulta válida que provoca error interno simulado")
        self.assertEqual(res["estado"], "error_contenido")
        self.assertEqual(res["ruta_ejecutada"], "fallback_general")
        self.assertIn("error interno temporal", res["respuesta"])
        self.assertIsNotNone(res["error"])


if __name__ == "__main__":
    unittest.main()
