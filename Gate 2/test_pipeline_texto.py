"""
Pruebas Unitarias para el Pipeline de Texto y Métricas Léxicas (Bloque 15, U2.2).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Auditoría de Precios
"""

import unittest
from pipeline_texto import procesar_texto, calcular_metricas


class TestPipelineTexto(unittest.TestCase):
    """Casos de prueba para normalización, tokenización y cálculo de métricas léxicas."""

    # -------------------------------------------------------------------------
    # 1. Pruebas de Limpieza y Tokenización (procesar_texto)
    # -------------------------------------------------------------------------
    def test_procesar_texto_normal(self):
        """Verifica minúsculas, eliminación de signos ortográficos y tokenización correcta."""
        texto = "¡Atención! Licitación 723-14-LP24: Paracetamol 500mg a $33.60 CLP."
        tokens = procesar_texto(texto)
        self.assertIn("atención", tokens)
        self.assertIn("licitación", tokens)
        self.assertIn("paracetamol", tokens)
        self.assertIn("500mg", tokens)
        self.assertIn("33", tokens)
        self.assertIn("60", tokens)
        self.assertIn("clp", tokens)
        # Asegurar que ningún signo de puntuación quedó suelto como token
        for t in tokens:
            self.assertFalse(any(c in "!?,;:$" for c in t))

    def test_procesar_texto_vacio_y_espacios(self):
        """Verifica que strings vacíos o con solo espacios retornen lista vacía []."""
        self.assertEqual(procesar_texto(""), [])
        self.assertEqual(procesar_texto("   \t\n  "), [])
        self.assertEqual(procesar_texto(None), [])

    def test_procesar_texto_solo_puntuacion(self):
        """Verifica que textos compuestos únicamente por signos de puntuación retornen [] sin excepciones."""
        self.assertEqual(procesar_texto("¡¡¡...???,,,;;;:::---_"), [])
        self.assertEqual(procesar_texto("$$$ %%% &&& @@@"), [])

    def test_procesar_texto_conserva_caracteres_espanoles_y_tildes(self):
        """Verifica preservación de eñes, acentos y diéresis en español."""
        texto = "Cenabast adjudicó Losartán con un daño mínimo a la distribución."
        tokens = procesar_texto(texto)
        self.assertIn("adjudicó", tokens)
        self.assertIn("losartán", tokens)
        self.assertIn("daño", tokens)
        self.assertIn("mínimo", tokens)

    # -------------------------------------------------------------------------
    # 2. Pruebas de Cálculo de Métricas Léxicas (calcular_metricas)
    # -------------------------------------------------------------------------
    def test_calcular_metricas_identicas(self):
        """Verifica que dos textos idénticos alcancen precisión, cobertura y F1 de 1.0."""
        texto = "El precio de referencia de Ceftriaxona es 1250 CLP."
        resultado = calcular_metricas(texto, texto)
        self.assertEqual(resultado["precision"], 1.0)
        self.assertEqual(resultado["cobertura"], 1.0)
        self.assertEqual(resultado["f1"], 1.0)

    def test_calcular_metricas_sin_coincidencia(self):
        """Verifica que ante cero intersección léxica, todas las métricas resulten 0.0."""
        ref = "Paracetamol 500 mg comprimidos orales"
        resp = "Insumos quirúrgicos gasas estériles"
        resultado = calcular_metricas(ref, resp)
        self.assertEqual(resultado["precision"], 0.0)
        self.assertEqual(resultado["cobertura"], 0.0)
        self.assertEqual(resultado["f1"], 0.0)

    def test_calcular_metricas_con_respuesta_o_referencia_vacia(self):
        """Verifica robustez ante entradas vacías o compuestas de solo signos."""
        resultado = calcular_metricas("Referencia válida", "")
        self.assertEqual(resultado["precision"], 0.0)
        self.assertEqual(resultado["cobertura"], 0.0)
        self.assertEqual(resultado["f1"], 0.0)

        resultado2 = calcular_metricas("???", "Respuesta válida")
        self.assertEqual(resultado2["f1"], 0.0)

    def test_calcular_metricas_coincidencia_parcial(self):
        """Verifica el cálculo de precisión, cobertura y F1 ante coincidencia parcial calculable."""
        ref = "paracetamol precio 22 clp"      # 4 tokens
        resp = "paracetamol precio 33 clp oferta" # 5 tokens (comunes: paracetamol, precio, clp -> 3)
        res = calcular_metricas(ref, resp)
        self.assertEqual(res["tokens_comunes"], 3)
        self.assertAlmostEqual(res["precision"], 3 / 5, places=3)
        self.assertAlmostEqual(res["cobertura"], 3 / 4, places=3)
        esperado_f1 = 2 * (0.6 * 0.75) / (0.6 + 0.75)
        self.assertAlmostEqual(res["f1"], round(esperado_f1, 4), places=3)


if __name__ == "__main__":
    unittest.main()
