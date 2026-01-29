# PRD: Personal Assistant Framework v2 (User-Friendly & Open Source)
Author: Feature Architect | Status: Draft | Date: 2026-01-28
Agents: @orchestrator, @feature-architect, @session-manager
Backlog IDs: BL-112, BL-093, BL-111, BL-114

## 1. Overview
### Problem Statement
Advanced AI frameworks are often too technical for average users, requiring manual configuration, complex CLI commands, and lacking a visual interface. Current "User Friendly" solutions often sacrifice privacy or lock users into a specific model/cloud.

### Proposed Solution
A **Model-Agnostic, Local-First AI Personal Assistant Framework** that bridges the gap between power-user capabilities and ease of use. It features a web-based **Dashboard** as a frontend, a **Wizard-style Installer (`pa.bat`)**, and an intelligent **Orchestrator** that handles complex tasks automatically. It prioritizes privacy by keeping sessions and knowledge local.

### Success Metrics
- **Onboarding Time:** < 5 minutes from download to first AI interaction.
- **Usability:** Non-technical users can configure workspaces and backups via Dashboard/Wizard.
- **Privacy:** 0% of private logs/sessions leaked to public repos.
- **Efficiency:** Orchestrator handles >80% of multi-step tasks without user manual intervention.

## 2. Goals & Non-Goals
### Goals
- **Dashboard as Frontend:** `docs/index.html` acts as the control center (Config, Backlog, Stats, History, Codebase).
- **`pa.bat` as Wizard:** Handles dependencies, language (ES/EN), backups, and technical config.
- **Seamless Flows:** Standardized Installation, Execution, and Update flows.
- **Core Intelligence:** Robust operation of CORE-Skills (Decision Engine, Prompt Improvement) and CORE-Agents (Orchestrator, Feature Architect).
- **Default Orchestration:** All CLI inputs are processed by `@orchestrator` to optimize/delegate.
- **Local Knowledge Base:** All sessions/thinking stored and classified locally.

### Non-Goals
- **SaaS Model:** The framework is not a cloud service; it is self-hosted/local software.
- **Closed Source:** No proprietary "black box" components.

## 3. Users & Context
### Primary Users
- **Developers:** Use CLI, customize agents, contribute to code.
- **Researchers/Content Creators:** Use Dashboard, "Context" management, and specialized skills.
- **Homelab/Self-Hosters:** Use automation and local-first privacy features.

### Usage Context
- **Local Machine:** Windows/Linux/macOS.
- **Hybrid Remote:** Syncs with private GitHub repo for backup, public repo for updates.

## 4. Requirements & User Stories

### 4.1. Dashboard (Frontend)
**User Story:** As a user, I want a visual dashboard to manage my AI assistant so I don't have to remember CLI commands.
- **AC1:** `docs/index.html` loads offline without external dependencies.
- **AC2:** Provides quick access to: Config, Backlog, Usage Stats, History, Codebase.
- **AC3:** Allows searching local documentation and session logs.

### 4.2. Installer Wizard (`pa.bat`)
**User Story:** As a beginner, I want a simple installer that sets everything up for me.
- **AC1:** Validates and installs Python/Git/Node requirements.
- **AC2:** Prompts for language selection (ES/EN) and applies it system-wide.
- **AC3:** Guides workspace creation and initial "AI Identity" setup.
- **AC4:** Configures the Dual-Remote strategy (Public Upstream / Private Origin).

### 4.3. Core Operation (Agents & Skills)
**User Story:** As a user, I want the system to be smart enough to handle complex tasks without me micromanaging it.
- **AC1:** **Decision Engine** routes tasks to Local, Delegate, or Remote LLM.
- **AC2:** **Orchestrator** intercepts all CLI prompts by default.
- **AC3:** **Context Evaluator** ensures AI responses meet quality standards.
- **AC4:** **Feature Architect** ensures new features don't break existing ones (Conflict Guard).

### 4.4. Local Knowledge Base
**User Story:** As a user, I want my past conversations to improve future answers without sending data to the cloud.
- **AC1:** Sessions stored in `sessions/YYYY/MM/`.
- **AC2:** "Thinking" process and prompts are logged structurally.
- **AC3:** Agents can query past sessions (Local RAG/Memory).

## 5. Design & Tech
### Installation Flow
1. **Download/Clone** Project.
2. **Run `pa.bat`**.
3. **Dependency Check:** Auto-install missing.
4. **Config Wizard:** Language, Workspaces, Secrets (stored locally).
5. **Pre-Flight:** Run `context-sync`, `update`, `diagnostics`.
6. **Launch:** Open Dashboard + AI CLI with Welcome Message.

### Execution Flow
1. **Run `pa.bat`**.
2. **Diagnostics:** Check integrity.
3. **Sync:** Update context and remote (private).
4. **Ready:** User types in CLI -> `@orchestrator` processes.

### Technical Stack
- **Core:** Python (Scripts/Agents), Shell/Batch (Bootstrapping).
- **UI:** HTML/JS (Alpine.js/Tailwind - Offline Vendorized).
- **Data:** Markdown (Storage), JSON (Config/Logs).

## 6. Analysis: Scope vs. Philosophy
**Current Status:**
- ✅ **High Alignment:** Local-first, Markdown-based, Model-agnostic.
- ⚠️ **Gap:** `pa.bat` needs more Wizard-like features (currently mostly a launcher).
- ⚠️ **Gap:** Dashboard is static; needs more "Control Panel" features (Edit config from UI).
- ⚠️ **Gap:** Orchestrator is active but not yet the *forced default* for all CLI interactions (requires manual invocation in some modes).

**Recommendations:**
1. **Enhance `pa.bat`:** Turn it into a robust CLI menu application (using `inquirer` style or Python TUI) before launching the LLM.
2. **Dashboard Interactive:** Make the Dashboard capable of *writing* to config files (via a local lightweight server or helper script).
3. **Unified CLI Entrypoint:** Deprecate direct usage of `llm` commands in favor of a wrapper that always passes through Orchestrator/DecisionEngine.
4. **Strict Dual-Remote:** Enforce the separation of Public/Private repos in the setup script to prevent accidental leaks.

## 7. Backlog Traceability
- **BL-112:** Dual-Remote Strategy -> Requirement 4.2.
- **BL-093:** Context Cache -> Requirement 4.4.
- **BL-085:** Dashboard UX -> Requirement 4.1.
- **BL-111:** PR Standardization -> Process Requirement.
