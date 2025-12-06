# Research & Decisions

This document captures the research and decisions made to resolve the "NEEDS CLARIFICATION" items in the project plan.

## 1. Core Technology Stack

- **Decision**: The project will be built on a dual-stack: Python for the backend AI services and Node.js/TypeScript for the frontend book platform.
  - **Language/Version**: Python 3.11+, Node.js 20+
  - **Primary Dependencies**: FastAPI (Python), Docusaurus (Node.js/React)
- **Rationale**:
  - Python is the de facto standard for AI/ML and has mature libraries like FastAPI and LangChain for building performant RAG services.
  - Docusaurus is a best-in-class static site generator specifically for documentation and books. It provides features like versioning, search, and MDX out-of-the-box, which are critical for this project. It is built on React.
- **Alternatives considered**:
  - **Next.js**: A powerful React framework, but more general-purpose. Docusaurus is more specialized for our needs.
  - **Hugo/Jekyll**: Simpler static site generators, but they lack the rich React ecosystem and component-based architecture of Docusaurus.

## 2. RAG Pipeline and Storage

- **Decision**:
  - **Orchestration**: LangChain will be used to manage the RAG pipeline (loading, chunking, embedding, retrieval, and question-answering).
  - **Vector Store**: FAISS (from Facebook AI) will be used as the initial vector store. The generated index will be a file stored in the repository.
  - **Content Format**: Content will be written in MDX (Markdown with JSX), allowing for interactive components within the book.
- **Rationale**:
  - LangChain significantly abstracts the complexity of building RAG pipelines.
  - FAISS is a highly efficient, in-memory vector library that is simple to start with (no separate database server needed). It is suitable for the proposed scale (~20 chapters).
  - MDX provides the flexibility to embed interactive React components directly into the book's content, which aligns with the "Beginner-Focused" and "Real Use Cases" principles.
- **Alternatives considered**:
  - **ChromaDB/Weaviate**: More feature-rich vector databases that run as separate services. They add operational complexity that is not needed for this initial phase but could be a future migration path if the project scales significantly.
  - **Plain Markdown**: Simpler, but lacks the ability to embed interactive components.

## 3. Testing Strategy

- **Decision**:
  - **Backend (API)**: `pytest` will be used for unit and integration tests.
  - **Frontend (Book)**: `Vitest` or `Jest` will be used for testing React components.
- **Rationale**: This is a standard and robust testing setup for a Python/React stack.
- **Alternatives considered**: `unittest` (Python stdlib, but more boilerplate), `Cypress`/`Playwright` (for E2E tests, which can be added later).

## 4. Deployment and Operations

- **Decision**:
  - **Target Platform**: The Docusaurus site will be deployed as a static website. The FastAPI backend will be deployed as a containerized service.
  - **Deployment Host**: Vercel or Netlify are ideal for the frontend static site, as they integrate directly with GitHub and have a generous free tier. The FastAPI backend can be hosted on a service like Render or Fly.io, also with free tiers suitable for this scale.
  - **Constraints & Automation**: Deployment will be automated via GitHub Actions. A workflow will trigger on pushes to the `main` branch to:
    1. Run the `scripts/process_content.py` to regenerate the FAISS index.
    2. Build and deploy the Docusaurus site.
    3. Build and deploy the FastAPI backend.
- **Rationale**: This approach fully automates the content-to-production pipeline, ensuring consistency and reliability. The chosen platforms are developer-friendly and cost-effective for this project's scale.
- **Alternatives considered**: GitHub Pages (for frontend, but less feature-rich than Vercel/Netlify), AWS/GCP (more powerful but significantly more complex to set up and manage for a project of this size).

## 5. Performance and Scale

- **Decision**:
  - **Performance Goal**: The primary goal is a p95 latency of <5 seconds for RAG queries.
  - **Scale/Scope**: The architecture is designed for a book of approximately 20-30 chapters. The RAG pipeline will operate on the entire content base.
- **Rationale**: A 5-second response time is acceptable for a non-real-time chatbot interface. The chosen stack (FAISS in-memory, FastAPI) can easily meet this goal for the defined scope. If content grows 10x+, a move to a more robust vector database might be needed.
- **Alternatives considered**: Real-time streaming responses could be implemented later using WebSockets to improve perceived performance, but this adds complexity not required for the initial build.
