import os
import sys
import argparse
import json
import re
from typing import List, Dict, Any, Tuple, Optional
from urllib.parse import quote # urllib.parse is part of the standard library

# --- ANSI Color Codes ---
class Colors:
    """ANSI escape codes for colored output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"

    @staticmethod
    def apply(text: str, color_code: str, is_tty: bool) -> str:
        """Applies color if output is to a TTY."""
        return f"{color_code}{text}{Colors.RESET}" if is_tty else text

# Global flag to check if stdout is a TTY
IS_TTY = sys.stdout.isatty()

# --- Helper Functions ---
def read_file_content(filepath: str) -> Optional[str]:
    """Reads file content, returns None if file doesn't exist or can't be read."""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except IOError:
        return None

def read_file_lines(filepath: str) -> Optional[List[str]]:
    """Reads file lines, returns None if file doesn't exist or can't be read."""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.readlines()
    except IOError:
        return None

def find_files_in_dir(directory: str, pattern: str) -> List[str]:
    """Finds files matching a regex pattern in a given directory."""
    if not os.path.isdir(directory):
        return []
    found_files = []
    try:
        for filename in os.listdir(directory):
            if re.match(pattern, filename):
                found_files.append(os.path.join(directory, filename))
    except OSError: # Handle permission errors or other issues
        pass
    return found_files

# --- Check Definitions ---
# Each check function returns: (passed: bool, points_awarded: int, message: str)
# The message should describe why it passed or failed.

def check_readme() -> Tuple[bool, int, str]:
    """1. README.md exists → 10pts (bonus +3 if has Architecture section)"""
    filepath = "README.md"
    content = read_file_content(filepath)
    if content:
        points = 10
        message = f"'{filepath}' exists."
        if re.search(r"^\s*#+\s*Architecture", content, re.IGNORECASE | re.MULTILINE):
            points += 3
            message += " Bonus +3 for 'Architecture' section."
        return True, points, message
    return False, 0, f"'{filepath}' not found."

def check_contributing() -> Tuple[bool, int, str]:
    """2. CONTRIBUTING.md exists → 8pts"""
    filepath = "CONTRIBUTING.md"
    if os.path.exists(filepath):
        return True, 8, f"'{filepath}' exists."
    return False, 0, f"'{filepath}' not found."

def check_docs_architecture() -> Tuple[bool, int, str]:
    """3. docs/architecture.md exists → 7pts"""
    filepath = "docs/architecture.md"
    if os.path.exists(filepath):
        return True, 7, f"'{filepath}' exists."
    return False, 0, f"'{filepath}' not found."

def check_agent_instructions() -> Tuple[bool, int, str]:
    """4. CLAUDE.md or .cursorrules or .github/copilot-instructions.md → 10pts"""
    files = ["CLAUDE.md", ".cursorrules", os.path.join(".github", "copilot-instructions.md")]
    for f in files:
        if os.path.exists(f):
            return True, 10, f"'{f}' found for agent instructions."
    return False, 0, f"None of {', '.join(files)} found."

def check_license() -> Tuple[bool, int, str]:
    """5. LICENSE exists → 5pts"""
    license_files = ["LICENSE", "LICENSE.md", "LICENSE.txt"]
    for f in license_files:
        if os.path.exists(f):
            return True, 5, f"'{f}' found."
    return False, 0, f"None of {', '.join(license_files)} found."

def check_tests_dir() -> Tuple[bool, int, str]:
    """6. tests/ or test/ directory → 8pts"""
    if os.path.isdir("tests"):
        return True, 8, "'tests/' directory found."
    if os.path.isdir("test"):
        return True, 8, "'test/' directory found."
    return False, 0, "'tests/' or 'test/' directory not found."

def check_test_config() -> Tuple[bool, int, str]:
    """7. pytest.ini or jest.config.* or vitest.config.* or pyproject.toml with [tool.pytest.ini_options] → 9pts"""
    if os.path.exists("pytest.ini"):
        return True, 9, "'pytest.ini' found."

    if find_files_in_dir(".", r"jest\.config\.(js|ts|cjs|mjs|json)$"):
        return True, 9, "Jest config file found."

    if find_files_in_dir(".", r"vitest\.config\.(js|ts|cjs|mjs)$"):
        return True, 9, "Vitest config file found."

    pyproject_content = read_file_content("pyproject.toml")
    if pyproject_content and "[tool.pytest.ini_options]" in pyproject_content:
        return True, 9, "'pyproject.toml' with '[tool.pytest.ini_options]' found."

    return False, 0, "No common test configuration file found."

def check_makefile_test_target() -> Tuple[bool, int, str]:
    """8. Makefile with test target → 8pts"""
    content = read_file_content("Makefile")
    if content:
        if re.search(r"^\s*test:\s*.*", content, re.MULTILINE):
            return True, 8, "'Makefile' with 'test' target found."
        return False, 0, "'Makefile' found but no 'test' target."
    return False, 0, "'Makefile' not found."

def check_formatter_config() -> Tuple[bool, int, str]:
    """9. Formatter config (.prettierrc, .editorconfig, pyproject.toml with [tool.black], .eslintrc) → 10pts"""
    prettier_configs = [
        ".prettierrc", ".prettierrc.json", ".prettierrc.js", ".prettierrc.cjs",
        ".prettierrc.mjs", ".prettierrc.yaml", ".prettierrc.yml", ".prettierrc.toml"
    ]
    for f in prettier_configs:
        if os.path.exists(f):
            return True, 10, f"'{f}' (Prettier config) found."

    if os.path.exists(".editorconfig"):
        return True, 10, "'.editorconfig' found."

    pyproject_content = read_file_content("pyproject.toml")
    if pyproject_content and "[tool.black]" in pyproject_content:
        return True, 10, "'pyproject.toml' with '[tool.black]' found."

    eslint_configs = [
        ".eslintrc", ".eslintrc.js", ".eslintrc.cjs", ".eslintrc.yaml",
        ".eslintrc.yml", ".eslintrc.json"
    ]
    for f in eslint_configs:
        if os.path.exists(f):
            return True, 10, f"'{f}' (ESLint config) found."

    return False, 0, "No common formatter configuration found."

def check_gitignore() -> Tuple[bool, int, str]:
    """10. .gitignore with >5 lines → 5pts"""
    lines = read_file_lines(".gitignore")
    if lines:
        # Filter out empty lines and comment lines
        effective_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
        if len(effective_lines) > 5:
            return True, 5, f"'.gitignore' found with {len(effective_lines)} effective lines (>5)."
        return False, 0, f"'.gitignore' found but has only {len(effective_lines)} effective lines (<=5)."
    return False, 0, "'.gitignore' not found."

def check_ci_config() -> Tuple[bool, int, str]:
    """11. CI config (.github/workflows/*.yml or .circleci or .gitlab-ci.yml) → 5pts"""
    if os.path.isdir(os.path.join(".github", "workflows")):
        if find_files_in_dir(os.path.join(".github", "workflows"), r".*\.yml$"):
            return True, 5, "GitHub Actions workflow found in '.github/workflows/'."
    if os.path.isdir(".circleci"):
        return True, 5, "'.circleci/' directory found."
    if os.path.exists(".gitlab-ci.yml"):
        return True, 5, "'.gitlab-ci.yml' found."
    return False, 0, "No common CI configuration found."

def check_docs_dir() -> Tuple[bool, int, str]:
    """12. docs/ directory → 5pts"""
    if os.path.isdir("docs"):
        return True, 5, "'docs/' directory found."
    return False, 0, "'docs/' directory not found."

def check_root_md_agent_llm() -> Tuple[bool, int, str]:
    """13. Any root .md with "agent" or "LLM" → 5pts"""
    root_md_files = find_files_in_dir(".", r".*\.md$")
    for filepath in root_md_files:
        content = read_file_content(filepath)
        if content and (re.search(r"\bagent\b", content, re.IGNORECASE) or re.search(r"\bLLM\b", content)):
            return True, 5, f"'{filepath}' contains 'agent' or 'LLM'."
    return False, 0, "No root '.md' file contains 'agent' or 'LLM'."

def check_package_manager_config() -> Tuple[bool, int, str]:
    """14. package.json or pyproject.toml → 5pts"""
    if os.path.exists("package.json"):
        return True, 5, "'package.json' found."
    if os.path.exists("pyproject.toml"):
        return True, 5, "'pyproject.toml' found."
    return False, 0, "'package.json' or 'pyproject.toml' not found."

# --- All Checks List ---
ALL_CHECKS = [
    {"name": "README.md exists (and Architecture section)", "points": 10, "func": check_readme, "bonus": 3},
    {"name": "CONTRIBUTING.md exists", "points": 8, "func": check_contributing},
    {"name": "docs/architecture.md exists", "points": 7, "func": check_docs_architecture},
    {"name": "Agent instructions (CLAUDE.md, .cursorrules, .github/copilot-instructions.md)", "points": 10, "func": check_agent_instructions},
    {"name": "LICENSE exists", "points": 5, "func": check_license},
    {"name": "Tests directory (tests/ or test/)", "points": 8, "func": check_tests_dir},
    {"name": "Test configuration (pytest.ini, jest/vitest config, pyproject.toml with pytest)", "points": 9, "func": check_test_config},
    {"name": "Makefile with 'test' target", "points": 8, "func": check_makefile_test_target},
    {"name": "Formatter config (.prettierrc, .editorconfig, pyproject.toml with black, .eslintrc)", "points": 10, "func": check_formatter_config},
    {"name": ".gitignore with >5 effective lines", "points": 5, "func": check_gitignore},
    {"name": "CI config (.github/workflows/*.yml, .circleci, .gitlab-ci.yml)", "points": 5, "func": check_ci_config},
    {"name": "docs/ directory exists", "points": 5, "func": check_docs_dir},
    {"name": "Root .md with 'agent' or 'LLM'", "points": 5, "func": check_root_md_agent_llm},
    {"name": "Package manager config (package.json or pyproject.toml)", "points": 5, "func": check_package_manager_config},
]

# --- Main Logic ---
def run_checks() -> Dict[str, Any]:
    """Executes all checks and compiles results."""
    total_score = 0
    max_possible_score = sum(c["points"] + c.get("bonus", 0) for c in ALL_CHECKS)
    results: List[Dict[str, Any]] = []
    failed_checks: List[Dict[str, Any]] = []

    for check_info in ALL_CHECKS:
        passed, points_awarded, message = check_info["func"]()
        total_score += points_awarded
        result = {
            "name": check_info["name"],
            "passed": passed,
            "points_awarded": points_awarded,
            "max_points": check_info["points"] + check_info.get("bonus", 0),
            "message": message
        }
        results.append(result)
        if not passed:
            failed_checks.append({
                "name": check_info["name"],
                "potential_points": check_info["points"] + check_info.get("bonus", 0),
                "message": message
            })

    # Sort failed checks by potential points for suggestions
    failed_checks.sort(key=lambda x: x["potential_points"], reverse=True)
    suggestions = [f"{f['name']} (worth {f['potential_points']} pts)" for f in failed_checks[:3]]

    return {
        "total_score": total_score,
        "max_possible_score": max_possible_score,
        "results": results,
        "suggestions": suggestions
    }

def get_grade(score: int) -> str:
    """Calculates letter grade based on score."""
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 40:
        return "D"
    else:
        return "F"

def print_results_cli(results_data: Dict[str, Any]) -> None:
    """Prints results to CLI with colorized output."""
    print(Colors.apply(Colors.BOLD + "Agent-Ready Repository Check\n", Colors.BLUE, IS_TTY))

    for result in results_data["results"]:
        status_icon = Colors.apply("✅", Colors.GREEN, IS_TTY) if result["passed"] else Colors.apply("❌", Colors.RED, IS_TTY)
        points_str = Colors.apply(f"[+{result['points_awarded']}pts]", Colors.GREEN, IS_TTY) if result["passed"] else Colors.apply("[+0pts]", Colors.RED, IS_TTY)
        print(f"{status_icon} {result['name']}: {result['message']} {points_str}")

    print(Colors.apply("\n--- Summary ---", Colors.BOLD, IS_TTY))
    total_score = results_data["total_score"]
    max_score = results_data["max_possible_score"]
    grade = get_grade(total_score)

    score_color = Colors.GREEN if total_score >= 75 else (Colors.YELLOW if total_score >= 40 else Colors.RED)
    grade_color = Colors.GREEN if grade in ("A", "B") else (Colors.YELLOW if grade == "C" else Colors.RED)

    print(f"Final Score: {Colors.apply(str(total_score), score_color, IS_TTY)}/{max_score} pts")
    print(f"Grade: {Colors.apply(grade, grade_color, IS_TTY)}")

    if results_data["suggestions"]:
        print(Colors.apply("\nTop 3 Improvement Suggestions:", Colors.BOLD, IS_TTY))
        for i, suggestion in enumerate(results_data["suggestions"]):
            print(f"  {i+1}. {Colors.apply(suggestion, Colors.YELLOW, IS_TTY)}")
    else:
        print(Colors.apply("\nGreat job! No immediate suggestions for improvement.", Colors.GREEN, IS_TTY))

def generate_badge_markdown(score: int, grade: str) -> str:
    """Generates Markdown badge text."""
    
    # Determine badge color based on grade
    badge_color = "brightgreen" # A, B
    if grade == "C":
        badge_color = "yellow"
    elif grade == "D":
        badge_color = "orange"
    elif grade == "F":
        badge_color = "red"

    label = quote("Agent Ready Score")
    message = quote(f"{score} {grade}")
    
    return f"![Agent Ready Score](https://img.shields.io/badge/{label}-{message}-{badge_color})"

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check if a repository is 'agent-ready' for AI coding agents."
    )
    parser.add_argument(
        "path", nargs="?", default=".",
        help="Path to the repository root (default: current directory)."
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output results in raw JSON format."
    )
    parser.add_argument(
        "--badge", action="store_true",
        help="Output Markdown badge text for the score."
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Exit with status 1 if the score is less than 75."
    )
    args = parser.parse_args()

    repo_path = os.path.abspath(args.path)
    if not os.path.isdir(repo_path):
        print(f"Error: '{repo_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(2)
    os.chdir(repo_path)

    results_data = run_checks()
    total_score = results_data["total_score"]
    grade = get_grade(total_score)

    if args.json:
        json_output = {
            "score": total_score,
            "max_score": results_data["max_possible_score"],
            "grade": grade,
            "checks": results_data["results"],
            "suggestions": results_data["suggestions"]
        }
        print(json.dumps(json_output, indent=2))
    elif args.badge:
        print(generate_badge_markdown(total_score, grade))
    else:
        print_results_cli(results_data)

    if args.strict and total_score < 75:
        sys.exit(1)

if __name__ == "__main__":
    main()
