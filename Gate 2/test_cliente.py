"""
Suite de Pruebas Unitarias para el Cliente Modular de Consumo de APIs (Bloque 14, U2.1).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Auditoría de Adquisiciones Hospitalarias

Criterios Verificados (100% Offline, sin consumo de red ni saldo API):
1. Clasificación estricta de códigos HTTP en enviar_peticion (401/403/400 -> ValueError; 429/500 -> TimeoutError).
2. Lógica de política de reintentos con con_reintento (backoff, recuperación y límite de intentos).
3. Ausencia total de reintentos ante errores de autenticación o sintaxis (ValueError).
4. Acumulación correcta del costo por tokens (registrar_costo) y aislamiento entre pruebas (auto-reset).
5. Encapsulación y transformación de TimeoutError a RuntimeError informativo en consultar_modelo.
"""

import unittest
from unittest.mock import patch, MagicMock
import requests

from cliente import (
    consultar_modelo,
    registrar_costo,
    reiniciar_costo,
    obtener_costo_total,
    costo_total_sesion,
)
from cliente_api import (
    armar_peticion,
    enviar_peticion,
    extraer_texto,
)
from cliente_reintento import con_reintento


class TestClienteModularCENABAST(unittest.TestCase):
    """Pruebas unitarias de robustez, resiliencia y contabilidad de costos del cliente API."""

    def setUp(self):
        """Fixture ejecutado antes de cada prueba para garantizar estado limpio y reproducible."""
        reiniciar_costo()

    def tearDown(self):
        """Limpieza posterior a la prueba."""
        reiniciar_costo()

    # -------------------------------------------------------------------------
    # 1. Pruebas de Clasificación Temprana de Errores HTTP en enviar_peticion
    # -------------------------------------------------------------------------
    @patch("requests.post")
    def test_enviar_peticion_clasifica_401_403_como_value_error(self, mock_post):
        """Verifica que respuestas 401 y 403 se clasifiquen como ValueError para no reintentar."""
        mock_resp_401 = MagicMock()
        mock_resp_401.status_code = 401
        mock_resp_401.text = "Unauthorized: Invalid API Key"
        mock_post.return_value = mock_resp_401

        cuerpo = {"contents": [{"parts": [{"text": "Consulta CENABAST"}]}]}
        with self.assertRaises(ValueError) as ctx:
            enviar_peticion(cuerpo)
        self.assertIn("Credencial inválida", str(ctx.exception))

        mock_resp_403 = MagicMock()
        mock_resp_403.status_code = 403
        mock_resp_403.text = "Forbidden: Insufficient quota or access blocked"
        mock_post.return_value = mock_resp_403

        with self.assertRaises(ValueError) as ctx:
            enviar_peticion(cuerpo)
        self.assertIn("Credencial inválida", str(ctx.exception))

    @patch("requests.post")
    def test_enviar_peticion_clasifica_400_api_key_invalid_como_value_error(self, mock_post):
        """Verifica que el error 400 con motivo API_KEY_INVALID lance ValueError inmediatamente."""
        mock_resp_400 = MagicMock()
        mock_resp_400.status_code = 400
        mock_resp_400.text = '{"error": {"status": "INVALID_ARGUMENT", "message": "API key not valid. Please pass a valid API key."}}'
        mock_post.return_value = mock_resp_400

        cuerpo = {"contents": [{"parts": [{"text": "Consulta de licitación"}]}]}
        with self.assertRaises(ValueError) as ctx:
            enviar_peticion(cuerpo)
        self.assertIn("Credencial inválida", str(ctx.exception))

    @patch("requests.post")
    def test_enviar_peticion_clasifica_429_como_timeout_error(self, mock_post):
        """Verifica que 429 (Rate Limit / Quota) se clasifique como TimeoutError para habilitar reintentos."""
        mock_resp_429 = MagicMock()
        mock_resp_429.status_code = 429
        mock_resp_429.text = "Resource has been exhausted (e.g. check quota)."
        mock_post.return_value = mock_resp_429

        cuerpo = {"contents": [{"parts": [{"text": "¿Cuál es el precio de referencia del Paracetamol?"}]}]}
        with self.assertRaises(TimeoutError) as ctx:
            enviar_peticion(cuerpo)
        self.assertIn("El proveedor no pudo procesar la petición", str(ctx.exception))

    @patch("requests.post")
    def test_enviar_peticion_clasifica_500_y_falla_de_red_como_timeout_error(self, mock_post):
        """Verifica que errores 500 y excepciones de red de requests se clasifiquen como TimeoutError."""
        # Escenario 500
        mock_resp_500 = MagicMock()
        mock_resp_500.status_code = 500
        mock_resp_500.text = "Internal Server Error"
        mock_post.return_value = mock_resp_500

        cuerpo = {"contents": [{"parts": [{"text": "Verificación 500"}]}]}
        with self.assertRaises(TimeoutError):
            enviar_peticion(cuerpo)

        # Escenario excepción de red Timeout
        mock_post.side_effect = requests.exceptions.Timeout("Connection timed out")
        with self.assertRaises(TimeoutError) as ctx:
            enviar_peticion(cuerpo)
        self.assertIn("No se pudo contactar al proveedor", str(ctx.exception))

    # -------------------------------------------------------------------------
    # 2. Pruebas de la Política de Reintentos con_reintento
    # -------------------------------------------------------------------------
    @patch("time.sleep")
    def test_con_reintento_reintenta_y_recupera_exito(self, mock_sleep):
        """Verifica que con_reintento espere y reintente cuando falla inicialmente pero luego tiene éxito."""
        llamadas = [0]

        def servicio_intermitente():
            llamadas[0] += 1
            if llamadas[0] < 3:
                raise TimeoutError("Congestión momentánea 429")
            return {"candidates": [{"content": {"parts": [{"text": "Precio de Losartán: $18.50 CLP"}]}}]}

        resultado = con_reintento(servicio_intermitente, intentos=3, espera_segundos=1)
        self.assertEqual(llamadas[0], 3)
        self.assertEqual(mock_sleep.call_count, 2)
        self.assertIn("candidates", resultado)

    @patch("time.sleep")
    def test_con_reintento_agota_reintentos_y_propaga_timeout_error(self, mock_sleep):
        """Verifica que con_reintento agote exactamente el número de intentos configurados y lance TimeoutError."""
        llamadas = [0]

        def servicio_caido():
            llamadas[0] += 1
            raise TimeoutError("Servicio no disponible")

        with self.assertRaises(TimeoutError):
            con_reintento(servicio_caido, intentos=4, espera_segundos=1)

        self.assertEqual(llamadas[0], 4)
        self.assertEqual(mock_sleep.call_count, 3)

    def test_con_reintento_no_reintenta_ante_value_error(self):
        """Verifica que ante un ValueError (auth/sintaxis), la función falle inmediatamente en el intento 1."""
        llamadas = [0]

        def servicio_credencial_invalida():
            llamadas[0] += 1
            raise ValueError("Credencial inválida")

        with self.assertRaises(ValueError):
            con_reintento(servicio_credencial_invalida, intentos=5, espera_segundos=1)

        # Debe haberse llamado exactamente UNA vez (cero reintentos)
        self.assertEqual(llamadas[0], 1)

    # -------------------------------------------------------------------------
    # 3. Pruebas de Registro y Acumulación de Costos (Bloque 13 / 14)
    # -------------------------------------------------------------------------
    def test_registrar_costo_acumula_correctamente_y_resetea(self):
        """Verifica el cálculo de costo por tokens consumidos, la acumulación y el reseteo de sesión."""
        self.assertEqual(obtener_costo_total(), 0.0)

        # Simular llamada 1: 500 tokens
        resp_1 = {"usageMetadata": {"totalTokenCount": 500}}
        costo_1 = registrar_costo(resp_1, costo_por_token=0.000002)
        self.assertAlmostEqual(costo_1, 0.001)
        self.assertAlmostEqual(obtener_costo_total(), 0.001)

        # Simular llamada 2: 1500 tokens
        resp_2 = {"usageMetadata": {"totalTokenCount": 1500}}
        costo_2 = registrar_costo(resp_2, costo_por_token=0.000002)
        self.assertAlmostEqual(costo_2, 0.003)
        self.assertAlmostEqual(obtener_costo_total(), 0.004)

        # Resetear sesión y verificar retorno a 0.0
        reiniciar_costo()
        self.assertEqual(obtener_costo_total(), 0.0)

    # -------------------------------------------------------------------------
    # 4. Pruebas de consultar_modelo y Encapsulación a RuntimeError
    # -------------------------------------------------------------------------
    @patch("cliente.con_reintento")
    def test_consultar_modelo_convierte_agotamiento_en_runtime_error(self, mock_con_reintento):
        """Verifica que el agotamiento de reintentos sea traducido a RuntimeError con mensaje amigable."""
        mock_con_reintento.side_effect = TimeoutError("Tiempo agotado")

        with self.assertRaises(RuntimeError) as ctx:
            consultar_modelo("¿Cuál es la mediana histórica de Ceftriaxona?")
        self.assertIn("El servicio no respondió tras varios intentos", str(ctx.exception))

    def test_consultar_modelo_propaga_value_error_directamente(self):
        """Verifica que consultas con preguntas vacías lancen ValueError sin intentar invocar la red."""
        with self.assertRaises(ValueError) as ctx:
            consultar_modelo("   ")
        self.assertIn("La pregunta no puede estar vacía", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
