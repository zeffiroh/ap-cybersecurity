"""Starter code for 1.2.b. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""


def solve(password: str) -> dict:
    """Return a weakness report dict for the given password.

    Args:
        password: the candidate password string (may be empty).
    Returns:
        {"weak": bool, "reasons": list[str]} where reasons is a sorted list of
        triggered rule labels. Possible labels:
          "too_short"            -- len(password) < 12
          "in_dictionary"        -- password.lower() is in the common wordlist
          "only_lowercase"       -- password contains only a-z characters
          "sequential_or_repeated" -- run of 3+ sequential or identical chars
        See interface.md for the exact COMMON_WORDS set and detection algorithm.
    """
    # TODO: implement all four rules and return {"weak": ..., "reasons": [...]}
    raise NotImplementedError("implement solve() -- see prompt.md")
