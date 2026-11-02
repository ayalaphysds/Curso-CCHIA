"""
Módulo de Recuperación Semántica, Filtrado y Citación de Fuentes (Bloques 26 y 27, U2.5).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Recuperación Auditable con Citas Textuales

Características:
1. Recuperación vectorial por similitud con k configurable (por defecto k=3).
2. Conexión directa con el filtro anti-inyección de 'src.seguridad' sobre 'page_content'.
3. Formateo estructurado del contexto con etiquetas explícitas '[fuente: <archivo>]'.
4. Manejo riguroso de contexto vacío o totalmente descartado (criterio no compensable).
"""

from typing import List, Tuple, Dict, Any, Optional
from langchain_core.documents import Document
from src.seguridad import filtrar_documentos_sospechosos

RESPUESTA_SIN_CONTEXTO = "No tengo informacion suficiente y verificada para responder esto."


import re
import unicodedata


def normalizar_texto(texto: str) -> str:
    """Normaliza texto a minúsculas y sin acentos ni diacríticos para comparación robusta."""
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "en", "para",
    "por", "con", "sin", "sobre", "entre", "hacia", "hasta",
    "cual", "cuál", "cuales", "cuáles", "como", "cómo", "que", "qué",
    "quien", "quién", "quienes", "quiénes", "donde", "dónde", "cuando", "cuándo",
    "porque", "porqué", "este", "esta", "estos", "estas", "ese", "esa", "esos", "esas",
    "aquel", "aquella", "tiene", "tienen", "son", "es", "hay", "era", "ser",
    "segun", "según", "todo", "toda", "todos", "todas", "otro", "otra", "otros", "otras",
    "mas", "más", "menos", "muy", "mucho", "mucha", "muchos", "muchas",
    "favor", "indicar", "indica", "informar", "informa", "saber", "conocer", "decir", "dime",
    "correo", "email", "usuario", "auditoria", "auditoría", "urgente"
}
STOPWORDS_NORM = {normalizar_texto(w) for w in STOPWORDS}

PALABRAS_GENERICAS = {
    "precio", "precios", "valor", "valores", "referencia", "referencial", "referenciales",
    "catalogo", "catálogo", "bases", "licitacion", "licitación", "licitaciones",
    "compra", "compras", "adquisicion", "adquisición", "adquisiciones",
    "cenabast", "institucional", "oficial", "nacional", "sistema", "ano", "año", "2026",
    "registro", "registros", "informacion", "información", "documento", "documentos",
    # Formas farmacéuticas y unidades
    "comprimido", "comprimidos", "tableta", "tabletas", "capsula", "cápsula", "capsulas", "cápsulas",
    "ampolla", "ampollas", "frasco", "frascos", "suspension", "suspensión", "dosis", "unidad", "unidades",
    "mg", "g", "ml", "ui",
    # Términos administrativos y de licitación
    "costo", "costos", "unitario", "unitaria", "unitarios", "unitarias",
    "estimado", "estimada", "estimados", "estimadas",
    "especificaciones", "tecnica", "técnica", "tecnicas", "técnicas", "tecnico", "técnico", "tecnicos", "técnicos",
    "adquirir", "central", "chile", "salud",
    # Términos generales adicionales
    "vuelo", "vuelos", "comercial", "comerciales"
}
PALABRAS_GENERICAS_NORM = {normalizar_texto(w) for w in PALABRAS_GENERICAS}


def calcular_relevancia_lexica(texto: str, palabras_clave: List[str]) -> float:
    """Calcula un score de relevancia léxica ponderado por coincidencias exactas y lematizadas."""
    if not palabras_clave:
        return 0.0
    texto_norm = normalizar_texto(texto)
    score = 0.0
    for p in palabras_clave:
        p_norm = normalizar_texto(p)
        if not p_norm:
            continue
        coincide = p_norm in texto_norm
        if not coincide and len(p_norm) > 4:
            if p_norm.endswith("es"):
                coincide = p_norm[:-2] in texto_norm
            elif p_norm.endswith("s"):
                coincide = p_norm[:-1] in texto_norm

        if coincide:
            # Ponderación mayor para nombres de fármacos y términos clave de compras
            if p_norm in ("paracetamol", "amoxicilina", "insulina", "ceftriaxona", "losartan", "multa", "sobreprecio", "catalogo", "bases", "politica"):
                score += 5.0
            else:
                score += 1.0
            # Bonificación adicional si aparece como palabra completa
            if re.search(r"\b" + re.escape(p_norm) + r"\b", texto_norm):
                score += 2.0
    return score


def recuperar_documentos(vectorstore, pregunta: str, k: int = 3) -> List[Document]:
    """
    Realiza recuperación híbrida (similitud vectorial + scoring léxico de dominio CENABAST).
    Garantiza que consultas con nombres específicos de fármacos o normativas recuperen
    los fragmentos de catálogo y bases correspondientes, y descarta candidatos cuando la consulta
    carece de relevancia léxica o temática respecto al corpus oficial.
    """
    if not pregunta or not str(pregunta).strip():
        return []

    pregunta_norm = normalizar_texto(pregunta)
    tokens = [w for w in re.findall(r"\w+", pregunta_norm) if len(w) > 2]
    palabras_pregunta = [w for w in tokens if w not in STOPWORDS_NORM]

    if not palabras_pregunta:
        return []

    terminos_sustantivos = [
        w for w in palabras_pregunta
        if w not in PALABRAS_GENERICAS_NORM and not w.isdigit()
    ]

    candidatos: List[Document] = []
    
    # Intentar obtener candidatos desde el vectorstore
    if hasattr(vectorstore, "similarity_search"):
        try:
            candidatos = vectorstore.similarity_search(pregunta, k=max(k * 3, 10))
        except Exception:
            candidatos = []
    elif hasattr(vectorstore, "as_retriever"):
        try:
            retriever = vectorstore.as_retriever(search_kwargs={"k": max(k * 3, 10)})
            candidatos = retriever.invoke(pregunta)
        except Exception:
            candidatos = []

    # Si el vectorstore tiene método get(), también inspeccionar los chunks almacenados para rescate léxico
    if hasattr(vectorstore, "get"):
        try:
            datos = vectorstore.get()
            docs_data = datos.get("documents", [])
            metas_data = datos.get("metadatas", [])
            ids_vistos = {d.metadata.get("chunk_id", getattr(d, "page_content", "")) for d in candidatos}

            for doc_text, meta in zip(docs_data, metas_data):
                cid = meta.get("chunk_id", doc_text[:50])
                if cid not in ids_vistos:
                    doc_norm = normalizar_texto(doc_text)
                    tokens_buscar = terminos_sustantivos if terminos_sustantivos else palabras_pregunta
                    if any(re.search(r"\b" + re.escape(p) + r"\b", doc_norm) for p in tokens_buscar):
                        candidatos.append(Document(page_content=doc_text, metadata=meta))
                        ids_vistos.add(cid)
        except Exception:
            pass

    if not candidatos:
        return []

    # Validar relevancia de los candidatos frente a la consulta
    if terminos_sustantivos:
        # Si la consulta contiene términos sustantivos (ej. repuestos, automotrices, Francia, Ibuprofeno),
        # al menos un término sustantivo debe coincidir en el contenido o en el nombre de la fuente.
        candidatos_relevantes = []
        for doc in candidatos:
            doc_norm = normalizar_texto(doc.page_content)
            fuente_norm = normalizar_texto(doc.metadata.get("fuente", "") or doc.metadata.get("source", ""))
            
            tiene_match = False
            for t in terminos_sustantivos:
                patron_palabra = re.compile(r"\b" + re.escape(t) + r"\b")
                if patron_palabra.search(doc_norm) or patron_palabra.search(fuente_norm):
                    tiene_match = True
                    break
                if len(t) > 4:
                    t_sing = None
                    if t.endswith("es"):
                        t_sing = t[:-2]
                    elif t.endswith("s"):
                        t_sing = t[:-1]
                    if t_sing:
                        patron_sing = re.compile(r"\b" + re.escape(t_sing) + r"\b")
                        if patron_sing.search(doc_norm) or patron_sing.search(fuente_norm):
                            tiene_match = True
                            break
            if tiene_match:
                candidatos_relevantes.append(doc)

        candidatos = candidatos_relevantes

        # Si ningún documento del corpus tiene relevancia léxica/temática con los términos sustantivos,
        # la consulta está fuera del corpus -> descartar y retornar []
        if not candidatos:
            return []
    else:
        # Si la consulta solo contiene palabras genéricas del dominio, verificar relevancia léxica mínima
        candidatos = [
            doc for doc in candidatos
            if calcular_relevancia_lexica(doc.page_content, palabras_pregunta) > 0.0 or
               any(p in normalizar_texto(doc.metadata.get("fuente", "")) for p in palabras_pregunta)
        ]
        if not candidatos:
            return []

    # Reordenar candidatos por relevancia híbrida
    def key_sort(doc: Document) -> Tuple[float, int]:
        score_lexico = calcular_relevancia_lexica(doc.page_content, palabras_pregunta)
        fuente = normalizar_texto(doc.metadata.get("fuente") or "")
        if any(p in fuente for p in palabras_pregunta):
            score_lexico += 3.0
        return (score_lexico, len(doc.page_content))

    candidatos.sort(key=key_sort, reverse=True)

    return candidatos[:k]



def formatear_contexto(documentos: List[Document]) -> str:
    """
    Construye el bloque de contexto inyectable en el prompt, agregando
    la etiqueta estricta de citación documental: [fuente: <nombre_archivo>].
    """
    bloques = []
    for doc in documentos:
        fuente = doc.metadata.get("fuente") or doc.metadata.get("source") or "documento_cenabast.md"
        bloques.append(f"[fuente: {fuente}]\n{doc.page_content.strip()}")
    return "\n\n".join(bloques)


def extraer_lista_fuentes(documentos: List[Document]) -> List[str]:
    """
    Extrae la lista ordenada y unívoca de fuentes presentes en los documentos validados.
    """
    fuentes = set()
    for doc in documentos:
        f = doc.metadata.get("fuente") or doc.metadata.get("source")
        if f:
            fuentes.add(f)
    return sorted(list(fuentes))


def recuperar_y_procesar(
    vectorstore,
    pregunta: str,
    k: int = 3
) -> Tuple[List[Document], List[Document], str, List[str]]:
    """
    Orquesta la recuperación semántica, el filtrado de seguridad y el formateo de contexto.
    
    Retorna:
        Tuple:
        - limpios (List[Document]): Chunks validados.
        - descartados (List[Document]): Chunks sospechosos o con inyección.
        - contexto_formateado (str): Contexto con etiquetas '[fuente: ...]' o vacío.
        - fuentes (List[str]): Lista de nombres de archivos fuente válidos.
    """
    recuperados = recuperar_documentos(vectorstore, pregunta, k=k)
    limpios, descartados = filtrar_documentos_sospechosos(recuperados)

    if not limpios:
        return [], descartados, "", []

    contexto = formatear_contexto(limpios)
    fuentes = extraer_lista_fuentes(limpios)

    return limpios, descartados, contexto, fuentes


def armar_prompt_rag(pregunta: str, contexto: str, fuentes: List[str]) -> str:
    """
    Construye el prompt completo para el modelo de lenguaje, con instrucción
    estricta de citar la fuente con la sintaxis '[fuente: <nombre_archivo>]'.
    """
    relacion_fuentes = ", ".join(fuentes) if fuentes else "ninguna"

    prompt = f"""ERES UN ASISTENTE AUDITOR EXPERTO DE ADQUISICIONES DE CENABAST (CHILE).
Tu objetivo es responder la consulta del usuario basándote EXCLUSIVAMENTE en el contexto oficial recuperado.

REGLAS DE ORO OBLIGATORIAS:
1. CITA OBLIGATORIAMENTE la fuente de donde obtienes cada dato o precio utilizando la sintaxis exacta: [fuente: <nombre_archivo>].
2. Si la información solicitada NO está presente en el contexto provisto, responde EXACTAMENTE:
   "{RESPUESTA_SIN_CONTEXTO}"
3. NO inventes cifras, multas ni especificaciones técnicas no respaldadas en el contexto.

FUENTES DOCUMENTALES RECUPERADAS: {relacion_fuentes}

CONTEXTO OFICIAL:
{contexto}

PREGUNTA DEL AUDITOR:
{pregunta}

RESPUESTA AUDITADA (INCLUYENDO CITA [fuente: <archivo>]):"""
    return prompt
