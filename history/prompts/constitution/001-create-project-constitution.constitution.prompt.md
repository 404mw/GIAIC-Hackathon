---
id: 001
title: Create Project Constitution
stage: constitution
date: 2025-12-05
surface: agent
model: gemini-pro
feature: none
branch: master
user: n/a
command: /sp.constitution
labels: [constitution, project-setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
- .specify/templates/plan-template.md
tests:
[]
---

## Prompt

/sp.constitution Goal: Maintain consistent technical, instructional, and architectural quality across the project.

Principles:
- Audience is beginners → content must be clear, progressive, example-driven, visually supported.
- Every explanation must be grounded in real use cases in robotics (ROS2, Gazebo, Isaac, sensors).
- Code must follow OOP, modularity, separation of concerns, extensibility, reusability.
- All content must scale: works for small examples and expands to full humanoid robotics pipelines.
- Use test-driven development mindset → specs before implementation, edge cases considered early.
- Writing style must be structured: Concept → Why it matters → Example → Hands-On steps → Summary.
- No vague claims. Every learning module must have measurable learning outcomes.
- Accessibility requirement → explain new terms plainly before using them.
- When in conflict, clarity > cleverness. Beginners must be able to follow smoothly.
- Consistency is law. Tone, formatting, terminology, difficulty progression must remain uniform.

## Response snapshot

I have successfully created the project constitution and updated the relevant templates.

- Created `.specify/memory/constitution.md` with the 10 principles.
- Updated `.specify/templates/plan-template.md` to include a constitution check.
- Created a Prompt History Record (PHR) for this operation.

## Outcome

- ✅ Impact: The project now has a clear set of guiding principles.
- 🧪 Tests: No tests were run.
- 📁 Files: 
  - `.specify/memory/constitution.md` (created)
  - `.specify/templates/plan-template.md` (modified)
  - `history/prompts/constitution/001-create-project-constitution.constitution.prompt.md` (created)
- 🔁 Next prompts: The user can now proceed with other commands like `/sp.specify` or `/sp.plan`.
- 🧠 Reflection: The process of creating the constitution and updating the templates went smoothly. The fallback mechanism for PHR creation on Windows worked as expected.

## Evaluation notes (flywheel)

- Failure modes observed: The bash script for PHR creation is not directly usable on Windows.
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
