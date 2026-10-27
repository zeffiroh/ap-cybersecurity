"""Starter code for 1.4.c. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
import re
from typing import List


def solve(model_output: str) -> List[str]:
    """Detect sensitive data leaks in LLM output.

    Args:
        model_output: string of text produced by an LLM.
    Returns:
        Sorted list of leak-type names from: ['api-key', 'email', 'password', 'system-prompt'].
        Empty list if no leaks detected.
    """
    # TODO: implement regex-based detection per prompt.md
    raise NotImplementedError("implement solve() -- see prompt.md")
