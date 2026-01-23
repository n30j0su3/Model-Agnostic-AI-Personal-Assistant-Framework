#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODELS_PATH = REPO_ROOT / ".context" / "models.md"
DEFAULT_PRIMARY = "claude-sonnet"
DEFAULT_FALLBACK = "gemini-pro"

DEFAULT_MODELS = [
    {
        "id": "claude-sonnet",
        "name": "Claude Sonnet 4",
        "provider": "Anthropic",
        "strengths": "Codigo, analisis profundo",
        "cli": "claude",
    },
    {
        "id": "claude-opus",
        "name": "Claude Opus 4",
        "provider": "Anthropic",
        "strengths": "Razonamiento complejo",
        "cli": "claude",
    },
    {
        "id": "gemini-pro",
        "name": "Gemini 2.5 Pro",
        "provider": "Google",
        "strengths": "Contexto largo, analisis",
        "cli": "gemini",
    },
    {
        "id": "gemini-flash",
        "name": "Gemini 2.5 Flash",
        "provider": "Google",
        "strengths": "Respuestas rapidas",
        "cli": "gemini",
    },
    {
        "id": "gpt-4",
        "name": "GPT-4",
        "provider": "OpenAI",
        "strengths": "General, plugins",
        "cli": "codex",
    },
    {
        "id": "local-ollama",
        "name": "Ollama (local)",
        "provider": "Local",
        "strengths": "Privacidad, offline",
        "cli": "ollama",
    },
]

RECOMMEND_RULES = [
    ({"codigo", "code", "programar", "implementar", "feature"}, "claude-sonnet"),
    ({"debug", "error", "bug", "fix"}, "claude-opus"),
    ({"rapido", "buscar", "investigar", "idea", "brainstorm"}, "gemini-flash"),
    ({"documento", "largo", "analisis", "resumen", "research"}, "gemini-pro"),
    ({"privado", "offline", "local", "sensible"}, "local-ollama"),
]


def build_models_markdown(primary, fallback, models):
    lines = [
        "# Orquestacion Multi-Modelo (Opcional)",
        "",
        "## Configuracion Activa",
        f"- **Modelo Principal**: {primary}",
        f"- **Fallback**: {fallback}",
        "",
        "## Catalogo de Modelos",
        "",
        "| ID | Nombre | Proveedor | Fortalezas | CLI |",
        "| --- | --- | --- | --- | --- |",
    ]
    for model in models:
        lines.append(
            f"| {model['id']} | {model['name']} | {model['provider']} | {model['strengths']} | {model['cli']} |"
        )
    lines.extend(
        [
            "",
            "## Reglas de Seleccion por Tarea",
            "- codigo, implementar, feature -> claude-sonnet",
            "- debug, error, bug -> claude-opus",
            "- rapido, buscar, investigar -> gemini-flash",
            "- documento largo, analisis -> gemini-pro",
            "- privado, offline, local -> local-ollama",
            "",
        ]
    )
    return "\n".join(lines)


def load_models_content():
    if not MODELS_PATH.exists():
        return ""
    return MODELS_PATH.read_text(encoding="utf-8")


def parse_active_models(content):
    primary_match = re.search(r"- \*\*Modelo Principal\*\*: (.+)", content)
    fallback_match = re.search(r"- \*\*Fallback\*\*: (.+)", content)
    primary = primary_match.group(1).strip() if primary_match else DEFAULT_PRIMARY
    fallback = fallback_match.group(1).strip() if fallback_match else DEFAULT_FALLBACK
    return primary, fallback


def parse_catalog(content):
    lines = content.splitlines()
    models = []
    in_table = False
    for line in lines:
        if line.strip() == "## Catalogo de Modelos":
            in_table = True
            continue
        if in_table:
            if line.startswith("## "):
                break
            if not line.strip():
                continue
            if line.strip().startswith("|") and "---" in line:
                continue
            if line.strip().startswith("|"):
                parts = [part.strip() for part in line.strip().strip("|").split("|")]
                if len(parts) < 5:
                    continue
                models.append(
                    {
                        "id": parts[0],
                        "name": parts[1],
                        "provider": parts[2],
                        "strengths": parts[3],
                        "cli": parts[4],
                    }
                )
    return models


def catalog_ids(models):
    return {model["id"] for model in models}


def ensure_initialized():
    if not MODELS_PATH.exists():
        print("[WARN] Orquestacion no activada. Ejecuta 'python scripts/orchestrate.py init'.")
        return False
    return True


def cmd_init():
    if MODELS_PATH.exists():
        content = load_models_content()
        if content.strip():
            print("[INFO] Orquestacion ya configurada en .context/models.md")
            return
    MODELS_PATH.parent.mkdir(parents=True, exist_ok=True)
    content = build_models_markdown(DEFAULT_PRIMARY, DEFAULT_FALLBACK, DEFAULT_MODELS)
    MODELS_PATH.write_text(content, encoding="utf-8")
    print("[OK] Orquestacion activada. Archivo creado: .context/models.md")


def cmd_status():
    if not ensure_initialized():
        return
    content = load_models_content()
    if not content.strip():
        print("[WARN] models.md esta vacio. Reejecuta 'orchestrate.py init'.")
        return
    primary, fallback = parse_active_models(content)
    print("[INFO] Configuracion activa:")
    print(f"  - Modelo principal: {primary}")
    print(f"  - Fallback: {fallback}")


def cmd_list():
    if not ensure_initialized():
        return
    content = load_models_content()
    if not content.strip():
        print("[WARN] models.md esta vacio. Reejecuta 'orchestrate.py init'.")
        return
    models = parse_catalog(content)
    if not models:
        models = DEFAULT_MODELS
    print("[INFO] Catalogo de modelos:")
    for model in models:
        print(
            f"  - {model['id']}: {model['name']} | {model['provider']} | {model['strengths']} | {model['cli']}"
        )


def write_config_value(content, label, value):
    pattern = rf"- \*\*{label}\*\*: .*"
    replacement = f"- **{label}**: {value}"
    if re.search(pattern, content):
        return re.sub(pattern, replacement, content)
    if "## Configuracion Activa" in content:
        lines = content.splitlines()
        output = []
        inserted = False
        for line in lines:
            output.append(line)
            if line.strip() == "## Configuracion Activa":
                output.append(replacement)
                inserted = True
        if inserted:
            return "\n".join(output)
    return content


def cmd_switch(model_id, is_fallback=False):
    if not ensure_initialized():
        return
    content = load_models_content()
    if not content.strip():
        print("[WARN] models.md esta vacio. Reejecuta 'orchestrate.py init'.")
        return
    models = parse_catalog(content)
    if not models:
        models = DEFAULT_MODELS
    if "## Configuracion Activa" not in content:
        content = build_models_markdown(DEFAULT_PRIMARY, DEFAULT_FALLBACK, models)
    if model_id not in catalog_ids(models):
        print(f"[ERROR] Modelo '{model_id}' no existe en el catalogo.")
        cmd_list()
        return
    label = "Fallback" if is_fallback else "Modelo Principal"
    content = write_config_value(content, label, model_id)
    MODELS_PATH.write_text(content, encoding="utf-8")
    action = "fallback" if is_fallback else "principal"
    print(f"[OK] Modelo {action} actualizado a: {model_id}")


def cmd_recommend(task_text):
    if not ensure_initialized():
        return
    normalized = task_text.lower()
    recommendation = None
    reason = None
    for keywords, model_id in RECOMMEND_RULES:
        if any(keyword in normalized for keyword in keywords):
            recommendation = model_id
            reason = ", ".join(sorted(keywords))
            break

    content = load_models_content()
    if not content.strip():
        print("[WARN] models.md esta vacio. Reejecuta 'orchestrate.py init'.")
        return
    models = parse_catalog(content)
    if not models:
        models = DEFAULT_MODELS
    primary, _ = parse_active_models(content)

    if recommendation and recommendation not in catalog_ids(models):
        recommendation = None

    if not recommendation:
        recommendation = primary
        reason = "sin coincidencias de palabras clave"

    print("[INFO] Recomendacion de modelo:")
    print(f"  - Tarea: {task_text}")
    print(f"  - Modelo sugerido: {recommendation}")
    print(f"  - Motivo: {reason}")


def prompt_confirm(message):
    choice = input(f"{message} [s/N]: ").strip().lower()
    return choice in {"s", "si", "y", "yes"}


def cmd_disable():
    if not MODELS_PATH.exists():
        print("[INFO] Orquestacion ya estaba desactivada.")
        return
    if not prompt_confirm("Desactivar orquestacion y borrar .context/models.md?"):
        print("[INFO] Operacion cancelada.")
        return
    MODELS_PATH.unlink()
    print("[OK] Orquestacion desactivada.")


def main():
    parser = argparse.ArgumentParser(description="Orquestacion multi-modelo (opcional).")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Activa la orquestacion y crea models.md")
    subparsers.add_parser("status", help="Muestra la configuracion activa")
    subparsers.add_parser("list", help="Lista modelos disponibles")

    switch_parser = subparsers.add_parser("switch", help="Cambia el modelo principal")
    switch_parser.add_argument("model_id", help="ID del modelo")
    switch_parser.add_argument(
        "--fallback",
        action="store_true",
        help="Actualiza el modelo fallback en lugar del principal",
    )

    recommend_parser = subparsers.add_parser("recommend", help="Sugiere modelo")
    recommend_parser.add_argument("task", nargs="+", help="Descripcion de la tarea")

    subparsers.add_parser("disable", help="Desactiva la orquestacion")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "init":
        cmd_init()
    elif args.command == "status":
        cmd_status()
    elif args.command == "list":
        cmd_list()
    elif args.command == "switch":
        cmd_switch(args.model_id, is_fallback=args.fallback)
    elif args.command == "recommend":
        cmd_recommend(" ".join(args.task))
    elif args.command == "disable":
        cmd_disable()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
