"""Starter code for 1.3.c. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List

# Fixed detection constants (do not change)
THRESHOLD = 80   # noise floor threshold (strictly greater than)
WINDOW = 5       # minimum consecutive samples above threshold to flag jamming


def solve(samples: List[int]) -> bool:
    """Return True if the sample series contains a sustained jamming event.

    A series is flagged if it contains a run of at least WINDOW consecutive
    samples that are ALL strictly greater than THRESHOLD.

    Args:
        samples: list of integer noise-floor measurements
    Returns:
        True if jamming detected, False otherwise
    """
    # TODO: scan samples and detect a run of WINDOW consecutive values > THRESHOLD
    raise NotImplementedError("implement solve() — see prompt.md")
