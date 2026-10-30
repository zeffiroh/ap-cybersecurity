from typing import Dict, List


def solve(config: Dict[str, object]) -> List[str]:
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
