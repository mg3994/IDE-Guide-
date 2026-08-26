# Repository Instructions

## Project

This repository is `mg3994/IDE-Guide-`.

Before making changes, inspect the repository structure, existing documentation, build configuration, CI workflows, and established coding conventions. Do not assume the technology stack or commands until verified from the repository.

## General Engineering Principles

- Preserve existing behavior unless the task explicitly requires a behavior change.
- Prefer simple, readable implementations over clever micro-optimizations.
- Do not introduce new dependencies unless explicitly requested or approved.
- Do not modify `package.json`, `tsconfig.json`, or equivalent dependency/compiler configuration without explicit instruction.
- Do not make breaking API or behavioral changes.
- Avoid large architectural changes unless explicitly requested.
- Keep changes narrowly scoped to the requested task.
- Reuse existing utilities and abstractions before introducing new ones.
- Consider edge cases and error handling before completing a change.

## Performance Work

When working on performance:

1. Measure or establish evidence of the bottleneck before optimizing.
2. Identify the smallest safe change with a meaningful expected impact.
3. Prefer optimizations that reduce CPU work, memory usage, I/O, network requests, rendering work, or algorithmic complexity.
4. Do not perform speculative micro-optimizations.
5. Preserve readability and maintainability.
6. Add a concise code comment explaining non-obvious performance optimizations.
7. Document how the performance impact was measured or can be verified.
8. If no defensible performance improvement can be identified, do not make an optimization merely for the sake of changing code.

## Validation

Before considering a change complete:

- Inspect the repository for the correct formatting command.
- Run the project's formatter where appropriate.
- Run the project's lint/static-analysis checks.
- Run the relevant tests.
- Prefer the full test suite when practical.
- Verify that the optimization or change does not alter existing functionality.
- Report commands that could not be run and why.

Never claim that tests or benchmarks passed unless they were actually executed.

## Bolt Performance Agent

When acting as Bolt:

- Read `.jules/bolt.md` before beginning performance work.
- Profile first and optimize second.
- Select exactly one small, low-risk performance improvement per task.
- Prefer changes that can be implemented cleanly in fewer than 50 lines.
- Measure the baseline when practical.
- Measure or provide a reproducible method for verifying the improvement.
- Add expected performance impact to the final report.
- Run formatting, lint/static analysis, and the full available test suite before completing the task.
- Do not create a PR when no suitable performance optimization exists.
- Do not add a journal entry for routine successful work.
- Only update `.jules/bolt.md` when a critical, codebase-specific performance learning is discovered.

## Git and Pull Requests

Performance changes should use the following PR title format:

`⚡ Bolt: [performance improvement]`

The PR description should contain:

- **What:** the optimization implemented.
- **Why:** the measured or identified bottleneck.
- **Impact:** expected or measured performance improvement.
- **Measurement:** how the improvement was verified.
- **Validation:** tests, linting, formatting, and benchmarks that were run.

Keep commits and pull requests focused. Do not mix unrelated refactoring with a performance optimization.
