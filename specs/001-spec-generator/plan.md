# Implementation Plan: High-Level Platform Architecture

**Branch**: `001-spec-generator` | **Date**: 2025-12-05 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-spec-generator/spec.md` and high-level goal from user prompt.

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the high-level architecture for the 'Physical AI & Humanoid Robotics' book platform. It includes a static site for the book content, a RAG-based chatbot for interactive queries, and an automated pipeline for content processing and deployment. The technical approach is based on a modern stack using Docusaurus, Python/FastAPI, and a vector database.

## Technical Context

**Language/Version**: Python 3.11+, Node.js 20+
**Primary Dependencies**: Docusaurus, FastAPI, LangChain, FAISS
**Storage**: FAISS vector index file, MDX content files
**Testing**: Pytest for backend, Vitest/Jest for frontend
**Target Platform**: Web/Static Site deployed via Vercel/Netlify and containerized API via Render/Fly.io
**Project Type**: Web Application (Static Site + API)
**Performance Goals**: <5 second p95 latency for RAG queries.
**Constraints**: Must be deployable from a GitHub repository via GitHub Actions.
**Scale/Scope**: Book with ~20-30 chapters; RAG operates on all content.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Principle I: Beginner-Focused Audience** - Docusaurus is excellent for clear, structured content.
- [x] **Principle II: Grounded in Real Use Cases** - The architecture supports embedding rich examples and simulations.
- [x] **Principle III: High Code Quality** - The separation of frontend/backend promotes modularity.
- [x] **Principle IV: Scalable Content** - The automated pipeline handles content growth.
- [x] **Principle V: TDD Mindset** - The plan is derived from a clear spec, and testing frameworks are defined.
- [x] **Principle VI: Structured Writing Style** - The Docusaurus/MDX format encourages a consistent structure.
- [x] **Principle VII: Measurable Learning Outcomes** - The architecture does not inhibit this.
- [x] **Principle VIII: Accessibility and Terminology** - The Docusaurus platform has good accessibility support.
- [x] **Principle IX: Clarity Over Cleverness** - The chosen stack is mainstream and well-documented.
- [x] **Principle X: Consistency is Law** - The use of a single platform (Docusaurus) and pipelines enforces consistency.

## Project Structure

### Documentation (this feature)

```text
specs/001-spec-generator/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
book/             # Docusaurus frontend
├── build/
├── docs/         # Book content in .mdx
├── src/
│   ├── components/ # React components, including Chatbot UI
│   └── pages/
├── static/
└── docusaurus.config.js

api/              # FastAPI RAG backend
├── app/
│   ├── main.py
│   ├── core/     # Config, settings
│   ├── services/ # RAG logic
│   └── models/   # Pydantic models
├── tests/
└── requirements.txt

scripts/          # Automation scripts
└── process_content.py # Generates embeddings

```

**Structure Decision**: The project will use a 'Web Application' structure, separating the `api` (FastAPI RAG service) from the `book` (Docusaurus site). This provides a clear separation of concerns between the content presentation layer and the AI service layer.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
