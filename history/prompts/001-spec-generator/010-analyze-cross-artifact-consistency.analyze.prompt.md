---
id: 010
title: Analyze Cross-Artifact Consistency
stage: analyze
date: 2025-12-07
surface: agent
model: gemini-pro
feature: 001-spec-generator
branch: 001-spec-generator
user: user
command: /sp.analyze
labels: [quality, consistency, analysis]
links:
  spec: specs/001-spec-generator/spec.md
  ticket: null
  adr: null
  pr: null
files:
- 'specs/001-spec-generator/spec.md'
- 'specs/001-spec-generator/plan.md'
- 'specs/001-spec-generator/tasks.md'
- '.specify/memory/constitution.md'
tests:
- (none)
---

## Prompt

```text
---
description: Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Identify inconsistencies, duplications, ambiguities, and underspecified items across the three core artifacts (`spec.md`, `plan.md`, `tasks.md`) before implementation. This command MUST run only after `/sp.tasks` has successfully produced a complete `tasks.md`.

## Operating Constraints

**STRICTLY READ-ONLY**: Do **not** modify any files. Output a structured analysis report. Offer an optional remediation plan (user must explicitly approve before any follow-up editing commands would be invoked manually).

**Constitution Authority**: The project constitution (`.specify/memory/constitution.md`) is **non-negotiable** within this analysis scope. Constitution conflicts are automatically CRITICAL and require adjustment of the spec, plan, or tasks—not dilution, reinterpretation, or silent ignoring of the principle. If a principle itself needs to change, that must occur in a separate, explicit constitution update outside `/sp.analyze`.

## Execution Steps

### 1. Initialize Analysis Context

Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` once from repo root and parse JSON for FEATURE_DIR and AVAILABLE_DOCS. Derive absolute paths:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md

Abort with an error message if any required file is missing (instruct the user to run missing prerequisite command). For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\'m Groot' (or double-quote if possible: "I'm Groot").

### 2. Load Artifacts (Progressive Disclosure)

Load only the minimal necessary context from each artifact:

**From spec.md:**

- Overview/Context
- Functional Requirements
- Non-Functional Requirements
- User Stories
- Edge Cases (if present)

**From plan.md:**

- Architecture/stack choices
- Data Model references
- Phases
- Technical constraints

**From tasks.md:**

- Task IDs
- Descriptions
- Phase grouping
- Parallel markers [P]
- Referenced file paths

**From constitution:**

- Load `.specify/memory/constitution.md` for principle validation

### 3. Build Semantic Models

Create internal representations (do not include raw artifacts in output):

- **Requirements inventory**: Each functional + non-functional requirement with a stable key (derive slug based on imperative phrase; e.g., "User can upload file" → `user-can-upload-file`)
- **User story/action inventory**: Discrete user actions with acceptance criteria
- **Task coverage mapping**: Map each task to one or more requirements or stories (inference by keyword / explicit reference patterns like IDs or key phrases)
- **Constitution rule set**: Extract principle names and MUST/SHOULD normative statements

### 4. Detection Passes (Token-Efficient Analysis)

Focus on high-signal findings. Limit to 50 findings total; aggregate remainder in overflow summary.

#### A. Duplication Detection

- Identify near-duplicate requirements
- Mark lower-quality phrasing for consolidation

#### B. Ambiguity Detection

- Flag vague adjectives (fast, scalable, secure, intuitive, robust) lacking measurable criteria
- Flag unresolved placeholders (TODO, TKTK, ???, `<placeholder>`, etc.)

#### C. Underspecification

- Requirements with verbs but missing object or measurable outcome
- User stories missing acceptance criteria alignment
- Tasks referencing files or components not defined in spec/plan

#### D. Constitution Alignment

- Any requirement or plan element conflicting with a MUST principle
- Missing mandated sections or quality gates from constitution

#### E. Coverage Gaps

- Requirements with zero associated tasks
- Tasks with no mapped requirement/story
- Non-functional requirements not reflected in tasks (e.g., performance, security)

#### F. Inconsistency

- Terminology drift (same concept named differently across files)
- Data entities referenced in plan but absent in spec (or vice versa)
- Task ordering contradictions (e.g., integration tasks before foundational setup tasks without dependency note)
- Conflicting requirements (e.g., one requires Next.js while other specifies Vue)

### 5. Severity Assignment

Use this heuristic to prioritize findings:

- **CRITICAL**: Violates constitution MUST, missing core spec artifact, or requirement with zero coverage that blocks baseline functionality
- **HIGH**: Duplicate or conflicting requirement, ambiguous security/performance attribute, untestable acceptance criterion
- **MEDIUM**: Terminology drift, missing non-functional task coverage, underspecified edge case
- **LOW**: Style/wording improvements, minor redundancy not affecting execution order

### 6. Produce Compact Analysis Report

Output a Markdown report (no file writes) with the following structure:

## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Duplication | HIGH | spec.md:L120-134 | Two similar requirements ... | Merge phrasing; keep clearer version |

(Add one row per finding; generate stable IDs prefixed by category initial.)

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|

**Constitution Alignment Issues:** (if any)

**Unmapped Tasks:** (if any)

**Metrics:**

- Total Requirements
- Total Tasks
- Coverage % (requirements with >=1 task)
- Ambiguity Count
- Duplication Count
- Critical Issues Count

### 7. Provide Next Actions

At end of report, output a concise Next Actions block:

- If CRITICAL issues exist: Recommend resolving before `/sp.implement`
- If only LOW/MEDIUM: User may proceed, but provide improvement suggestions
- Provide explicit command suggestions: e.g., "Run /sp.specify with refinement", "Run /sp.plan to adjust architecture", "Manually edit tasks.md to add coverage for 'performance-metrics'"

### 8. Offer Remediation

Ask the user: "Would you like me to suggest concrete remediation edits for the top N issues?" (Do NOT apply them automatically.)

## Operating Principles

### Context Efficiency

- **Minimal high-signal tokens**: Focus on actionable findings, not exhaustive documentation
- **Progressive disclosure**: Load artifacts incrementally; don't dump all content into analysis
- **Token-efficient output**: Limit findings table to 50 rows; summarize overflow
- **Deterministic results**: Rerunning without changes should produce consistent IDs and counts

### Analysis Guidelines

- **NEVER modify files** (this is read-only analysis)
- **NEVER hallucinate missing sections** (if absent, report them accurately)
- **Prioritize constitution violations** (these are always CRITICAL)
- **Use examples over exhaustive rules** (cite specific instances, not generic patterns)
- **Report zero issues gracefully** (emit success report with coverage statistics)
```

## Response snapshot

## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **C1** | **Inconsistency** | **CRITICAL** | `spec.md`<br>`plan.md`<br>`tasks.md` | **Artifact Mismatch**: The `spec.md` describes a "Specification Generator" tool, but the `plan.md` and `tasks.md` describe the architecture and tasks for a "Book Platform with RAG Chatbot". The artifacts are for two different projects. | The `spec.md` needs to be regenerated or manually rewritten to describe the "Book Platform" feature that is actually being built. Run `/sp.specify` with the correct feature description. |
| **C2** | **Constitution** | **CRITICAL** | `spec.md`<br>`plan.md` | **Violation of TDD Mindset (Principle V)**: The implementation plan and tasks do not correspond to the approved specification. This breaks the core "spec-driven" workflow. | This is a direct consequence of C1. Resolving the artifact mismatch will resolve this constitutional violation. |
| **G1** | **Coverage Gap** | **CRITICAL** | `spec.md`<br>`tasks.md` | **Zero Task Coverage**: All functional requirements (`FR-001` to `FR-006`) defined in `spec.md` have no corresponding tasks in `tasks.md`. | This is a symptom of C1. Once the `spec.md` is corrected, `tasks.md` must be regenerated or updated to match. |
| **G2** | **Coverage Gap** | **HIGH** | `tasks.md` | **Unmapped Tasks**: All tasks (`T001` to `T023`) are unmapped to any requirement in `spec.md`, as they belong to a different project. | This is a symptom of C1. Correcting the spec and tasks will resolve this. |
| **C3** | **Inconsistency** | **HIGH** | `tasks.md` | **Tasks Marked as Complete**: All 23 tasks are marked with `[X]`, indicating they are already complete. Pre-implementation analysis is meant to occur *before* work starts. | If implementation has not started, remove the `[X]` markers. If it has, this analysis should be used for course correction, not gating. |
| **C4** | **Inconsistency** | **MEDIUM** | `tasks.md`:L38<br>`book/src/components/` | **File Extension Mismatch**: Task `T008` refers to `Callout.js`, but the project uses TypeScript and the actual file is `Callout.tsx`. | Update task description in `tasks.md` to use the correct `.tsx` extension for React components in this project. |
| **C5** | **Inconsistency** | **MEDIUM** | `plan.md`:L91<br>`book/` | **Config File Mismatch**: The `plan.md` project structure diagram lists `docusaurus.config.js`, but the file in the project is `docusaurus.config.ts`. | Update the `plan.md` to reflect the use of TypeScript for the Docusaurus configuration file (`.ts`). |
| **C6** | **Inconsistency** | **MEDIUM** | `tasks.md`:L50, L56<br>`api/faiss_index/` | **Index Filename Mismatch**: Tasks `T012` and `T014` refer to `faiss_index.bin`, but the generated index files are `index.faiss` and `index.pkl`. | Update `tasks.md` and `plan.md` to use the correct index filenames (`index.faiss`, `index.pkl`) and paths. |

---

### Coverage Summary Table

Due to the critical mismatch between the spec and tasks, a meaningful coverage mapping is not possible.

| Requirement Key | Has Task? | Task IDs | Notes |
| :--- | :--- | :--- | :--- |
| `generate-branch-name` | **No** | (none) | Requirement is for the wrong project. |
| `handle-name-collisions` | **No** | (none) | Requirement is for the wrong project. |
| `create-feature-branch` | **No** | (none) | Requirement is for the wrong project. |
| `create-spec-file` | **No** | (none) | Requirement is for the wrong project. |
| `populate-spec-file` | **No** | (none) | Requirement is for the wrong project. |
| `spec-placeholders` | **No** | (none) | Requirement is for the wrong project. |

---

### Metrics

-   Total Requirements: 6
-   Total Tasks: 23
-   **Coverage %**: 0%
-   Ambiguity Count: 0
-   Duplication Count: 0
-   **Critical Issues Count**: 3

## Outcome

- ✅ Impact: Identified critical inconsistencies blocking development. Provided actionable recommendations to resolve them.
- 🧪 Tests: No tests were run. This was a static analysis task.
- 📁 Files: Read 4 files. Did not modify any files.
- 🔁 Next prompts: User was advised to run `/sp.specify`, `/sp.plan`, and `/sp.tasks` to regenerate artifacts.
- 🧠 Reflection: The core failure was a complete mismatch between the specification and the implementation plan. This highlights the importance of the `/sp.analyze` command to catch such deviations early.

## Evaluation notes (flywheel)

- Failure modes observed: Critical deviation between specification and plan/tasks.
- Graders run and results (PASS/FAIL): PASS (Analysis completed successfully).
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
