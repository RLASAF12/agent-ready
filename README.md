# agent-ready: AI Agent Readiness Checker

`agent-ready` is a Python CLI that evaluates a code repository's structure and content for optimal performance with AI coding agents like Claude Code, Cursor, and GitHub Copilot.

AI coding agents are now standard development tools. The quality and relevance of their suggestions, refactors, and code generation heavily depend on the clarity, consistency, and discoverability of a repository's codebase. `agent-ready` helps identify areas for improvement to maximize agent effectiveness.

## Quick Start

To check a repository, simply run the script with the path to your repository:

```bash
# Clone the agent-ready repository
git clone https://github.com/your-org/agent-ready.git
cd agent-ready

# Run the check against your target repository
python3 agent_ready.py /path/to/your/project
```

## What It Checks

`agent-ready` performs the following checks, assigning points based on best practices for AI agent comprehension:

| Check                                       | Points |
| :------------------------------------------ | :----- |
| `README.md` exists and is substantial       | 10     |
| `.gitignore` exists and is comprehensive    | 8      |
| `requirements.txt` or equivalent exists     | 7      |
| `pyproject.toml` or `setup.py` exists       | 7      |
| Clear project structure (e.g., `src/`)      | 8      |
| Docstrings/comments present (sample check)  | 10     |
| Type hints used (sample check)              | 8      |
| Test suite detected (`tests/` folder)       | 9      |
| Linter config detected (`.flake8`, `pyproject.toml`) | 6 |
| Formatter config detected (`.prettierrc`, `pyproject.toml`) | 6 |
| CI/CD config detected (`.github/workflows`, `gitlab-ci.yml`) | 5 |
| `CONTRIBUTING.md` exists                    | 4      |
| `LICENSE` file exists                       | 4      |
| Recent activity (last 3 months)             | 8      |
| **Total Possible Score**                    | **100**|

## Grading Scale

The final score translates to a grade:

| Grade | Score Range |
| :---- | :---------- |
| A     | 90-100      |
| B     | 80-89       |
| C     | 70-79       |
| D     | 60-69       |
| F     | < 60        |

## Flags

`agent-ready` supports the following flags:

*   `--json`: Output results as a JSON object. Useful for programmatic consumption.
*   `--badge`: Output a Markdown badge string representing the grade.
*   `--strict`: Exit with a non-zero status code if the grade is below 'B'. Useful for CI/CD pipelines.

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
      - name: Checkout agent-ready
        uses: actions/checkout@v4
        with:
          repository: your-org/agent-ready # Replace with actual repo URL
          path: agent-ready

      - name: Checkout target repository
        uses: actions/checkout@v4
        with:
          path: target-repo

      - name: Run agent-ready check
        run: python3 agent-ready/agent_ready.py target-repo --strict
```
