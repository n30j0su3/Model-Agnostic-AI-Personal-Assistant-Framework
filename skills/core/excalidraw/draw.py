#!/usr/bin/env python3
"""
Wrapper para Excalidraw CLI.
Permite abrir o crear diagramas desde el framework.
"""

import sys
import shutil
import subprocess
from pathlib import Path

def check_install():
    if not shutil.which("excalidraw"):
        print("[ERROR] 'excalidraw' CLI no encontrado en el PATH.")
        print("Por favor instala: npm install -g excalidraw-cli")
        return False
    return True

def open_diagram(path_str):
    path = Path(path_str)
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    
    # En Windows, excalidraw-cli abre el navegador automáticamente si se ejecuta sin argumentos o con archivo
    # Pero cmd /c es necesario si es un script batch/cmd
    cmd = ["excalidraw", str(path)]
    if sys.platform == "win32":
        cmd = ["cmd", "/c", "excalidraw", str(path)]
        
    print(f"[INFO] Abriendo Excalidraw para: {path}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Falló la ejecución: {e}")

if __name__ == "__main__":
    if not check_install():
        sys.exit(1)
        
    if len(sys.argv) < 2:
        print("Uso: python skills/core/excalidraw/draw.py <archivo.excalidraw>")
        sys.exit(1)
        
    open_diagram(sys.argv[1])
