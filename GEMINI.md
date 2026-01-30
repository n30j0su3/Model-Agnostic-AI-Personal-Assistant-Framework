# Model-Agnostic AI Personal Assistant Framework

## Project Overview

The **Model-Agnostic AI Personal Assistant Framework** is a unified system designed to manage personal AI assistants with local context. It empowers users to own their data and leverage multiple AI tools (Gemini, Claude, OpenCode, Codex) seamlessly.

**Key Features:**
*   **Local Context:** All knowledge is stored in `.md` files under user control.
*   **Multi-Tool Workflow:** Supports simultaneous operation of major AI CLIs.
*   **Modular Architecture:** Extensible via **Agents** and **Skills**.
*   **Workspaces:** Pre-configured environments for different disciplines (Personal, Professional, Research, etc.).
*   **Privacy-First:** "Dev HQ" approach keeps personal data in a private repository (`origin`), while public releases go to a sanitized `upstream`.

## Building and Running

### Prerequisites
*   **Python:** 3.11+
*   **Git:** 2.30+
*   **OS:** Windows 10/11, macOS 12+, or Linux.

### Key Commands

**Start the Framework:**
*   **Windows:** `pa.bat`
*   **macOS/Linux:** `./pa.sh`
*   **Dashboard:** `python scripts/pa.py` (Interactive control panel)

**Development Mode (Feature Session):**
*   **Windows:** `dev.bat`
*   **macOS/Linux:** `./dev.sh`
*   **Direct:** `python scripts/pa.py --feature`

**Installation/Setup:**
*   **Installer:** `python scripts/install.py`
*   **Sync Context:** `python scripts/sync-context.py`
*   **Sync Remotes:** `python scripts/sync-remotes.py --private-remote origin`

## Development Conventions

### Code Style (Python)
*   **Version:** Python 3.11+
*   **Indentation:** 4 spaces.
*   **Line Length:** Max 100 characters.
*   **Typing:** Use type hints.
*   **Strings:** Double quotes `"` preferred. f-strings for formatting.
*   **File Operations:** Use `pathlib.Path`.

### Git Workflow
*   **Remote Strategy:**
    *   `origin` (Private): Contains real sessions, logs, and personal context.
    *   `upstream` (Public): Sanitized releases only.
*   **Branches:**
    *   `main`: Private development branch.
    *   `public-release`: Sanitized public branch.
*   **Commit Messages:** In Spanish (`feat:`, `fix:`, `docs:`).

### Critical Rules
*   **`/init` Constraint:** If invoked via `/init`, **MUST** run `dev.bat` / `./dev.sh` immediately. No modifications to `AGENTS.md` allowed.
*   **Privacy:** NEVER commit real sessions or sensitive data to `upstream`.

## Architecture

**Directory Structure:**
*   `.context/`: Central knowledge base (`MASTER.md`).
*   `agents/`: Specialized AI agents (e.g., `@orchestrator`, `@session-manager`).
*   `skills/`: Modular tools/capabilities (e.g., `@pdf`, `@xlsx`).
*   `workspaces/`: Isolated domains for tasks.
*   `sessions/`: Daily logs and traceability.
*   `scripts/`: Python automation scripts.
*   `docs/`: Documentation.

## Key Components

### Core Agents
*   **@orchestrator:** Manages multi-step tasks and delegates to other agents.
*   **@session-manager:** Handles daily sessions and lifecycle.
*   **@decision-engine:** Optimizes routing (Local vs. Remote) to save tokens.
*   **@feature-architect:** Manages the product backlog and features.
*   **@conflict-guard:** Prevents technical overlaps.

### Core Skills
*   **@ui-ux-pro-max:** Generates professional design systems.
*   **@code-reviewer:** Deep code analysis and clean code enforcement.
*   **@prompt-improvement:** Refines prompts for better AI responses.
*   **@task-management:** Tracks tasks across workspaces.
*   **File Handlers:** `@pdf`, `@docx`, `@xlsx`, `@pptx` for document manipulation.
