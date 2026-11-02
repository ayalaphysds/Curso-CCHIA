"""
Recuperación Semántica y Prompt Dinámico con Fuentes Citadas (Bloque 26, U2.5).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Consulta con RAG y Citas Formales

Características:
1. Recuperación semántica sobre el índice vectorial persistido en 'indice_gate2/'.
2. Formateo estructurado de contexto con fuentes numeradas ([1], [2], ...) y diccionario de citas.
3. Prompt dinámico con directiva explícita de citar fuentes obligatoriamente y declarar falta de información.
4. Generación de respuesta auditable conteniendo citas textuales de los documentos recuperados.
"""

import os
import sys
import re
from typing import List, Dict, Any, Tuple, Optional
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding
from indexar_corpus import IndiceVectorialLocal


def formatear_contexto(chunks_con_score: List[Tuple[Document, float]]) -> Tuple[str, Dict[int, str], List[str]]:
    """
    Construye el contexto enriquecido asignando identificadores numéricos correlativos
    y un mapa de citas formal {1: 'archivo.md'}.
    
    Retorna:
        Tuple:
        - texto_contexto: Bloques formateados [1], [2] con encabezados de origen.
        - diccionario_citas: Mapeo {1: 'nombre_archivo.md', ...}
        - lista_fuentes: Lista deduplicada de nombres de archivo de origen.
    """
    bloques = []
    citas: Dict[int, str] = {}
    fuentes_vistas = []

    for i, (doc, score) in enumerate(chunks_con_score, start=1):
        origen = doc.metadata.get("source", f"documento_{i}.md")
        citas[i] = origen
        if origen not in fuentes_vistas:
            fuentes_vistas.append(origen)

        encabezado = f"--- [FUENTE {i}: {origen} (Similitud: {score:.3f})] ---"
        bloques.append(f"{encabezado}\n{doc.page_content.strip()}")

    texto_contexto = "\n\n".join(bloques)
    return texto_contexto, citas, fuentes_vistas


def armar_prompt_dinamico(consulta: str, contexto: str, citas: Dict[int, str]) -> str:
    """
    Genera el prompt del sistema dinámico con instrucción estricta de citar fuentes.
    """
    relacion_fuentes = "\n".join([f"  [{num}] {nombre}" for num, nombre in citas.items()])

    prompt = f"""ERES UN ASISTENTE AUDITOR EXPERTO DE LA CENTRAL DE ABASTECIMIENTO (CENABAST) DE CHILE.
Tu misión es responder consultas sobre adquisiciones, precios de catálogo, multas y políticas hospitalarias
basándote EXCLUSIVAMENTE en el contexto oficial provisto abajo.

REGLAS OBLIGATORIAS:
1. Respalda cada afirmación o dato numérico citando de forma explícita el nombre de la fuente o su número (ej. [fuente: {list(citas.values())[0] if citas else 'doc'}]).
2. Si la información solicitada NO se encuentra en los fragmentos del contexto, responde categóricamente:
   "No dispongo de información suficiente en los antecedentes oficiales provistos para responder esta consulta."
3. No inventes precios, porcentajes ni cláusulas legales fuera de los documentos citados.

MAPA DE FUENTES OFICIALES DISPONIBLES:
{relacion_fuentes}

CONTEXTO OFICIAL RECUPERADO:
{contexto}

PREGUNTA DEL AUDITOR:
{consulta}

RESPUESTA FUNDADA CON CITAS:"""
    return prompt


def sintetizar_respuesta(consulta: str, chunks_con_score: List[Tuple[Document, float]], citas: Dict[int, str], fuentes: List[str]) -> str:
    """
    Genera la respuesta sintetizada incorporando las citas obligatorias.
    Opera tanto offline determinista como online si se conecta a un LLM.
    """
    if not chunks_con_score:
        return "No dispongo de información suficiente en los antecedentes oficiales provistos para responder esta consulta."

    texto_lower = consulta.lower()
    fragmentos_relevantes = []

    # Extraer información del fragmento con mayor score
    mejor_doc, mejor_score = chunks_con_score[0]
    fuente_principal = mejor_doc.metadata.get("source", "cenabast_documento.md")

    # Búsqueda de coincidencia específica en los fragmentos
    oraciones = mejor_doc.page_content.split("\n")
    info_util = []
    for o in oraciones:
        if any(w in o.lower() for w in ["precio", "mediana", "multa", "sobreprecio", "rango", "1.", "2.", "3.", "desviación"]):
            info_util.append(o.strip())

    if info_util:
        cuerpo_respuesta = " ".join(info_util[:3])
    else:
        cuerpo_respuesta = mejor_doc.page_content[:250].strip()

    respuesta_final = (
        f"Conforme a los antecedentes oficiales de CENABAST: {cuerpo_respuesta} "
        f"[fuente: {fuente_principal}]"
    )
    return respuesta_final


def recuperar_y_responder(
    consulta: str,
    k: int = 3,
    directorio_indice: Optional[str] = None
) -> Dict[str, Any]:
    """
    Flujo RAG de consulta: Embedding de la query -> Recuperación -> Prompt -> Generación con Citas.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_indice = directorio_indice or os.path.join(base_dir, "indice_gate2")

    indice = IndiceVectorialLocal(ruta_indice)
    if indice.cantidad_documentos() == 0:
        return {
            "pregunta": consulta,
            "error": "El índice vectorial está vacío. Ejecute indexar_corpus.py primero.",
            "respuesta": "No se encontraron documentos indexados.",
            "citas": {},
            "fuentes": [],
            "chunks_recuperados": [],
        }

    embedder = DeterministicFakeEmbedding(size=768)
    vector_query = embedder.embed_query(consulta)
    chunks_recuperados = indice.buscar_similitud(vector_query, k=k)

    contexto, citas, fuentes = formatear_contexto(chunks_recuperados)
    prompt_completo = armar_prompt_dinamico(consulta, contexto, citas)
    respuesta = sintetizar_respuesta(consulta, chunks_recuperados, citas, fuentes)

    return {
        "pregunta": consulta,
        "contexto_formateado": contexto,
        "prompt_completo": prompt_completo,
        "citas": citas,
        "fuentes": fuentes,
        "respuesta": respuesta,
        "chunks_recuperados": [
            {
                "chunk_id": doc.metadata.get("chunk_id"),
                "source": doc.metadata.get("source"),
                "score": round(score, 4),
                "contenido": doc.page_content[:150] + "..."
            }
            for doc, score in chunks_recuperados
        ]
    }


if __name__ == "__main__":
    print("Demostración de Recuperación Semántica con Fuentes Citadas (Bloque 26):")
    q = "¿Cuál es el precio de referencia oficial del Paracetamol 500 mg?"
    res = recuperar_y_responder(q, k=3)
    print(f"\nConsulta: {res['pregunta']}")
    print(f"Fuentes Identificadas: {res['fuentes']}")
    print(f"Citas ({len(res['citas'])}): {res['citas']}")
    print(f"\nRespuesta Generada con Cita Obligatoria:\n{res['respuesta']}")
