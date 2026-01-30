# Excalidraw CLI Skill

> **Description**: Permite generar diagramas y esquemas visuales directamente desde la terminal utilizando `excalidraw-cli`.
> **Version**: 1.0.0
> **Source**: https://github.com/swiftlysingh/excalidraw-cli

## Requisitos

- Node.js instalado.
- Paquete instalado: `npm install -g excalidraw-cli`

## Instrucciones para el Agente

1. **Detección**: Antes de usar, verifica si `excalidraw` está disponible en el PATH.
2. **Instalación**: Si no está instalado, ofrece al usuario ejecutar `npm install -g excalidraw-cli`.
3. **Uso**:
   - Para abrir el editor: `excalidraw <archivo.excalidraw>`
   - El CLI suele ser interactivo o lanzar una ventana de navegador.

## Comandos Típicos

```bash
# Crear/Editar un diagrama
excalidraw docs/architecture/diagrama-flujo.excalidraw
```

## Integración con Framework

Este skill se utiliza cuando el usuario pide "diagramar", "dibujar" o "esquematizar" una arquitectura o flujo.
