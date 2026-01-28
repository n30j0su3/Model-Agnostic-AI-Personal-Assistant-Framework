# Feature Analysis Report - BL-072 Integrate session-tracking into session-manager

## Metadata
- report_id: far-2026-01-27-004
- backlog_id: BL-072
- status: approved
- author_agent: @feature-architect
- created_at: 2026-01-27T12:00:00Z
- last_updated: 2026-01-27T12:00:00Z

## Context
- Problem: session-tracking and session-manager are split with overlapping responsibilities.
- Objective: integrate session-tracking into session-manager and consolidate documentation and scripts.

## Scope
- Includes: integrate session-tracking into session-manager, move log-task.py, merge SKILL.md into AGENT.md, remove skill.
- Excludes: preserving session-tracking as a standalone skill.
- Constraints/limits: prevent doc drift and manage loss of standalone skill.

## Overlaps and Conflicts
- conflict_guard_input_ref: not run
- conflict_guard_result: not evaluated
- summary: no overlap analysis recorded.

## Decisions
- decision_engine_ref: not recorded
- decisions:
  - decision: integrate session-tracking into session-manager.
    rationale: reduce overlap and simplify ownership.
    impact: unified session tracking pipeline.
  - decision: merge SKILL.md into AGENT.md and remove skill.
    rationale: consolidate documentation in the agent.
    impact: single source of truth.
  - decision: move log-task.py under session-manager.
    rationale: keep script aligned with owning component.
    impact: centralized task logging.

## Risks
- risks:
  - risk: documentation drift.
    severity: medium
    mitigation: update AGENT.md and docs together.
  - risk: loss of standalone skill.
    severity: low
    mitigation: document migration path in agent docs.

## Plan and Next Steps
- actions:
  - migrate log-task.py into session-manager.
  - update AGENT.md with session-tracking content.
  - delete session-tracking skill directory.
  - update related docs.
- dependencies:
  - none

## Backlog and Traceability
- backlog_updates:
  - BL-072 -> FAR documented (approved).
- events:
  - none recorded.
- artifacts:
  - type: report
    path: docs/architecture/reports/far-bl-072.md
    note: approved FAR for BL-072
