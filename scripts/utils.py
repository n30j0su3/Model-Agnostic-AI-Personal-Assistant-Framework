#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

class PlatformHelper:
    """Clase de utilidad para garantizar compatibilidad multiplataforma."""
    
    @staticmethod
    def clear_screen():
        """Limpia la terminal de forma compatible con Windows y POSIX."""
        if sys.stdout.isatty():
            os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def get_python_executable():
        """Retorna el ejecutable de Python actual."""
        return sys.executable

    @staticmethod
    def run_command(command_list, cwd=None, capture_output=True):
        """Ejecuta un comando de subproceso de forma segura."""
        try:
            return subprocess.run(
                command_list, 
                cwd=cwd, 
                capture_output=capture_output, 
                text=True, 
                check=False
            )
        except FileNotFoundError as e:
            return subprocess.CompletedProcess(
                args=command_list, 
                returncode=1, 
                stderr=f"Executable not found: {e}"
            )

def get_repo_root():
    """Retorna la raíz del repositorio usando pathlib."""
    return Path(__file__).resolve().parents[1]
