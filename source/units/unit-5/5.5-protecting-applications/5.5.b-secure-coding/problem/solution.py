"""Reference solution for 5.5.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import Dict, List


def solve(config: Dict[str, object]) -> List[str]:
    """Audit an application configuration against the secure-coding rule set.

    Returns a sorted list of violated rule names (only rules that fail appear).
    """
    violations = []

    if config.get("debug_mode") is True:
        violations.append("debug-mode-enabled")

    if config.get("db_query_style") == "concatenated":
        violations.append("non-parameterized-query")

    if config.get("secrets_in_code") is True:
        violations.append("hardcoded-secret")

    if config.get("error_verbosity") == "verbose":
        violations.append("verbose-error-messages")

    if config.get("dependencies_pinned") is False:
        violations.append("unpinned-dependencies")

    if config.get("runs_as") == "root":
        violations.append("excessive-privilege")

    if config.get("code_review_required") is False:
        violations.append("no-code-review")

    return sorted(violations)
