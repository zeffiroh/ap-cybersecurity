"""Starter code for 1.4.b. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List

PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "disregard",
    "you are now",
    "system:",
]


def solve(prompt_text: str) -> List[str]:
    """Detect prompt-injection patterns in user input to an LLM application.

    Args:
        prompt_text: raw string of user-supplied input.
    Returns:
        Sorted list of matched pattern names (see PATTERNS and interface.md).
    """
    # TODO: implement per prompt.md — check each pattern against prompt_text (case-insensitive)
    raise NotImplementedError("implement solve() — see prompt.md")
