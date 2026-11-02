"""
Módulo de Indexación Vectorial Persistente (Bloque 24 y 25, U2.5).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Indexación de Documentos Normativos y Catálogo de Precios

Características:
1. Segmentación recursiva mediante RecursiveCharacterTextSplitter (chunk_size=300, chunk_overlap=50).
2. Metadatos consistentes en cada chunk: 'fuente' (nombre de archivo), 'chunk_id', 'titulo'.
3. Persistencia durable en Chroma Vector Store ('indice_gate2/').
4. Prevención estricta de duplicación: verifica 'vectorstore.get()["ids"]' antes de indexar.
5. Soporte dual de Embeddings: DeterministicFakeEmbedding(size=768) para modo offline/mock y
   GoogleGenerativeAIEmbeddings cuando se dispone de credenciales activas.
"""

import os
import glob
from typing import List, Tuple, Optional
from dotenv import load_dotenv

load_dotenv()

from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


def obtener_embeddings(mock: bool = True):
    """
    Retorna la función de embeddings adecuada según la configuración y entorno.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if mock or not api_key or os.getenv("USE_MOCK_LLM", "").lower() in ("true", "1"):
        return DeterministicFakeEmbedding(size=768)

    try:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        return GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)
    except Exception:
        # Fallback de resiliencia si la librería o red no están disponibles
        return DeterministicFakeEmbedding(size=768)


def cargar_documentos_desde_directorio(directorio_data: str) -> List[Document]:
    """
    Lee todos los archivos markdown en el directorio indicado y crea objetos Document con
    metadatos normalizados (incluyendo la clave obligatoria 'fuente').
    """
    patron = os.path.join(directorio_data, "*.md")
    archivos = sorted(glob.glob(patron))
    documentos: List[Document] = []

    for ruta in archivos:
        nombre_archivo = os.path.basename(ruta)
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()

        doc = Document(
            page_content=contenido,
            metadata={
                "fuente": nombre_archivo,
                "source": nombre_archivo,
                "archivo": nombre_archivo,
                "categoria": "cenabast_oficial",
            }
        )
        documentos.append(doc)

    return documentos


def segmentar_documentos(
    documentos: List[Document],
    chunk_size: int = 300,
    chunk_overlap: int = 50
) -> List[Document]:
    """
    Segmenta documentos usando RecursiveCharacterTextSplitter asegurando
    que los metadatos 'fuente' y 'chunk_id' se propaguen íntegros a cada fragmento.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n## ", "\n\n### ", "\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_documents(documentos)
    for i, chunk in enumerate(chunks):
        fuente = chunk.metadata.get("fuente", "documento.md")
        chunk.metadata["chunk_id"] = f"{fuente}_chunk_{i}"
        # Asegurar compatibilidad estricta con cualquier consumidor
        chunk.metadata["fuente"] = fuente
        chunk.metadata["source"] = fuente

    return chunks


def crear_o_cargar_indice(
    directorio_data: Optional[str] = None,
    directorio_indice: str = "indice_gate2",
    collection_name: str = "gate2_cenabast",
    mock: bool = True,
    forzar_reindexar: bool = False
) -> Tuple[Chroma, str]:
    """
    Carga o inicializa la colección persistente en Chroma.
    
    Si el índice ya contiene documentos y no se solicita 'forzar_reindexar',
    se reutiliza directamente sin duplicar fragmentos.
    
    Retorna:
        Tuple:
        - vectorstore (Chroma)
        - estado ("indice_reutilizado" o "indice_creado")
    """
    embeddings = obtener_embeddings(mock=mock)
    os.makedirs(directorio_indice, exist_ok=True)

    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=directorio_indice
    )

    datos_existentes = vectorstore.get()
    tiene_documentos = bool(datos_existentes and datos_existentes.get("ids"))

    if tiene_documentos and not forzar_reindexar:
        return vectorstore, "indice_reutilizado"

    # Si se fuerza reindexar y ya existían, limpiamos
    if forzar_reindexar and tiene_documentos:
        ids_a_borrar = datos_existentes["ids"]
        if ids_a_borrar:
            vectorstore.delete(ids=ids_a_borrar)

    # Si no se pasó directorio_data, intentamos localizar 'Gate 2/data' relativo
    if not directorio_data:
        candidatos = [
            os.path.join(os.path.dirname(__file__), "..", "data"),
            os.path.join(os.getcwd(), "data"),
            os.path.join(os.getcwd(), "Gate 2", "data"),
        ]
        for c in candidatos:
            if os.path.isdir(c):
                directorio_data = os.path.abspath(c)
                break

    if not directorio_data or not os.path.isdir(directorio_data):
        # Crear un corpus base mínimo en caso de ejecución aislada
        documentos_base = [
            Document(
                page_content="Catálogo de Precios Referenciales CENABAST: Paracetamol 500mg tiene precio unitario de $12 CLP por tableta. Amoxicilina 500mg tiene precio de $35 CLP.",
                metadata={"fuente": "cenabast_catalogo_precios_referencia_2026.md"}
            ),
            Document(
                page_content="Protocolo de Adjudicaciones CENABAST: Desviaciones mayores al 20% sobre el precio de referencia requieren autorización expresa de supervisión humana.",
                metadata={"fuente": "cenabast_protocolo_supervision_adjudicaciones.md"}
            ),
        ]
        chunks = segmentar_documentos(documentos_base)
    else:
        documentos = cargar_documentos_desde_directorio(directorio_data)
        chunks = segmentar_documentos(documentos)

    if chunks:
        vectorstore.add_documents(chunks)
        return vectorstore, "indice_creado"

    return vectorstore, "indice_vacio"
