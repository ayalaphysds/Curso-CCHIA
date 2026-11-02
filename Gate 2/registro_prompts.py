"""
Registro Inmutable y Versionado Criptográfico de Prompts (Bloque 32, U2.7).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Gobernanza de Plantillas de Auditoría

Características:
1. Versionado formal de plantillas de prompts mediante huellas criptográficas SHA-256.
2. Inmutabilidad: Toda alteración en el texto de una plantilla genera un hash unívoco diferente.
3. Trazabilidad: Historial cronológico con autor, fecha, descripción del cambio y versión semántica.
4. Consulta determinista por huella o versión semántica.
"""

import hashlib
import json
import datetime
from typing import Dict, Any, List, Optional


class RegistroDePrompts:
    """
    Gestor de plantillas de prompts con control de versiones criptográfico inmutable.
    """

    def __init__(self):
        # Mapeo: { nombre_prompt: [ { version, hash_sha256, plantilla, fecha, autor, descripcion }, ... ] }
        self._registro: Dict[str, List[Dict[str, Any]]] = {}

    @staticmethod
    def calcular_hash_sha256(texto: str) -> str:
        """Calcula la huella digital SHA-256 del contenido exacto de una plantilla."""
        return hashlib.sha256(texto.strip().encode("utf-8")).hexdigest()

    def registrar_version(
        self,
        nombre: str,
        plantilla: str,
        descripcion: str,
        autor: str = "Auditor CENABAST",
        version_semantica: Optional[str] = None
    ) -> str:
        """
        Registra una nueva versión de una plantilla calculando su huella SHA-256.
        
        Retorna:
            str: Huella digital SHA-256 de 64 caracteres hexadecimales.
        """
        if not nombre or not isinstance(nombre, str):
            raise ValueError("El nombre del prompt no puede estar vacío.")
        if not plantilla or not isinstance(plantilla, str) or not plantilla.strip():
            raise ValueError("La plantilla del prompt no puede estar vacía.")

        huella = self.calcular_hash_sha256(plantilla)

        if nombre not in self._registro:
            self._registro[nombre] = []

        historial = self._registro[nombre]
        num_version = version_semantica or f"v{len(historial) + 1}.0"

        # Verificar si la versión ya existe con idéntico hash (idempotencia)
        for entrada in historial:
            if entrada["hash_sha256"] == huella:
                return huella

        nuevo_registro = {
            "nombre": nombre,
            "version": num_version,
            "hash_sha256": huella,
            "plantilla": plantilla.strip(),
            "descripcion": descripcion,
            "autor": autor,
            "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        historial.append(nuevo_registro)
        return huella

    def obtener_version(self, nombre: str, version: Optional[str] = None, huella: Optional[str] = None) -> Dict[str, Any]:
        """Recupera una versión específica por número de versión, por huella SHA-256 o la más reciente."""
        if nombre not in self._registro or not self._registro[nombre]:
            raise KeyError(f"No existen prompts registrados con el nombre '{nombre}'.")

        historial = self._registro[nombre]

        if huella:
            for entrada in historial:
                if entrada["hash_sha256"] == huella:
                    return entrada
            raise KeyError(f"No se encontró el prompt '{nombre}' con huella SHA-256 '{huella}'.")

        if version:
            for entrada in historial:
                if entrada["version"] == version:
                    return entrada
            raise KeyError(f"No se encontró la versión '{version}' para el prompt '{nombre}'.")

        # Retorna la última registrada por defecto
        return historial[-1]

    def listar_historial(self, nombre: str) -> List[Dict[str, Any]]:
        """Retorna el historial completo de cambios para un prompt dado."""
        if nombre not in self._registro:
            return []
        return list(self._registro[nombre])


# -----------------------------------------------------------------------------
# Instancia Global y Plantillas Estándar de CENABAST
# -----------------------------------------------------------------------------
registro_prompts_cenabast = RegistroDePrompts()

# Registro de la versión 1.0 del prompt de auditoría de sobreprecio
PROMPT_AUDITORIA_V1 = """Eres un auditor técnico de compras públicas hospitalarias de CENABAST.
Evalúa la oferta para el medicamento {farmaco} con precio ofertado de ${precio_ofertado} CLP frente a la mediana histórica de ${precio_referencia} CLP.
Calcula el porcentaje de desviación y emite dictamen formal conforme a las bases de licitación."""

# Registro de la versión 2.0 (incorporando instrucción estricta de citación RAG)
PROMPT_AUDITORIA_V2 = """ERES UN AUDITOR SENIOR DE ADQUISICIONES DE LA CENTRAL DE ABASTECIMIENTO (CENABAST).
Evalúa la oferta para el medicamento {farmaco} cotizado a ${precio_ofertado} CLP considerando el contexto normativo oficial provisto.
REGLAS OBLIGATORIAS:
1. Cita explícitamente el documento fuente que respalda el precio de catálogo [cenabast_catalogo_precios_referencia_2026.md].
2. Si la desviación supera el 15.0%, declara sobreprecio crítico y exige supervisión humana.
3. Emite dictamen estructurado en formato JSON."""

hash_v1 = registro_prompts_cenabast.registrar_version(
    nombre="auditar_sobreprecio_farmaco",
    plantilla=PROMPT_AUDITORIA_V1,
    descripcion="Versión inicial básica de auditoría de precios",
    version_semantica="v1.0"
)

hash_v2 = registro_prompts_cenabast.registrar_version(
    nombre="auditar_sobreprecio_farmaco",
    plantilla=PROMPT_AUDITORIA_V2,
    descripcion="Versión reforzada con citación obligatoria de fuentes y umbrales de supervisión",
    version_semantica="v2.0"
)


if __name__ == "__main__":
    print("=" * 75)
    print("  REGISTRO CRIPTOGRÁFICO DE PROMPTS CENABAST (BLOQUE 32)")
    print("=" * 75)
    historial = registro_prompts_cenabast.listar_historial("auditar_sobreprecio_farmaco")
    for entrada in historial:
        print(f"\n[VERSIÓN {entrada['version']}]")
        print(f"  Huella SHA-256: {entrada['hash_sha256']}")
        print(f"  Descripción:   {entrada['descripcion']}")
        print(f"  Fecha UTC:     {entrada['timestamp_utc']}")
        print(f"  Plantilla (primeros 100 caracteres): \"{entrada['plantilla'][:100]}...\"")
