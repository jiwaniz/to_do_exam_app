<!--
  Sync Impact Report
  ==================
  Version change: 1.0.0 → 1.1.0
  Modified principles: None
  Added sections:
    - Principle V: Token Optimization
  Removed sections: None
  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ compatible
    - .specify/templates/spec-template.md ✅ compatible
    - .specify/templates/tasks-template.md ✅ compatible
  Follow-up TODOs: None
-->

# Todo CLI Constitution

## Core Principles

### I. Simplicity First

Every feature MUST use the smallest viable implementation that
satisfies requirements. No abstractions, patterns, or indirections
are permitted unless they solve a demonstrated, current problem.

- YAGNI: Do not build for hypothetical future requirements.
- Prefer flat structures over nested hierarchies.
- A function MUST do one thing; a module MUST have one responsibility.
- If a solution requires more than 50 lines in a single function,
  break it into named steps with clear intent.

**Rationale**: A console To-Do app serves as a learning project;
unnecessary complexity defeats the purpose and obscures core logic.

### II. CLI-First Interface

All user interaction MUST occur through a text-based console menu.
Input comes from stdin/arguments; output goes to stdout; errors go
to stderr.

- The main menu MUST be self-documenting (numbered options with
  clear labels).
- Every user action MUST provide confirmation or feedback on
  completion.
- Invalid input MUST produce a helpful error message and re-prompt
  without crashing.
- The app MUST handle graceful exit (Ctrl+C / quit option).

**Rationale**: Console-first ensures the app is testable,
scriptable, and accessible without GUI dependencies.

### III. File-Based Persistence

All to-do data MUST be persisted to a local JSON file so items
survive between sessions.

- The storage file MUST use a human-readable JSON format.
- Read/write operations MUST handle missing or corrupted files
  gracefully (create new or warn, never crash).
- Data integrity: writes MUST be atomic where possible (write to
  temp file, then rename).
- The storage path MUST be configurable (default: `todos.json` in
  the working directory).

**Rationale**: JSON file storage is the simplest persistence
mechanism that requires no external dependencies and allows users
to inspect/edit data manually.

### IV. Test-First (TDD) (NON-NEGOTIABLE)

All feature implementation MUST follow the Red-Green-Refactor cycle.

- **Red**: Tests MUST be written and approved before any
  implementation code.
- **Green**: Write the minimum code to make failing tests pass.
- **Refactor**: Clean up while keeping all tests green.
- Every functional requirement MUST have at least one corresponding
  test.
- Tests MUST be independent: no test may depend on another test's
  side effects.
- Test files MUST mirror source structure under a `tests/` directory.

**Rationale**: TDD ensures correctness from the start, prevents
regressions, and produces a living specification of behavior.

### V. Token Optimization

All AI-assisted development MUST minimize token consumption across
every phase of the workflow without sacrificing clarity or correctness.

- Prompts and artifacts MUST be concise: no filler words, redundant
  explanations, or verbose formatting.
- Specs, plans, and tasks MUST use bullet points and short sentences
  over paragraphs where possible.
- Code MUST avoid unnecessary comments that restate what the code
  already expresses; comment only non-obvious intent.
- AI interactions MUST batch related questions into single prompts
  rather than multiple round-trips.
- Generated artifacts MUST omit boilerplate sections that add no
  value for the specific feature.
- Prefer precise references (file:line, entity names) over lengthy
  contextual descriptions.

**Rationale**: Token efficiency reduces cost, speeds up AI responses,
and forces disciplined thinking. Every token MUST earn its place.

## Code Quality Standards

- Python 3.10+ is the target runtime.
- All code MUST pass linting (ruff or flake8) with zero warnings.
- Type hints MUST be used for all function signatures.
- No third-party dependencies for core functionality; standard
  library only.
- Naming: snake_case for functions/variables, PascalCase for classes,
  UPPER_CASE for constants.

## Development Workflow

1. **Specify**: Define what to build (spec.md).
2. **Plan**: Design how to build it (plan.md).
3. **Task**: Break plan into testable increments (tasks.md).
4. **Red**: Write failing tests for the next task.
5. **Green**: Implement until tests pass.
6. **Refactor**: Improve code quality while tests stay green.
7. **Commit**: One logical change per commit with a descriptive message.

Each phase MUST be completed and validated before moving to the next.

## Governance

- This constitution is the highest-authority document for the
  Todo CLI project. All specs, plans, and code MUST comply.
- Amendments require: (1) a written proposal, (2) documented
  rationale, (3) updated version number following SemVer.
- Compliance is checked at every phase gate (spec review, plan
  review, code review).
- When a principle conflicts with a practical need, the conflict
  MUST be documented in a Complexity Tracking table with
  justification.

**Version**: 1.1.0 | **Ratified**: 2026-02-14 | **Last Amended**: 2026-02-14
