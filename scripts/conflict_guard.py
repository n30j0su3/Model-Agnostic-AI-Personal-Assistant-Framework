#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_OVERLAP_WARNING = 0.30
DEFAULT_OVERLAP_CONFLICT = 0.45
DEFAULT_MAX_OVERLAPS = 3

STOP_WORDS = {
    "a",
    "an",
    "and",
    "as",
    "by",
    "de",
    "del",
    "el",
    "en",
    "for",
    "is",
    "la",
    "las",
    "los",
    "of",
    "on",
    "or",
    "para",
    "por",
    "que",
    "sin",
    "the",
    "to",
    "un",
    "una",
    "y",
}


def load_json_input(path):
    if path:
        content = Path(path).read_text(encoding="utf-8")
    else:
        content = sys.stdin.read()
    if not content.strip():
        raise ValueError("Empty input")
    return json.loads(content)


def parse_front_matter(path):
    if not path.exists():
        return {}
    content = path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end_index = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_index = idx
            break
    if end_index is None:
        return {}
    data = {}
    for line in lines[1:end_index]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"')
        if key:
            data[key] = value
    return data


def extract_description(path):
    if not path.exists():
        return ""
    content = path.read_text(encoding="utf-8", errors="replace")
    in_front_matter = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped == "---":
            in_front_matter = not in_front_matter
            continue
        if in_front_matter:
            continue
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        return stripped
    return ""


def list_component_dirs(base):
    if not base.exists():
        return []
    return [
        path
        for path in base.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    ]


def load_components():
    components = []
    skills_root = REPO_ROOT / "skills"
    agents_root = REPO_ROOT / "agents"
    workspaces_root = REPO_ROOT / "workspaces"

    for scope in ("core", "custom"):
        for skill_dir in list_component_dirs(skills_root / scope):
            skill_file = skill_dir / "SKILL.md"
            front = parse_front_matter(skill_file)
            name = front.get("name") or skill_dir.name
            desc = front.get("description") or extract_description(skill_file)
            components.append(
                {
                    "type": "skill",
                    "name": name,
                    "description": desc,
                    "path": skill_dir,
                }
            )

        for agent_dir in list_component_dirs(agents_root / scope):
            agent_file = agent_dir / "AGENT.md"
            front = parse_front_matter(agent_file)
            name = front.get("name") or agent_dir.name
            desc = front.get("description") or extract_description(agent_file)
            components.append(
                {
                    "type": "agent",
                    "name": name,
                    "description": desc,
                    "path": agent_dir,
                }
            )

    for workspace_dir in list_component_dirs(workspaces_root):
        components.append(
            {
                "type": "workspace",
                "name": workspace_dir.name,
                "description": "",
                "path": workspace_dir,
            }
        )

    return components


def tokenize(text):
    cleaned = re.sub(r"[^a-z0-9]+", " ", text.lower())
    tokens = [token for token in cleaned.split() if token and token not in STOP_WORDS]
    return set(tokens)


def jaccard_similarity(tokens_a, tokens_b):
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a.intersection(tokens_b)
    union = tokens_a.union(tokens_b)
    if not union:
        return 0.0
    return len(intersection) / len(union)


def format_path(path_value):
    try:
        path = Path(path_value)
    except TypeError:
        return ""
    if path.is_absolute():
        try:
            return str(path.relative_to(REPO_ROOT))
        except ValueError:
            return str(path)
    return str(path)


def identify_component_for_path(path_value):
    path_str = str(path_value).replace("\\", "/")
    parts = [part for part in path_str.split("/") if part]
    for idx, part in enumerate(parts):
        if part in ("skills", "agents") and idx + 2 < len(parts):
            scope = parts[idx + 1]
            if scope in ("core", "custom"):
                return parts[idx + 2]
        if part == "workspaces" and idx + 1 < len(parts):
            return parts[idx + 1]
    return None


def load_dependency_map():
    dependency_map = {}
    for path in (REPO_ROOT / "package.json", REPO_ROOT / ".opencode" / "package.json"):
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        for section in ("dependencies", "devDependencies"):
            for name, version in data.get(section, {}).items():
                dependency_map[name] = str(version)
    return dependency_map


def validate_required_fields(payload):
    required = ["component_type", "name", "description", "paths_to_create"]
    missing = [field for field in required if not payload.get(field)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")


def normalize_paths(paths_value):
    if isinstance(paths_value, str):
        return [paths_value]
    if isinstance(paths_value, list):
        return [path for path in paths_value if isinstance(path, str)]
    return []


def run_conflict_guard(payload, overlap_warning, overlap_conflict, max_overlaps):
    validate_required_fields(payload)

    name = payload.get("name", "")
    description = payload.get("description", "")
    tags = payload.get("tags") or []
    dependencies = payload.get("dependencies") or []
    paths_to_create = normalize_paths(payload.get("paths_to_create"))

    conflicts = []
    warnings = []

    if not description or len(tokenize(description)) < 3:
        warnings.append(
            {
                "type": "NEEDS_REVIEW",
                "message": "Description is too short to evaluate functional overlap.",
            }
        )

    components = load_components()

    name_lower = name.lower()
    for component in components:
        if component["name"].lower() == name_lower:
            conflicts.append(
                {
                    "type": "NAME_COLLISION",
                    "message": f"Name '{name}' already exists as a {component['type']}.",
                    "offending_path": None,
                    "existing_component": component["name"],
                    "severity": "high",
                }
            )
            break

    for path_value in paths_to_create:
        path_obj = Path(path_value)
        if not path_obj.is_absolute():
            path_obj = REPO_ROOT / path_obj
        if path_obj.exists():
            conflicts.append(
                {
                    "type": "PATH_COLLISION",
                    "message": f"Path '{format_path(path_value)}' already exists.",
                    "offending_path": format_path(path_value),
                    "existing_component": identify_component_for_path(path_value),
                    "severity": "high",
                }
            )

    dependency_map = load_dependency_map()
    seen_deps = {}
    for dep in dependencies:
        if not isinstance(dep, dict):
            continue
        dep_name = dep.get("name")
        dep_version = dep.get("version_specifier")
        if not dep_name:
            continue
        if dep_name in seen_deps and seen_deps[dep_name] != dep_version:
            conflicts.append(
                {
                    "type": "DEPENDENCY_CONFLICT",
                    "message": f"Dependency '{dep_name}' has conflicting version specifiers.",
                    "offending_path": None,
                    "existing_component": "input",
                    "severity": "medium",
                }
            )
        seen_deps[dep_name] = dep_version
        if (
            dep_name in dependency_map
            and dep_version
            and dependency_map[dep_name] != dep_version
        ):
            conflicts.append(
                {
                    "type": "DEPENDENCY_CONFLICT",
                    "message": (
                        f"Dependency '{dep_name}' version '{dep_version}' conflicts with"
                        f" existing '{dependency_map[dep_name]}'."
                    ),
                    "offending_path": None,
                    "existing_component": dep_name,
                    "severity": "medium",
                }
            )

    input_text = " ".join([name, description] + list(tags))
    input_tokens = tokenize(input_text)
    overlap_scores = []
    for component in components:
        if component["name"].lower() == name_lower:
            continue
        if not component["description"]:
            continue
        component_tokens = tokenize(component["description"])
        similarity = jaccard_similarity(input_tokens, component_tokens)
        if similarity >= overlap_warning:
            overlap_scores.append((similarity, component))

    overlap_scores.sort(key=lambda item: item[0], reverse=True)
    for similarity, component in overlap_scores[:max_overlaps]:
        if similarity >= overlap_conflict:
            conflicts.append(
                {
                    "type": "FUNCTIONAL_OVERLAP",
                    "message": (
                        f"Potential functional overlap with '{component['name']}'"
                        f" (similarity {similarity:.2f})."
                    ),
                    "offending_path": None,
                    "existing_component": component["name"],
                    "severity": "medium",
                }
            )
        else:
            warnings.append(
                {
                    "type": "LOW_SIGNAL_OVERLAP",
                    "message": (
                        f"Low-signal overlap with '{component['name']}'"
                        f" (similarity {similarity:.2f})."
                    ),
                }
            )

    return {
        "has_conflicts": bool(conflicts),
        "conflicts": conflicts,
        "warnings": warnings,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Conflict guard for framework components"
    )
    parser.add_argument("-i", "--input", help="Path to JSON input file")
    parser.add_argument(
        "--overlap-warning",
        type=float,
        default=DEFAULT_OVERLAP_WARNING,
        help="Similarity threshold to emit warnings",
    )
    parser.add_argument(
        "--overlap-conflict",
        type=float,
        default=DEFAULT_OVERLAP_CONFLICT,
        help="Similarity threshold to emit conflicts",
    )
    parser.add_argument(
        "--max-overlaps",
        type=int,
        default=DEFAULT_MAX_OVERLAPS,
        help="Max overlaps to report",
    )
    args = parser.parse_args()

    overlap_warning = args.overlap_warning
    overlap_conflict = args.overlap_conflict
    if overlap_warning >= overlap_conflict:
        overlap_warning = max(overlap_conflict * 0.7, 0.1)

    try:
        payload = load_json_input(args.input)
        result = run_conflict_guard(
            payload, overlap_warning, overlap_conflict, args.max_overlaps
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
