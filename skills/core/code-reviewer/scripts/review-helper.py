#!/usr/bin/env python3
import sys
import json

def format_review(findings):
    """
    Formatea una lista de hallazgos en una tabla Markdown.
    findings: lista de dicts con keys: level, location, description, suggestion
    """
    if not findings:
        return "No se encontraron problemas en la revisión. ¡Buen trabajo! ✅"

    report = "# Code Review Report\n\n"
    report += "| Nivel | Ubicación | Problema | Sugerencia |\n"
    report += "| :--- | :--- | :--- | :--- |\n"
    
    for f in findings:
        report += f"| {f['level']} | `{f['location']}` | {f['description']} | {f['suggestion']} |\n"
    
    return report

if __name__ == "__main__":
    # Ejemplo de uso desde la IA
    test_data = [
        {"level": "Advertencia", "location": "auth.py:12", "description": "Uso de variable global", "suggestion": "Pasar como parámetro"},
        {"level": "Mejora", "location": "utils.py:45", "description": "Función demasiado larga", "suggestion": "Refactorizar en sub-funciones"}
    ]
    print(format_review(test_data))
