# Context Manifest

## Version
- Current: 1.0.0
- Last Updated: 2026-01-23
- Schema: v1

## Structure

| File | Purpose | Source |
| --- | --- | --- |
| MASTER.md | Global preferences and rules | Manual edit |
| opencode.md | OpenCode context sync | MASTER.md + local overrides |
| claude.md | Claude context sync | MASTER.md + local overrides |
| gemini.md | Gemini context sync | MASTER.md + local overrides |
| agents.md | Agents context sync | MASTER.md + local overrides |
| profile.md | Installation profile | install.py |
| models.md | Orchestration config (optional) | orchestrate.py |
| manifest.md | Context manifest | Manual edit |
| versions/ | Context snapshots | context-version.py |
| backups/ | Context backups | context-version.py |

## Versioning Rules

- Snapshots are stored in `.context/versions/` with timestamp prefixes.
- Backups are stored in `.context/backups/` as zip archives.
- Snapshots are created before each sync.
- Validation runs after each sync.
- Git tracks the context files; no vendor lock-in.

## Merge Rules

See `docs/architecture/scopes.mdx` for merge and override guidance.
