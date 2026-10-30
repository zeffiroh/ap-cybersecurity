import re
from typing import Dict, List

_SQL_KEYWORD = re.compile(r"\b(SELECT|INSERT|UPDATE|DELETE)\b", re.IGNORECASE)
_DYNAMIC_BUILD = re.compile(r"\+|f[\"']|\.format\(|%\s*[\"']|[\"']\s*%")
_EVAL_USE = re.compile(r"\b(eval|exec)\s*\(")
_SECRET_ASSIGN = re.compile(
    r"\b\w*(password|secret|api_key|token)\w*\s*=\s*[\"']", re.IGNORECASE
)


def solve(lines: List[str]) -> List[Dict[str, object]]:
    findings = []
    for i, line in enumerate(lines, start=1):
        cats = set()
        if _SQL_KEYWORD.search(line) and _DYNAMIC_BUILD.search(line):
            cats.add("sql-injection-risk")
        if _EVAL_USE.search(line):
            cats.add("eval-use")
        if _SECRET_ASSIGN.search(line):
            cats.add("hardcoded-secret")
        for cat in cats:
            findings.append({"line": i, "category": cat})
    findings.sort(key=lambda f: (f["line"], f["category"]))
    return findings
