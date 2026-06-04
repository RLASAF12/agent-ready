# agent-ready: AI Agent Readiness Checker

[![PyPI version](https://img.shields.io/pypi/v/agent-ready-cli.svg)](https://pypi.org/project/agent-ready-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/agent-ready-cli.svg)](https://pypi.org/project/agent-ready-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

`agent-ready` is a Python CLI that evaluates a code repository's structure and content for optimal performance with AI coding agents like Claude Code, Cursor, and GitHub Copilot.

AI coding agents are now standard development tools. The quality and relevance of their suggestions, refactors, and code generation heavily depend on the clarity, consistency, and discoverability of a repository's codebase. `agent-ready` helps identify areas for improvement to maximize agent effectiveness.

## Installation

```bash
pip install agent-ready-cli
```

## Quick Start

```bash
agent-ready /path/to/your/project
```

## What It Checks

`agent-ready` performs the following checks, assigning points based on best practices for AI agent comprehension:

| Check | Points |
|-------|--------|
| README.md exists and is substantial | 10 |
| .gitignore exists and is comprehensive | 8 |
| requirements.txt or equivalent exists | 7 |
| pyproject.toml or setup.py exists | 7 |
| Clear project structure (e.g., src/) | 8 |
| Docstrings/comments present (sample check) | 10 |
| Type hints used (sample check) | 8 |
| Test suite detected (tests/ folder) | 9 |
| Linter config detected (.flake8, pyproject.toml) | 6 |
| Formatter config detected (.prettierrc, pyproject.toml) | 6 |
| CI/CD config detected (.github/workflows, gitlab-ci.yml) | 5 |
| CONTRIBUTING.md exists | 4 |
| LICENSE file exists | 4 |
| Recent activity (last 3 months) | 8 |
| **Total Possible Score** | **100** |

## Grading Scale

| Grade | Score Range |
|-------|-------------|
| A | 90–100 |
| B | 80–89 |
| C | 70–79 |
| D | 60–69 |
| F | < 60 |

## Flags

- `--json`: Output results as a JSON object. Useful for programmatic consumption.
- `--badge`: Output a Markdown badge string representing the grade.
- `--strict`: Exit with a non-zero status code if the grade is below 'B'. Useful for CI/CD pipelines.

## Badge Example

```markdown
![Agent Readiness Grade](https://img.shields.io/badge/agent--ready-A-brightgreen)
```

## Use in CI

Integrate `agent-ready` into your CI/CD pipeline to ensure ongoing agent readiness.

```yaml
name: Agent Readiness Check

on: [push, pull_request]

jobs:
  check-readiness:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install agent-ready
        run: pip install agent-ready-cli

      - name: Run agent-ready check
        run: agent-ready . --strict
```
