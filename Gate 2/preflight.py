"""
Script de Validación Preflight del Repositorio y del Índice Vectorial (Bloque 28, U2.5).
Especialización en IA Accenture - Curso CCHIA
Caso de Negocio: CENABAST - Auditoría Pre-Despliegue

Verificaciones Realizadas:
1. Existencia y persistencia efectiva del índice vectorial en disco (Gate 2/indice_gate2/).
2. Verificación de reglas de seguridad en .gitignore (.env e índices excluidos de control de versiones).
3. Integridad del corpus documental de referencia (Gate 2/data/ con al menos 5 archivos .md).
4. Disponibilidad de dependencias esenciales en el entorno de ejecución.
"""

import os
import sys
import json
import glob

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def verificar_indice_persistido(ruta_indice: str) -> bool:
    """Verifica que el índice vectorial exista en disco con documentos y vectores."""
    if not os.path.isdir(ruta_indice):
        print(f"✗ ERROR: Directorio de índice no encontrado en: {ruta_indice}")
        return False

    archivo_docs = os.path.join(ruta_indice, "indice_documentos.json")
    archivo_vectores = os.path.join(ruta_indice, "vectores.npy")

    if not os.path.isfile(archivo_docs) or not os.path.isfile(archivo_vectores):
        print("✗ ERROR: Faltan archivos del vector store (indice_documentos.json o vectores.npy)")
        return False

    try:
        with open(archivo_docs, "r", encoding="utf-8") as f:
            docs = json.load(f)
        if len(docs) == 0:
            print("✗ ERROR: El índice de documentos está vacío (0 registros).")
            return False
        print(f"✓ Índice vectorial persistido verificado ({len(docs)} chunks en disco).")
        return True
    except Exception as e:
        print(f"✗ ERROR al leer índice: {e}")
        return False


def verificar_gitignore(ruta_gitignore: str) -> bool:
    """Verifica que .gitignore incluya la protección de secretos y almacenamiento vectorial."""
    if not os.path.isfile(ruta_gitignore):
        print(f"✗ ADVERTENCIA: No se encontró .gitignore en: {ruta_gitignore}")
        return False

    with open(ruta_gitignore, "r", encoding="utf-8") as f:
        contenido = f.read()

    reglas_criticas = [".env", "indice_gate2", "vectorstore"]
    todas_ok = True
    for regla in reglas_criticas:
        if regla not in contenido:
            print(f"✗ ADVERTENCIA: Falta regla '{regla}' en .gitignore")
            todas_ok = False
        else:
            print(f"✓ Regla de exclusión '{regla}' presente en .gitignore")
    return todas_ok


def verificar_corpus(ruta_data: str) -> bool:
    """Verifica que el corpus CENABAST cuente con los documentos requeridos."""
    if not os.path.isdir(ruta_data):
        print(f"✗ ERROR: Carpeta de datos no encontrada: {ruta_data}")
        return False

    archivos = glob.glob(os.path.join(ruta_data, "*.md"))
    if len(archivos) < 5:
        print(f"✗ ERROR: Corpus insuficiente. Se encontraron {len(archivos)} archivos, se requieren al menos 5.")
        return False

    print(f"✓ Corpus de referencia verificado ({len(archivos)} documentos markdown en data/).")
    return True


def verificar_librerias() -> bool:
    """Verifica disponibilidad de librerías del core."""
    librerias = ["langchain_core", "langgraph", "numpy", "pytest"]
    todas = True
    for lib in librerias:
        try:
            __import__(lib)
            print(f"✓ Paquete instalado: {lib}")
        except ImportError:
            print(f"✗ Paquete faltante: {lib}")
            todas = False
    return todas


def ejecutar_preflight() -> int:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(base_dir)

    ruta_indice = os.path.join(base_dir, "indice_gate2")
    ruta_data = os.path.join(base_dir, "data")
    ruta_gitignore = os.path.join(repo_root, ".gitignore")

    print("=" * 70)
    print("  VERIFICACIÓN PREFLIGHT DEL PROYECTO (BLOQUE 28)")
    print("=" * 70)

    chk_indice = verificar_indice_persistido(ruta_indice)
    chk_corpus = verificar_corpus(ruta_data)
    chk_git = verificar_gitignore(ruta_gitignore)
    chk_libs = verificar_librerias()

    print("-" * 70)
    if chk_indice and chk_corpus and chk_git and chk_libs:
        print("✓ PREFLIGHT EXITOSO: Todos los componentes operativos y seguros.")
        print("=" * 70)
        return 0
    else:
        print("✗ PREFLIGHT CON OBSERVACIONES: Revise los puntos marcados con ✗.")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(ejecutar_preflight())
