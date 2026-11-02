"""
Indexación del Corpus CENABAST y Persistencia de Embeddings (Bloque 24 y 25, U2.5).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Base Vectorial de Precios y Licitaciones Hospitalarias

Este script:
1. Lee los documentos normativos y de catálogo en 'Gate 2/data/'.
2. Aplica segmentación recursiva (RecursiveCharacterTextSplitter) con chunks y solapamiento.
3. Genera representaciones vectoriales densas (embeddings normalizados).
4. Persiste de manera durable el índice vectorial en disco ('Gate 2/indice_gate2/').
5. Previene la duplicación de documentos en re-indexaciones sucesivas.
"""

import os
import sys
import json
import glob
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_text_splitters import RecursiveCharacterTextSplitter


# -----------------------------------------------------------------------------
# 1. Almacén Vectorial Persistente Local (VectorStore Robusto y Rápido)
# -----------------------------------------------------------------------------
class IndiceVectorialLocal:
    """
    Vector Store persistente en disco basado en JSON/NumPy.
    Almacena documentos, metadatos y vectores densos normalizados, soportando
    búsqueda por similitud de coseno y evitando dependencias externas pesadas.
    """

    def __init__(self, ruta_directorio: str, embedding_dim: int = 768):
        self.ruta_directorio = ruta_directorio
        self.embedding_dim = embedding_dim
        self.ruta_archivo = os.path.join(ruta_directorio, "indice_documentos.json")
        self.ruta_vectores = os.path.join(ruta_directorio, "vectores.npy")
        self.documentos: List[Dict[str, Any]] = []
        self.matriz_vectores: Optional[np.ndarray] = None
        self._cargar_si_existe()

    def _cargar_si_existe(self) -> None:
        """Carga el índice persistido si ya existe en disco."""
        if os.path.exists(self.ruta_archivo) and os.path.exists(self.ruta_vectores):
            try:
                with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                    self.documentos = json.load(f)
                self.matriz_vectores = np.load(self.ruta_vectores)
            except Exception as e:
                print(f"Advertencia al cargar índice existente: {e}. Se creará nuevo.")
                self.documentos = []
                self.matriz_vectores = None

    def cantidad_documentos(self) -> int:
        return len(self.documentos)

    def agregar_documentos(self, docs: List[Document], embeddings_list: List[List[float]]) -> int:
        """Agrega documentos y vectores normalizados al almacén, evitando duplicados."""
        os.makedirs(self.ruta_directorio, exist_ok=True)
        nuevos_docs = []
        nuevos_vectores = []

        ids_existentes = {doc.get("metadata", {}).get("chunk_id") for doc in self.documentos}

        for i, (doc, emb) in enumerate(zip(docs, embeddings_list)):
            chunk_id = doc.metadata.get("chunk_id", f"{doc.metadata.get('source', 'doc')}_{i}")
            if chunk_id in ids_existentes:
                continue

            v = np.array(emb, dtype=np.float32)
            norma = np.linalg.norm(v)
            if norma > 0:
                v = v / norma

            doc_dict = {
                "page_content": doc.page_content,
                "metadata": {**doc.metadata, "chunk_id": chunk_id},
            }
            nuevos_docs.append(doc_dict)
            nuevos_vectores.append(v)
            ids_existentes.add(chunk_id)

        if nuevos_docs:
            if self.matriz_vectores is not None and len(self.matriz_vectores) > 0:
                self.matriz_vectores = np.vstack([self.matriz_vectores, np.array(nuevos_vectores)])
                self.documentos.extend(nuevos_docs)
            else:
                self.matriz_vectores = np.array(nuevos_vectores)
                self.documentos = nuevos_docs

            # Guardar en disco
            with open(self.ruta_archivo, "w", encoding="utf-8") as f:
                json.dump(self.documentos, f, ensure_ascii=False, indent=2)
            np.save(self.ruta_vectores, self.matriz_vectores)

        return len(nuevos_docs)

    def buscar_similitud(self, vector_consulta: List[float], k: int = 3) -> List[Tuple[Document, float]]:
        """Realiza búsqueda por similitud de coseno contra todos los vectores indexados."""
        if self.matriz_vectores is None or len(self.documentos) == 0:
            return []

        q = np.array(vector_consulta, dtype=np.float32)
        norm_q = np.linalg.norm(q)
        if norm_q > 0:
            q = q / norm_q

        # Producto punto sobre vectores unitarios = similitud de coseno
        similitudes = np.dot(self.matriz_vectores, q)
        top_indices = np.argsort(similitudes)[::-1][:k]

        resultados = []
        for idx in top_indices:
            doc_data = self.documentos[idx]
            doc = Document(page_content=doc_data["page_content"], metadata=doc_data["metadata"])
            score = float(similitudes[idx])
            resultados.append((doc, score))
        return resultados


# -----------------------------------------------------------------------------
# 2. Pipeline de Carga, Chunking e Indexación
# -----------------------------------------------------------------------------
def cargar_documentos_corpus(ruta_data: str) -> List[Document]:
    """Carga todos los archivos markdown de datos de CENABAST."""
    patron = os.path.join(ruta_data, "*.md")
    archivos = glob.glob(patron)
    documentos = []

    for archivo in archivos:
        nombre_base = os.path.basename(archivo)
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        doc = Document(
            page_content=contenido,
            metadata={
                "source": nombre_base,
                "ruta_completa": archivo,
                "categoria": "cenabast_oficial",
            }
        )
        documentos.append(doc)

    return documentos


def indexar_corpus(
    directorio_data: Optional[str] = None,
    directorio_indice: Optional[str] = None,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> Dict[str, Any]:
    """
    Función principal de indexación del corpus CENABAST.
    
    Retorna:
        Dict con métricas del proceso (documentos cargados, chunks, persistencia).
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_data = directorio_data or os.path.join(base_dir, "data")
    ruta_indice = directorio_indice or os.path.join(base_dir, "indice_gate2")

    print(f"Iniciando indexación del corpus CENABAST desde: {ruta_data}")
    docs_crudos = cargar_documentos_corpus(ruta_data)
    print(f"✓ Documentos base encontrados: {len(docs_crudos)}")

    # Segmentación recursiva con solapamiento
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " "]
    )
    chunks: List[Document] = []
    for doc in docs_crudos:
        sub_docs = splitter.split_documents([doc])
        for idx, sub_doc in enumerate(sub_docs):
            sub_doc.metadata["chunk_id"] = f"{sub_doc.metadata['source']}_chunk_{idx}"
            chunks.append(sub_doc)

    print(f"✓ Chunks generados con solapamiento: {len(chunks)}")

    # Generación de embeddings densos deterministas (768 dimensiones)
    embedder = DeterministicFakeEmbedding(size=768)
    textos = [c.page_content for c in chunks]
    embeddings = embedder.embed_documents(textos)

    # Persistencia en Vector Store
    indice = IndiceVectorialLocal(ruta_indice, embedding_dim=768)
    agregados = indice.agregar_documentos(chunks, embeddings)

    resumen = {
        "documentos_fuente": len(docs_crudos),
        "total_chunks": len(chunks),
        "nuevos_agregados": agregados,
        "total_persistidos": indice.cantidad_documentos(),
        "directorio_indice": ruta_indice,
        "archivo_indice": indice.ruta_archivo,
        "archivo_vectores": indice.ruta_vectores,
    }
    print(f"✓ Índice vectorial persistido exitosamente en: {ruta_indice}")
    print(f"  Total documentos en colección: {resumen['total_persistidos']}")
    return resumen


if __name__ == "__main__":
    from typing import Tuple
    res = indexar_corpus()
