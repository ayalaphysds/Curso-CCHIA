"""
Script de diagnóstico y verificación de entorno virtual.
Especialización en IA Accenture - Curso CCHIA
Unidad U1.2 · Bloque 3: Entorno Virtual y Dependencias
"""

import sys
import os

# Asegurar codificación UTF-8 en consolas Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def diagnosticar():
    print("=" * 65)
    print("[DIAGNÓSTICO DE ENTORNO PYTHON]")
    print("=" * 65)
    
    # 1. Comprobar si está en un entorno virtual
    # Si sys.prefix != sys.base_prefix, el script se ejecuta dentro de un venv
    en_venv = (sys.prefix != getattr(sys, "base_prefix", sys.prefix))
    
    if en_venv:
        print("[ESTADO] -> ESTÁS DENTRO DE UN ENTORNO VIRTUAL (.venv)")
    else:
        print("[ESTADO] -> ESTÁS EN EL PYTHON GLOBAL DEL SISTEMA (Fuera de .venv)")
        
    print(f"\n* Intérprete activo (sys.executable):")
    print(f"  {sys.executable}")
    
    print(f"\n* Directorio del entorno (sys.prefix):")
    print(f"  {sys.prefix}")
    
    print(f"\n* Directorio base de Python (sys.base_prefix):")
    print(f"  {getattr(sys, 'base_prefix', sys.prefix)}")
    
    # 2. Verificar librerías clave instaladas
    print("\n* Verificación de librerías en este entorno:")
    librerias = [("requests", "requests"), ("python-dotenv", "dotenv"), ("urllib3", "urllib3")]
    for nombre_pkg, nombre_mod in librerias:
        try:
            modulo = __import__(nombre_mod)
            version = getattr(modulo, "__version__", "OK")
            print(f"  [OK] {nombre_pkg:<15}: Versión {version}")
        except ImportError:
            print(f"  [NO] {nombre_pkg:<15}: NO INSTALADA en este intérprete")
            
    print("=" * 65)
    if en_venv:
        print("[LISTO] Tu entorno está correctamente aislado y listo para usar.")
    else:
        print("[CONSEJO] Activa tu entorno virtual ejecutando:")
        print("          .\\.venv\\Scripts\\Activate.ps1")
    print("=" * 65)

if __name__ == "__main__":
    diagnosticar()
