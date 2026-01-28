#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
AGENTS_MD = ROOT / "agents" / "AGENTS.md"
ROUTING_JSON = ROOT / "skills" / "core" / "decision-engine" / "agent-routing.json"
CATALOG_JSON = ROOT / "agents" / "core" / "orchestrator" / "catalog.json"


def parse_agents_md(path):
    if not path.exists():
        return {}
    content = path.read_text(encoding="utf-8")
    agents = {}
    # Match ### @agent-name followed by properties
    blocks = re.findall(r"### (@[a-zA-Z0-9\-]+)\n(.*?)(?=\n### |$)", content, re.DOTALL)
    for name, body in blocks:
        props = {}
        for line in body.strip().split("\n"):
            if line.startswith("- **"):
                key_match = re.match(r"- \*\*(.*?)\*\*: (.*)", line)
                if key_match:
                    key = key_match.group(1).lower()
                    val = key_match.group(2).strip().strip("`").strip("'")
                    props[key] = val
        agents[name] = props
    return agents


def main():
    agents_meta = parse_agents_md(AGENTS_MD)

    routing_data = {}
    if ROUTING_JSON.exists():
        routing_data = json.loads(ROUTING_JSON.read_text(encoding="utf-8"))

    catalog = {}
    # Combine metadata and routing keywords
    all_names = set(agents_meta.keys()) | set(routing_data.keys())

    for name in all_names:
        meta = agents_meta.get(name, {})
        catalog[name] = {
            "name": name,
            "description": meta.get("propósito", meta.get("purpose", "N/D")),
            "location": meta.get("ubicación", meta.get("location", "N/D")),
            "keywords": routing_data.get(name, []),
        }

    CATALOG_JSON.write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"[OK] Catalogo actualizado en {CATALOG_JSON}")


if __name__ == "__main__":
    main()
