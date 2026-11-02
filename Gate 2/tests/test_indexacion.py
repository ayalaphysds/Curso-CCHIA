"""
Pruebas Unitarias de Indexación y Segmentación Vectorial (Gate 2).
Especialización en IA Accenture - Curso CCHIA
"""

import os
import sys
import pytest
from langchain_core.documents import Document

directorio_gate2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if directorio_gate2 not in sys.path:
    sys.path.insert(0, directorio_gate2)

from src.indexador import (
    cargar_documentos_desde_directorio,
    segmentar_documentos,
    obtener_embeddings,
    crear_o_cargar_indice,
)


class TestIndexacionGate2:
    """Pruebas del módulo de indexación vectorial para el corpus de CENABAST."""

    @pytest.fixture
    def ruta_data(self):
        return os.path.join(directorio_gate2, "data")

    def test_cargar_documentos_desde_directorio(self, ruta_data):
        docs = cargar_documentos_desde_directorio(ruta_data)
        assert len(docs) >= 5, "El corpus debe contener al menos 5 documentos normativos"
        for doc in docs:
            assert "fuente" in doc.metadata, "Cada documento debe tener la clave de metadatos 'fuente'"
            assert doc.metadata["fuente"].endswith(".md"), "La fuente debe ser un archivo markdown"
            assert len(doc.page_content.strip()) > 50, "El contenido del documento no debe estar vacío"

    def test_segmentar_documentos_preserva_fuente_y_asigna_chunk_id(self):
        docs = [
            Document(
                page_content="Licitación de medicamentos hospitalarios. " * 30,
                metadata={"fuente": "bases_cenabast.md"}
            )
        ]
        chunks = segmentar_documentos(docs, chunk_size=150, chunk_overlap=30)
        assert len(chunks) > 1, "El splitter debe fragmentar el documento largo"
        for i, chunk in enumerate(chunks):
            assert chunk.metadata["fuente"] == "bases_cenabast.md"
            assert f"chunk_{i}" in chunk.metadata["chunk_id"]

    def test_obtener_embeddings_mock_retorna_deterministic_embedding(self):
        embeddings = obtener_embeddings(mock=True)
        assert embeddings is not None
        vector = embeddings.embed_query("Prueba de vector")
        assert len(vector) == 768, "El vector mock debe tener dimensión 768"

    def test_crear_o_cargar_indice_reutilizacion_sin_duplicados(self, tmp_path, ruta_data):
        indice_tmp = str(tmp_path / "indice_test")
        
        # Primera creación: debe crear el índice
        vs1, estado1 = crear_o_cargar_indice(
            directorio_data=ruta_data,
            directorio_indice=indice_tmp,
            collection_name="col_test_1",
            mock=True
        )
        assert estado1 == "indice_creado"
        total_1 = len(vs1.get()["ids"])
        assert total_1 > 0

        # Segunda carga: debe reutilizar el índice sin duplicar fragmentos
        vs2, estado2 = crear_o_cargar_indice(
            directorio_data=ruta_data,
            directorio_indice=indice_tmp,
            collection_name="col_test_1",
            mock=True
        )
        assert estado2 == "indice_reutilizado"
        total_2 = len(vs2.get()["ids"])
        assert total_1 == total_2, "La reutilización del índice no debe duplicar documentos"
