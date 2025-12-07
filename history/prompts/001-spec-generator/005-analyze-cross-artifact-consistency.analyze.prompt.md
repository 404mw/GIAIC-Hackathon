---
id: 005
title: Analyze Cross-Artifact Consistency
stage: analyze
date: 2025-12-06
surface: agent
model: gemini-pro
feature: 001-spec-generator
branch: 001-spec-generator
user: 404mw
command: /sp.analyze
labels: ["analysis", "consistency", "quality"]
links:
  spec: "specs/001-spec-generator/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "none"
tests:
  - "none"
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

Abort with an error message if any required file is missing (instruct the user to run missing prerequisite command). 
For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

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

## Context

we use context7 mcp to fetch the docusaurus docs and use UV as the package manager instead of pip
```

## Response snapshot

```markdown
## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| F1 | Inconsistency | **CRITICAL** | spec.md vs. plan.md, tasks.md | The `spec.md` describes a "Specification Generator" feature (`/sp.specify`), but the `plan.md` and `tasks.md` describe a completely different "High-Level Platform Architecture" for a book website with a RAG chatbot. The plan does not implement the spec. | Halt implementation. Re-run `/sp.plan` and `/sp.tasks` with the correct intent aligned with `spec.md`, or create a new specification for the Platform Architecture feature. |
| E1 | Coverage Gap | **CRITICAL** | spec.md, tasks.md | All Functional Requirements (FR-001 to FR-006) and Success Criteria (SC-001 to SC-003) in `spec.md` have zero task coverage in `tasks.md` due to the content inconsistency (F1). | Address the core inconsistency (F1). Generate tasks that directly implement the requirements in `spec.md`. |
| C1 | Underspecification | HIGH | spec.md, tasks.md | The `tasks.md` file introduces four distinct User Stories (Book Content Site, Content Processing Pipeline, RAG API Service, Chatbot UI) that are not defined or specified in `spec.md`. | These user stories represent significant new features. They must be formally defined in a specification document before implementation to align with the TDD mindset (Principle V). |

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| gen-branch-name | No | (none) | No tasks in `tasks.md` relate to this requirement. |
| handle-branch-collision | No | (none) | No tasks in `tasks.md` relate to this requirement. |
| create-new-branch | No | (none) | No tasks in `tasks.md` relate to this requirement. |
| create-spec-file | No | (none) | No tasks in `tasks.md` relate to this requirement. |
| populate-spec-file | No | (none) | No tasks in `tasks.md` relate to this requirement. |
| include-placeholders | No | (none) | No tasks in `tasks.md` relate to this requirement. |
| quality-checklist | No | (none) | No tasks in `tasks.md` relate to this NFR. |
| generation-timeout | No | (none) | No tasks in `tasks.md` relate to this NFR. |
| user-success-rate | No | (none) | No tasks in `tasks.md` relate to this NFR. |

**Metrics:**

- Total Requirements: 9
- Total Tasks: 23
- Coverage %: 0%
- Ambiguity Count: 0
- Duplication Count: 0
- Critical Issues Count: 2
```

## Outcome

- ✅ Impact: Identified critical inconsistencies between specification and implementation plan, preventing incorrect work.
- 🧪 Tests: n/a
- 📁 Files: 1 created
- 🔁 Next prompts: User to decide whether to regenerate the plan/tasks for the correct spec, or to create a new spec for the existing plan.
- 🧠 Reflection: The core of the issue was a context mismatch during the generation of the plan and tasks. The agent correctly identified this as a critical, blocking failure. The analysis prevented wasted effort on implementing the wrong feature.

## Evaluation notes (flywheel)

- Failure modes observed: Critical mismatch between different stages of the development lifecycle (spec vs. plan/tasks).
- Graders run and results (PASS/FAIL): PASS (Analysis was successful)
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
```